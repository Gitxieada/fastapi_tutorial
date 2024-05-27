from fastapi import Query
from pydantic import BaseModel


class SchedulingInfo(BaseModel):
    # 预约医生编号
    dno: str
    # 预约时间
    start_time:str = None


class MakeReserveOrderForm(BaseModel):
    # 预约医生编号
    dno: str
    # 预约医生排号时段
    nsindex: str



class SubscribeOrderCheckForm(BaseModel):
    # 新增需要时段索引排班索引编号
    dno: str = Query(...,min_length=1,description="医生编号ID")
    orderid: str = Query(..., min_length=1, description="订单编号ID")
    visit_uopenid: str = Query(..., min_length=1, description="就诊人微信ID")




class PayReserveOrderForm(BaseModel):
    # 预约医生编号
    dno: str
    # 预约医生排号时段
    nsindex: str
    # 预约人信息
    visit_uname: str
    visit_uphone: str
    visit_uopenid:str =None
    visit_usex:str
    visit_uage:str


class PayCancelPayOrderForm(BaseModel):
    '''
    下单需要相关字段信息
    '''
    visit_uopenid: str = Query(..., min_length=1,description="就诊人微信ID")
    # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单 5：申请退款状态 6：已退款状态）
    orderid:str
    # 预约医生的编号
    dno:str

