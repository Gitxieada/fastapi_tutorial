
from pydantic import BaseModel
from fastapi import Depends, Query
from pydantic.dataclasses import dataclass


class SubscribeOrderCheckForm(BaseModel):
    # 新增需要时段索引排班索引编号
    dno: str = Query(...,min_length=1,description="医生编号ID")
    orderid: str = Query(..., min_length=1, description="订单编号ID")
    visit_uopenid: str = Query(..., min_length=1, description="就诊人微信ID")

class UserOrderIonfoListForm(BaseModel):
    '''
    下单需要相关字段信息
    '''
    visit_uopenid: str = Query(..., min_length=1,description="就诊人微信ID")
    # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单 5：申请退款状态 6：已退款状态）
    statue:int = None


class WxCodeForm(BaseModel):
    code: str = Query(..., min_length=1,description="微信CODE")


@dataclass
class GetOrderinfos(BaseModel):
    '''
    连表查询出来的位置要字段要保持一致信息
    '''
    orderid: str
    statue:int
    dno:str
    visittime:str
    visitday:str
    visit_statue:int
    dnname:str
    addr:str
    rank:str
    pic:str
