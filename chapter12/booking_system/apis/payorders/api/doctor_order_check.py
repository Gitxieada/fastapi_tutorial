from fastapi import Depends
from apis.payorders.repository import PayOrderServeries
from apis.doctor.repository import DoctorServeries
from db.async_database import depends_get_db_session
from db.async_database import AsyncSession
from exts.responses.json_response import Success, Fail
from utils.datatime_helper import num_to_string, get_timestamp10
from apis.payorders.api import router_payorders
from apis.payorders.schemas import SubscribeOrderCheckForm
from utils.datatime_helper import datetime
from utils import ordernum_helper
from exts.wechatpy.pay import WeChatPay, WeChatPayException
from config.config import get_settings
from apis.payorders.dependencies import get_client_ip
from apis.payorders.repository import PayOrderServeries


@router_payorders.post("/doctor_order_check", summary='订单状态查询')
async def callbadk(forms: SubscribeOrderCheckForm=Depends(),
                   db_session: AsyncSession = Depends(depends_get_db_session),
                   client_ip: str = Depends(get_client_ip)):


    # 查询当前的订单的支付状态
    doctor_nsnum_info_result = await PayOrderServeries.get_order_info_dno_orderid_visituopenid_state(db_session,forms.dno,
                                                                                          forms.visit_uopenid,
                                                                                          forms.orderid)
    if not doctor_nsnum_info_result:
        return Fail(api_code=200, result=None, message='暂无此订单记录信息！')

    return Success(api_code=200, result={'status': doctor_nsnum_info_result.statue},
                   message='查询成功') if doctor_nsnum_info_result else Fail(api_code=200, result=None,
                                                                         message='无排班记录信息,或已过有效期')
