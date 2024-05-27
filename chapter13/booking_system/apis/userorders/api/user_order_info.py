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


@router_userorders.post("/user_order_info", summary='用户订单详情查看')
async def callbadk(forms: SubscribeOrderCheckForm, db_session: AsyncSession = Depends(depends_get_db_session)):
    # 获取预约详情信息列表
    doctor_nsnum_info_result = await Serveries.get_order_info_list_by_visit_uopenid_detailt(
        db_session,
        visit_uopenid=forms.visit_uopenid.strip(),
        orderid=forms.orderid.strip(),
        dno=forms.dno.strip(),
    )
    # is_reserve -属性 1:表示可以点击预约  2：有排班记录，但是已预约满
    return Success(api_code=200, result=doctor_nsnum_info_result, message='查询成功') if doctor_nsnum_info_result else Fail(
        api_code=200, result=None, message='无此订单状态列表信息！')
