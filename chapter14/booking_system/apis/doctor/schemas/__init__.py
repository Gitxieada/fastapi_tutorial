from pydantic import BaseModel


class SchedulingInfo(BaseModel):
    # 预约医生编号
    dno: str
    # 预约时间
    start_time: str = None


class MakeReserveOrderForm(BaseModel):
    # 预约医生编号
    dno: str
    # 预约医生排号时段
    nsindex: str


class PayReserveOrderForm(BaseModel):
    # 预约医生编号
    dno: str
    # 预约医生排号时段
    nsindex: str
    # 预约人信息
    visit_uname: str
    visit_uphone: str
    visit_uopenid: str = None
    visit_usex: str
    visit_uage: str
