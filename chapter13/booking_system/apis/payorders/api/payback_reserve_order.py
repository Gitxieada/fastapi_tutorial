from fastapi import Depends, Request
from fastapi.responses import Response
from apis.payorders.repository import PayOrderServeries
from db.async_database import depends_get_db_session
from db.async_database import AsyncSession
from apis.payorders.api import router_payorders
from utils import xmlhelper
from exts.wechatpy.pay import WeChatPay, InvalidSignatureException
from config.config import get_settings
from exts.wechatpy.client import WeChatClient



@router_payorders.post("/payback_reserve_order", summary='支付订单回调处理')
async def callbadk(request: Request, db_session: AsyncSession = Depends(depends_get_db_session)):
    wx_pay = WeChatPay(appid=get_settings().GZX_ID, api_key=get_settings().GZX_PAY_KEY, mch_id=get_settings().MCH_ID)
    body = await request.body()
    try:
        _result = wx_pay.parse_payment_result(body)
    except InvalidSignatureException as e:
        # 日志记录
        _result = xmlhelper.parse_xml_data(body)
        out_trade_no = _result.get('out_trade_no')
        # 微信要求的回复的模式
        resXml = "<xml>" + "<return_code><![CDATA[FAIL]]></return_code>" + "<return_msg><![CDATA[签名不一致]]></return_msg>" + "</xml> "
        return Response(content=resXml, media_type="application/xml")

    except Exception as e:
        # 日志记录
        _result = xmlhelper.parse_xml_data(body)
        resXml = "<xml>" + "<return_code><![CDATA[FAIL]]></return_code>" + "<return_msg><![CDATA[签名不一致]]></return_msg>" + "</xml> "
        return Response(content=resXml, media_type="text/xml; charset=utf-8")

    if _result:
        # 返回状态码信息
        return_code = _result.get('return_code')

        # 处理状态码
        if return_code != 'SUCCESS':
            # 微信手机支付回调失败订单号
            resXml = "<xml>" + "<return_code><![CDATA[FAIL]]></return_code>" + "<return_msg><![CDATA[报文为空]]></return_msg>" + "</xml> "
            return Response(content=resXml, media_type="text/xml; charset=utf-8")

        # 业务错误处理结果
        result_code = _result.get('result_code')

        # 业务支付成功处理
        if result_code == 'SUCCESS':
            pass
            wx_gzx_id = _result.get('appid')
            attach = _result.get('attach')
            bank_type = _result.get('bank_type')
            cash_fee = _result.get('cash_fee')
            fee_type = _result.get('fee_type')
            is_subscribe = _result.get('is_subscribe')
            wx_mch_id = _result.get('mch_id')
            nonce_str = _result.get('nonce_str')
            openid = _result.get('openid')
            out_trade_no = _result.get('out_trade_no')
            time_end = _result.get('time_end')
            total_fee = _result.get('total_fee')
            trade_type = _result.get('trade_type')
            transaction_id = _result.get('transaction_id')

            # 回调透传信息 attach-在查询API和支付通知中原样返回，可作为自定义参数使用。
            #attach = f"{forms.dno}|{orderid}|{forms.nsindex}"
            attach_info = attach.split("|")
            attach_dno = attach_info[0]
            attach_orderid = attach_info[1]
            attach_visit_uopenid = openid
            attach_nsindex = attach_info[2]

            # 查询当前的订单的支付状态
            doctor_nsnum_info_result = await PayOrderServeries.get_order_info_byorder_dno_state(db_session, attach_dno,
                                                                                                attach_orderid)
            if not doctor_nsnum_info_result:
                resXml = "<xml>" + "<return_code><![CDATA[SUCCESS]]></return_code>" + "<return_msg><![CDATA[查无此订单信息]]></return_msg>" + "</xml> "
                return Response(content=resXml, media_type="text/xml; charset=utf-8")

            # 订单信息存在
            # 更新支付的成功状态！
            # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单 5：申请退款状态 6：已退款状态）
            if doctor_nsnum_info_result.statue == 2:
                resXml = "<xml>" + "<return_code><![CDATA[SUCCESS]]></return_code>" + "<return_msg><![CDATA[OK]]></return_msg>" + "</xml> "
                return Response(content=resXml, media_type="text/xml; charset=utf-8")

            isok, updata_result = await PayOrderServeries.updata_order_info_byorder_dno(db_session, dno=attach_dno,
                                                                                        orderid=attach_orderid,
                                                                                        visit_uopenid=attach_visit_uopenid,
                                                                                        updata={
                                                                                            'statue': 2,
                                                                                            # 标记已支付，待就诊！
                                                                                            'visit_statue': 1,
                                                                                            'notify_callback_time': 'now()',
                                                                                            'is_subscribe': is_subscribe,
                                                                                        }
                                                                                        )

            # 设置具体的点击通知URL地址为，查询订单详情页信息地址
            visittime = doctor_nsnum_info_result.visittime
            visitday = doctor_nsnum_info_result.visitday

            # 模板订单跳转地址详情信息
            template_url = f'http://xxxxxxxx/pages/orderDetailed/orderDetailed?did={attach_dno}&oid={attach_orderid}'
            if isok:
                # 开发发送预约成功的模板通知信息
                client = WeChatClient(appid=get_settings().GZX_ID, secret=get_settings().GZX_SECRET)
                # client.session = sync_redis_client
                resulst = client.message.send_template(to_user_openid=attach_visit_uopenid,
                                                       template_id='XXXXXXXXXXXXXXXXXXXXXX',
                                                       url=template_url,
                                                       data={
                                                           "first": {
                                                               "value": f"您预约挂号{visitday}{visittime}成功！",
                                                               "color": "#173177"
                                                           },
                                                           # 科室
                                                           "keyword2": {
                                                               "value": "中医科",
                                                               "color": "#173177"
                                                           },
                                                           # 就诊地址
                                                           "keyword3": {
                                                               "value": "XXXXXXXXXXXXXX中医馆",
                                                               "color": "#173177"
                                                           },
                                                           # 备注信息
                                                           "remark": {
                                                               "value": "本次预约成功，如需取消，请在就诊前一天申请，超过时间则申请无效，无法退费，谢谢谅解！",
                                                               "color": "#173177"
                                                           }
                                                       }
                                                       )
                # 响应微信支付回调处理
                resXml = "<xml>" + "<return_code><![CDATA[SUCCESS]]></return_code>" + "<return_msg><![CDATA[OK]]></return_msg>" + "</xml> "
                return Response(content=resXml, media_type="text/xml; charset=utf-8")
        else:
            resXml = "<xml>" + "<return_code><![CDATA[FAIL]]></return_code>" + "<return_msg><![CDATA[业务支付状态非SUCCESS]]></return_msg>" + "</xml> "
            return Response(content=resXml, media_type="text/xml; charset=utf-8")
    else:
        # 微信手机支付回调失败订单号
        resXml = "<xml>" + "<return_code><![CDATA[FAIL]]></return_code>" + "<return_msg><![CDATA[报文为空]]></return_msg>" + "</xml> "
        return Response(content=resXml, media_type="text/xml; charset=utf-8")
