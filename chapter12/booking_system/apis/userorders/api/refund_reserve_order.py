from fastapi import Depends
from db.async_database import depends_get_db_session
from db.async_database import AsyncSession
from exts.responses.json_response import Success, Fail
from utils.datatime_helper import currday_time_info_tochane_datetime
from ..api import router_userorders
from ..schemas import SubscribeOrderCheckForm
from ..repository import Serveries
import datetime
import time


@router_userorders.put("/refund_reserve_order", summary='订单退款申请')
async def callbadk(forms: SubscribeOrderCheckForm, db_session: AsyncSession = Depends(depends_get_db_session)):
    # 检测订单的状态
    doctor_nsnum_info_result = await Serveries.get_order_info_byorder_dno_state(db_session, dno=forms.dno,
                                                                                orderid=forms.orderid)
    if not doctor_nsnum_info_result:
        return Fail(api_code=200, result=None, message='暂无此订单记录信息！')

    if doctor_nsnum_info_result.statue == 1:
        pass
        # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单）
        return Fail(api_code=200, result=None, message='该订单还为支付！无法申请退款！')

    if doctor_nsnum_info_result.statue == 5:
        pass
        return Fail(api_code=200, result=None, message='该订单处于申请退款状态,请勿重复操作！')

    if doctor_nsnum_info_result.statue == 3:
        pass
        # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单）
        return Fail(api_code=200, result=None, message='该订单已操作过取消！请勿重复操作！')

    if doctor_nsnum_info_result.statue == 4:
        pass
        # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单）
        return Fail(api_code=200, result=None, message='该已超时未支付,订单已过有效期！不可操作！')

    # 已经支付的订单信息
    if doctor_nsnum_info_result.statue == 2:
        pass
        # 来获取时间差中的秒数。注意，seconds获得的秒只是时间差中的小时、分钟和秒部分的和，并没有包含时间差的天数（既是两个时间点不是同一天，失效）
        today = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time())).replace("-", "")
        todaydate = datetime.datetime.strptime(today, "%Y%m%d %H:%M:%S")  # 字符串转化为date形式
        datiem = (currday_time_info_tochane_datetime(doctor_nsnum_info_result.visitday) - datetime.timedelta(days=1))
        subscribe_times = datetime.datetime.strptime(f"{str(datiem).replace('00:00:00', '')}23:59:59",
                                                     "%Y-%m-%d %H:%M:%S")
        # 当前时间小于预约时间的最后截止时间之后就不可以预约
        if todaydate >= subscribe_times:
            return Fail(api_code=200, result=None, message='非常抱歉，您已超过申请退款约定时间，暂无法给你申请退款处理！')

    isok = Serveries.updata_order_info_byorder_dno_olny(db_session, dno=forms.dno,
                                                        orderid=forms.orderid,
                                                        visit_uopenid=forms.visit_uopenid,
                                                        updata={
                                                            'statue': 5,
                                                            'refund_statue': 1,
                                                            'apply_refund_time': 'now()'
                                                        }
                                                        )
    return Success(api_code=200, result=None, message='申请退款成功！已提交审核！') if isok else Fail(api_code=200, result=None,
                                                                                         message='申请退款失败！')
