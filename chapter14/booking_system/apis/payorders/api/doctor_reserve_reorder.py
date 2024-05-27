from fastapi import Depends
from apis.payorders.repository import PayOrderServeries
from db.async_database import depends_get_db_session
from db.async_database import AsyncSession
from exts.responses.json_response import Success, Fail
from apis.payorders.api import router_payorders
from apis.payorders.schemas import PayCancelPayOrderForm
from exts.wechatpy.pay import WeChatPay, WeChatPayException
from apis.payorders.dependencies import get_client_ip
from utils import datatime_helper, json_helper
from config.config import get_settings
import decimal


@router_payorders.get("/doctor_reserve_order", summary='未支付订单重新发起支付')
async def callbadk(forms: PayCancelPayOrderForm = Depends(),
                   db_session: AsyncSession = Depends(depends_get_db_session),
                   client_ip: str = Depends(get_client_ip)):
    # 获取预约详情信息列表
    doctor_order_info_result = await PayOrderServeries.get_order_info_dno_orderid_visituopenid_state(
        db_session,
        visit_uopenid=forms.visit_uopenid.strip(),
        orderid=forms.orderid.strip(),
        dno=forms.dno.strip(),
    )
    print(doctor_order_info_result.dno)
    # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单 5：申请退款状态 6：已退款状态）
    # 先查询出上次下单的记录到的信息
    if not doctor_order_info_result:
        return Fail(api_code=200, result=None, message='无此订单记录信息！')

    if doctor_order_info_result.statue == 4:
        return Fail(api_code=200, result=None, message='订单已超时未支付！建议取消重新下单！')

    # 对订单信息进行校验，只有未付款的清单信息才可以继续下一步的支付的操作
    if doctor_order_info_result.statue != 1:
        return Fail(api_code=200, result=None, message='订单信息状态异常信息！无法继续支付！建议取消重新下单！')

    # 查询当前预约时段
    nsindex = doctor_order_info_result.nsindex
    # 查询排班信息
    doctor_nsnum_info_result = await PayOrderServeries.get_doctor_scheduling_info_info_order(db_session, dno=forms.dno,
                                                                                             nsindex=nsindex)
    if not doctor_nsnum_info_result:
        return Fail(api_code=200, result=None, message='无排班记录信息!')

    # 对比当前的预约时段是否有效
    print('doctor_nsnum_info_result.tiempm', doctor_nsnum_info_result.tiempm)
    if not datatime_helper.effectiveness_tiempm(str(doctor_nsnum_info_result.tiempm)):
        return Fail(api_code=200, result=None, message='当前预约时段无效!请更换另一个时段进行预约！')

    order_info = {
        'dno': forms.dno,
        'nsindex': nsindex,
        'orderid': doctor_order_info_result.orderid if doctor_order_info_result.orderid else None,
        'visit_uphone': doctor_order_info_result.visit_uphone,
        'visit_uopenid': forms.visit_uopenid,
        'visittime': doctor_order_info_result.visittime
    }

    # 新手支付生成
    try:
        wx_pay = WeChatPay(appid=get_settings().GZX_ID, api_key=get_settings().GZX_PAY_KEY,
                           mch_id=get_settings().MCH_ID)
        orderid = doctor_order_info_result.orderid
        order_info_json = json_helper.dict_to_json(order_info)
        payfee = doctor_order_info_result.payfee
        visittime = doctor_order_info_result.visittime
        # =================
        doctor_info_result = await PayOrderServeries.get_doctor_info(db_session, dno=forms.dno)
        dnname = doctor_info_result.dnname

        # 解决办法：01商户订单号重复 问题
        # 保证再次支付下单时发起的请求参数和第一次一样。
        # 商品描述
        body = f'XXX中医馆诊费'
        # 商品详细描述
        detail = f'XXX中医馆预约时段:{visittime}'
        # 总金额，单位分
        total_fee = decimal.Decimal(payfee) * 100
        # total_fee = 1
        # 订单支付成功回调通知
        notify_url = get_settings().NOTIFY_URL
        # out_trade_no - 商户系统内部订单号
        # 回调透传信息 attach-在查询API和支付通知中原样返回，可作为自定义参数使用。
        attach = f"{forms.dno}|{orderid}|{nsindex}"
        # 支付响应回调对象
        pay_wx_res_result = wx_pay.order.create(
            trade_type='JSAPI',
            body=body,
            detail=detail,
            total_fee=total_fee,
            client_ip=client_ip,
            notify_url=notify_url,
            attach=attach,
            user_id=forms.visit_uopenid,
            out_trade_no=orderid
        )
    except WeChatPayException as wcpayex:
        # 记录请求异常回调信息
        order_info['wcpayex.errmsg'] = wcpayex.errmsg
        return Fail(api_code=200, result=None, message=f'微信支付配置服务异常，请稍后重试！！错误提示{wcpayex.errmsg}')
    except Exception:
        import traceback
        traceback.print_exc()
        return Fail(api_code=200, result=None, message='微信支付服务未知错误异常，请稍后重试！！')

    return_code = pay_wx_res_result.get('return_code')
    if return_code == 'SUCCESS':
        # 提取相关的参数信息
        wx_gzx_id = pay_wx_res_result.get('appid')
        wx_mch_id = pay_wx_res_result.get('mch_id')
        sign = pay_wx_res_result.get('sign')
        nonce_str = pay_wx_res_result.get('nonce_str')
        prepay_id = pay_wx_res_result.get('prepay_id')

        # 二次前面返回相关的支付信息
        timestamp = str(datatime_helper.get_timestamp10())
        wx_jsapi_data = wx_pay.order.get_appapi_params_xiugai(prepay_id=pay_wx_res_result.get('prepay_id'),
                                                              timestamp=timestamp,
                                                              nonce_str=pay_wx_res_result.get('nonce_str'))

        #  更新当前支付的订单信息
        # 更新没有支付的成功的订单的，状态！
        doctor_nsnum_info_result = await PayOrderServeries.updata_order_info_byorder_dno(db_session,
                                                                                         dno=forms.dno,
                                                                                         orderid=forms.orderid,
                                                                                         visit_uopenid=forms.visit_uopenid,
                                                                                         statue=1,
                                                                                         )
        if doctor_nsnum_info_result:
            return Success(api_code=200, result={'orderid': orderid, 'wx_info': wx_jsapi_data},
                           message='您已提交订单，请尽快支付哟！')
        else:
            order_info['creat_order_info_error'] = '创建订单到数据库的时候异常'
            return Fail(api_code=200, result=None, message='微信服务请求处理异常，请稍后重试！！')

    else:
        # 记录请求异常回调信息
        order_info['wx_return_code'] = pay_wx_res_result.get('return_code')
        order_info['wx_return_msg'] = pay_wx_res_result.get('return_msg')
        return Fail(api_code=200, result=None, message='微信服务请求处理异常，请稍后重试！！')
