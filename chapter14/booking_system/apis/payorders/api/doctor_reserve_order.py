from fastapi import Depends
from apis.payorders.repository import PayOrderServeries
from apis.doctor.repository import DoctorServeries
from db.async_database import depends_get_db_session
from db.async_database import AsyncSession
from exts.responses.json_response import Success, Fail
from utils.datatime_helper import num_to_string, get_timestamp10
from apis.payorders.api import router_payorders
from apis.payorders.schemas import PayReserveOrderForm
from utils.datatime_helper import datetime
from utils import ordernum_helper,json_helper
from exts.wechatpy.pay import WeChatPay, WeChatPayException
from config.config import get_settings
from apis.payorders.dependencies import get_client_ip
# 初始化同步连接rabbitmq
from exts.rabbit import sync_rabbit_client
from exts.async_rabbit import async_rabbit_client
import decimal
from asgiref.sync import sync_to_async

@router_payorders.post("/doctor_reserve_order", summary='填写预约人员信息,处理订单的提交')
async def callbadk(forms: PayReserveOrderForm,
                   db_session: AsyncSession = Depends(depends_get_db_session),
                   client_ip: str = Depends(get_client_ip)):
    # 检测是否没支付的订单信息，取消或支付后才可以继续操作预约
    get_order_info = await PayOrderServeries.get_order_info_byvisit_uopenid_state(db_session,
                                                                                  visit_uopenid=forms.visit_uopenid,
                                                                                  statue=1)
    if get_order_info:
        return Fail(api_code=200, result=None, message='您当前存在未支付的订单记录，请支付或取消后再操作！')

    # 下单处理
    doctor_result, doctor_nsnuminfo_result = await DoctorServeries.get_doctor_curr_nsindex_scheduling_info(db_session,
                                                                                                           dno=forms.dno,
                                                                                                           nsindex=forms.nsindex)
    if not doctor_nsnuminfo_result:
        return Fail(api_code=200, result=None, message='排班信息不存在！！')

    tiempmss = str(doctor_nsnuminfo_result.tiempm).split(' ')[1].split(':')
    visitday = str(doctor_nsnuminfo_result.dnotime)
    visitdaytime = f"{visitday} {tiempmss[0]}:{tiempmss[1]}:00"
    tiemampmstr = doctor_nsnuminfo_result.tiemampmstr
    visittime = '{} {} {}'.format(num_to_string(doctor_nsnuminfo_result.dnotime.isoweekday()),
                                  '上午' if doctor_nsnuminfo_result.ampm == 'am' else '下午', tiemampmstr)
    # 订单编号
    orderid = ordernum_helper.order_num_3(user_num=forms.visit_uphone)
    payfee = str(doctor_result.fee)
    order_info = {
        'dno': forms.dno,
        'nsindex': forms.nsindex,
        'orderid': orderid,
        'visit_uphone': forms.visit_uphone,
        'visit_uopenid': forms.visit_uopenid,
        'visittime': visittime
    }
    # 开始提交微信支付生成订单信息
    order_info_json = json_helper.dict_to_json(order_info)
    # 支付订单生成，但是注意的地方是，这里因为是同步的的，这里回引起阻塞哟！
    wx_pay = WeChatPay(appid=get_settings().GZX_ID, api_key=get_settings().GZX_PAY_KEY, mch_id=get_settings().MCH_ID)
    try:
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
        attach = f"{forms.dno}|{orderid}|{forms.nsindex}"
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
        pass
    except WeChatPayException as wcpayex:
        # 记录请求异常回调信息
        order_info['wcpayex.return_msg'] = wcpayex.errmsg
        print(wcpayex.errmsg)
        return Fail(api_code=200, result=None, message=f'微信支付配置服务异常，请稍后重试！！{wcpayex.errmsg}')
    except Exception:
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
        timestamp = str(get_timestamp10())
        wx_jsapi_data = wx_pay.order.get_appapi_params_xiugai(prepay_id=pay_wx_res_result.get('prepay_id'),
                                                              timestamp=timestamp,
                                                              nonce_str=pay_wx_res_result.get('nonce_str'))



        creat_order_info_result = await PayOrderServeries.creat_order_info(db_session, dno=forms.dno,
                                                                           orderid=orderid,
                                                                           # 订单所属-支付诊费
                                                                           payfee=payfee,
                                                                           visit_uname=forms.visit_uname,
                                                                           visit_uopenid=forms.visit_uopenid,
                                                                           visit_uphone=forms.visit_uphone,
                                                                           visit_usex=forms.visit_usex,
                                                                           visit_uage=forms.visit_uage,
                                                                           # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单）
                                                                           statue=1,
                                                                           # 订单所属-就诊状态（0:待预约 1：待就诊 2：已就诊）
                                                                           visit_statue=0,
                                                                           # 订单所属-就诊日期
                                                                           visitday=visitday,
                                                                           # 订单所属-就诊时间（周x-上午-8：00）
                                                                           visittime=visittime,
                                                                           create_time=datetime.datetime.now(),
                                                                           # =========================
                                                                           nsindex=forms.nsindex
                                                                           )


        # 订单创建完成后，需要执行预约号源数的库存扣减

        # 开始发送订单到消息队列中
        # 获取消息操作事件- 15分钟（函数内部已经*1000）
        pay_message_ttl = 60 * 15
        order_exchange_name = 'xz-order-exchange'
        order_routing_key = 'order_handler'
        sync_rabbit_client.send_basic_publish(exchange_name=order_exchange_name, routing_key=order_routing_key,
                                              body=order_info_json, content_type='application/json', is_delay=True,
                                              message_ttl=pay_message_ttl)

        if creat_order_info_result:
            return Success(api_code=200, result={'orderid': orderid, 'wx_info': wx_jsapi_data}, message='订单预约成功！')

    # 记录请求异常回调信息
    return Fail(api_code=200, result=None, message='微信服务请求处理异常，请稍后重试！！')


@router_payorders.post("/doctor_reserve_order_async", summary='填写预约人员信息,处理订单的提交')
async def callbadk(forms: PayReserveOrderForm,
                   db_session: AsyncSession = Depends(depends_get_db_session),
                   client_ip: str = Depends(get_client_ip)):
    # 检测是否没支付的订单信息，取消或支付后才可以继续操作预约
    get_order_info = await PayOrderServeries.get_order_info_byvisit_uopenid_state(db_session,
                                                                                  visit_uopenid=forms.visit_uopenid,
                                                                                  statue=1)
    if get_order_info:
        return Fail(api_code=200, result=None, message='您当前存在未支付的订单记录，请支付或取消后再操作！')

    # 下单处理
    doctor_result, doctor_nsnuminfo_result = await DoctorServeries.get_doctor_curr_nsindex_scheduling_info(db_session,
                                                                                                           dno=forms.dno,
                                                                                                           nsindex=forms.nsindex)
    if not doctor_nsnuminfo_result:
        return Fail(api_code=200, result=None, message='排班信息不存在！！')

    tiempmss = str(doctor_nsnuminfo_result.tiempm).split(' ')[1].split(':')
    visitday = str(doctor_nsnuminfo_result.dnotime)
    visitdaytime = f"{visitday} {tiempmss[0]}:{tiempmss[1]}:00"
    tiemampmstr = doctor_nsnuminfo_result.tiemampmstr
    visittime = '{} {} {}'.format(num_to_string(doctor_nsnuminfo_result.dnotime.isoweekday()),
                                  '上午' if doctor_nsnuminfo_result.ampm == 'am' else '下午', tiemampmstr)
    # 订单编号
    orderid = ordernum_helper.order_num_3(user_num=forms.visit_uphone)
    payfee = str(doctor_result.fee)
    order_info = {
        'dno': forms.dno,
        'nsindex': forms.nsindex,
        'orderid': orderid,
        'visit_uphone': forms.visit_uphone,
        'visit_uopenid': forms.visit_uopenid,
        'visittime': visittime
    }
    # 开始提交微信支付生成订单信息
    order_info_json = json_helper.dict_to_json(order_info)
    # 支付订单生成，但是注意的地方是，这里因为是同步的的，这里回引起阻塞哟！
    wx_pay = WeChatPay(appid=get_settings().GZX_ID, api_key=get_settings().GZX_PAY_KEY, mch_id=get_settings().MCH_ID)
    try:
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
        attach = f"{forms.dno}|{orderid}|{forms.nsindex}"
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
        pass
    except WeChatPayException as wcpayex:
        # 记录请求异常回调信息
        order_info['wcpayex.return_msg'] = wcpayex.errmsg
        print(wcpayex.errmsg)
        return Fail(api_code=200, result=None, message=f'微信支付配置服务异常，请稍后重试！！{wcpayex.errmsg}')
    except Exception:
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
        timestamp = str(get_timestamp10())
        wx_jsapi_data = wx_pay.order.get_appapi_params_xiugai(prepay_id=pay_wx_res_result.get('prepay_id'),
                                                              timestamp=timestamp,
                                                              nonce_str=pay_wx_res_result.get('nonce_str'))



        creat_order_info_result = await PayOrderServeries.creat_order_info(db_session, dno=forms.dno,
                                                                           orderid=orderid,
                                                                           # 订单所属-支付诊费
                                                                           payfee=payfee,
                                                                           visit_uname=forms.visit_uname,
                                                                           visit_uopenid=forms.visit_uopenid,
                                                                           visit_uphone=forms.visit_uphone,
                                                                           visit_usex=forms.visit_usex,
                                                                           visit_uage=forms.visit_uage,
                                                                           # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单）
                                                                           statue=1,
                                                                           # 订单所属-就诊状态（0:待预约 1：待就诊 2：已就诊）
                                                                           visit_statue=0,
                                                                           # 订单所属-就诊日期
                                                                           visitday=visitday,
                                                                           # 订单所属-就诊时间（周x-上午-8：00）
                                                                           visittime=visittime,
                                                                           create_time=datetime.datetime.now(),
                                                                           # =========================
                                                                           nsindex=forms.nsindex
                                                                           )


        # 订单创建完成后，需要执行预约号源数的库存扣减

        # 开始发送订单到消息队列中
        # 获取消息操作事件- 15分钟（函数内部已经*1000）
        pay_message_ttl = 5
        order_exchange_name = 'xz-order-exchange1'
        order_routing_key = 'order_handler1'
        await async_rabbit_client.send_basic_publish(routing_key=order_routing_key,
                                              body=order_info_json, content_type='application/json', is_delay=True,
                                              message_ttl=pay_message_ttl)

        if creat_order_info_result:
            return Success(api_code=200, result={'orderid': orderid, 'wx_info': wx_jsapi_data}, message='订单预约成功！')

    # 记录请求异常回调信息
    return Fail(api_code=200, result=None, message='微信服务请求处理异常，请稍后重试！！')


@router_payorders.post("/doctor_reserve_order_async_as_tarn", summary='填写预约人员信息,处理订单的提交')
async def callbadk(forms: PayReserveOrderForm,
                   db_session: AsyncSession = Depends(depends_get_db_session),
                   client_ip: str = Depends(get_client_ip)):
    # 检测是否没支付的订单信息，取消或支付后才可以继续操作预约
    get_order_info = await PayOrderServeries.get_order_info_byvisit_uopenid_state(db_session,
                                                                                  visit_uopenid=forms.visit_uopenid,
                                                                                  statue=1)
    if get_order_info:
        return Fail(api_code=200, result=None, message='您当前存在未支付的订单记录，请支付或取消后再操作！')

    # 下单处理
    doctor_result, doctor_nsnuminfo_result = await DoctorServeries.get_doctor_curr_nsindex_scheduling_info(db_session,
                                                                                                           dno=forms.dno,
                                                                                                           nsindex=forms.nsindex)
    if not doctor_nsnuminfo_result:
        return Fail(api_code=200, result=None, message='排班信息不存在！！')

    tiempmss = str(doctor_nsnuminfo_result.tiempm).split(' ')[1].split(':')
    visitday = str(doctor_nsnuminfo_result.dnotime)
    visitdaytime = f"{visitday} {tiempmss[0]}:{tiempmss[1]}:00"
    tiemampmstr = doctor_nsnuminfo_result.tiemampmstr
    visittime = '{} {} {}'.format(num_to_string(doctor_nsnuminfo_result.dnotime.isoweekday()),
                                  '上午' if doctor_nsnuminfo_result.ampm == 'am' else '下午', tiemampmstr)
    # 订单编号
    orderid = ordernum_helper.order_num_3(user_num=forms.visit_uphone)
    payfee = str(doctor_result.fee)
    order_info = {
        'dno': forms.dno,
        'nsindex': forms.nsindex,
        'orderid': orderid,
        'visit_uphone': forms.visit_uphone,
        'visit_uopenid': forms.visit_uopenid,
        'visittime': visittime
    }
    # 开始提交微信支付生成订单信息
    order_info_json = json_helper.dict_to_json(order_info)
    # 支付订单生成，但是注意的地方是，这里因为是同步的的，这里回引起阻塞哟！




    wx_pay = WeChatPay(appid=get_settings().GZX_ID, api_key=get_settings().GZX_PAY_KEY, mch_id=get_settings().MCH_ID)
    try:
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
        attach = f"{forms.dno}|{orderid}|{forms.nsindex}"
        # 支付响应回调对象

        pay_wx_res_result = await sync_to_async(func=wx_pay.order.create)(trade_type='JSAPI',
            body=body,
            detail=detail,
            total_fee=total_fee,
            client_ip=client_ip,
            notify_url=notify_url,
            attach=attach,
            user_id=forms.visit_uopenid,
            out_trade_no=orderid)

        # pay_wx_res_result = wx_pay.order.create(
        #     trade_type='JSAPI',
        #     body=body,
        #     detail=detail,
        #     total_fee=total_fee,
        #     client_ip=client_ip,
        #     notify_url=notify_url,
        #     attach=attach,
        #     user_id=forms.visit_uopenid,
        #     out_trade_no=orderid
        # )
        pass
    except WeChatPayException as wcpayex:
        # 记录请求异常回调信息
        order_info['wcpayex.return_msg'] = wcpayex.errmsg
        print(wcpayex.errmsg)
        return Fail(api_code=200, result=None, message=f'微信支付配置服务异常，请稍后重试！！{wcpayex.errmsg}')
    except Exception:
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
        timestamp = str(get_timestamp10())
        wx_jsapi_data = wx_pay.order.get_appapi_params_xiugai(prepay_id=pay_wx_res_result.get('prepay_id'),
                                                              timestamp=timestamp,
                                                              nonce_str=pay_wx_res_result.get('nonce_str'))



        creat_order_info_result = await PayOrderServeries.creat_order_info(db_session, dno=forms.dno,
                                                                           orderid=orderid,
                                                                           # 订单所属-支付诊费
                                                                           payfee=payfee,
                                                                           visit_uname=forms.visit_uname,
                                                                           visit_uopenid=forms.visit_uopenid,
                                                                           visit_uphone=forms.visit_uphone,
                                                                           visit_usex=forms.visit_usex,
                                                                           visit_uage=forms.visit_uage,
                                                                           # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单）
                                                                           statue=1,
                                                                           # 订单所属-就诊状态（0:待预约 1：待就诊 2：已就诊）
                                                                           visit_statue=0,
                                                                           # 订单所属-就诊日期
                                                                           visitday=visitday,
                                                                           # 订单所属-就诊时间（周x-上午-8：00）
                                                                           visittime=visittime,
                                                                           create_time=datetime.datetime.now(),
                                                                           # =========================
                                                                           nsindex=forms.nsindex
                                                                           )


        # 订单创建完成后，需要执行预约号源数的库存扣减

        # 开始发送订单到消息队列中
        # 获取消息操作事件- 15分钟（函数内部已经*1000）
        pay_message_ttl = 5
        order_exchange_name = 'xz-order-exchange1'
        order_routing_key = 'order_handler1'
        await async_rabbit_client.send_basic_publish(routing_key=order_routing_key,
                                              body=order_info_json, content_type='application/json', is_delay=True,
                                              message_ttl=pay_message_ttl)

        if creat_order_info_result:
            return Success(api_code=200, result={'orderid': orderid, 'wx_info': wx_jsapi_data}, message='订单预约成功！')

    # 记录请求异常回调信息
    return Fail(api_code=200, result=None, message='微信服务请求处理异常，请稍后重试！！')
