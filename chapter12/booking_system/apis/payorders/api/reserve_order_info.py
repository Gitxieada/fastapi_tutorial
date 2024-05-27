from fastapi import Depends
from apis.doctor.repository import DoctorServeries
from db.async_database import depends_get_db_session
from db.async_database import AsyncSession
from exts.responses.json_response import Success, Fail
from utils.datatime_helper import num_to_string
from apis.payorders.api import router_payorders
from apis.payorders.schemas import MakeReserveOrderForm
from utils.datatime_helper import diff_days_for_now_time



@router_payorders.post("/reserve_order_info", summary='获取预约订单信息')
async def callbadk(forms: MakeReserveOrderForm, db_session: AsyncSession = Depends(depends_get_db_session)):
    # 查询预约信息
    doctor_result, doctor_nsnuminfo_result = await DoctorServeries.get_doctor_curr_nsindex_scheduling_info(db_session,
                                                                                                           dno=forms.dno,
                                                                                                           nsindex=forms.nsindex)
    if not doctor_result:
        return Fail(message="当前医生信息不存在！")
    if not doctor_nsnuminfo_result:
        return Fail(message="当前医生无此排班信息！")
    # 已消耗的库存预约数
    if doctor_nsnuminfo_result.nsnumstock <= 0:
        return Fail(message="当前时段预约已无号！")
        # 过期的不显示处理
    is_limt_start_time = diff_days_for_now_time(str(doctor_nsnuminfo_result.dnotime))
    if is_limt_start_time < 0:
        return Fail(message="当前日期无效,无排班信息!")
    backresult = {
        'dnotime': str(doctor_nsnuminfo_result.dnotime),
        'dnoampm_tag': '{} {} {}'.format(
            num_to_string(doctor_nsnuminfo_result.dnotime.isoweekday()),
            '上午' if doctor_nsnuminfo_result.ampm == 'am' else '下午',
            doctor_nsnuminfo_result.tiemampmstr
        )
    }
    return Success(result={**doctor_result, **backresult}) if doctor_result else Fail(message="无当前医生排班信息")