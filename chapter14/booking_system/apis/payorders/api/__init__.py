from fastapi import APIRouter
router_payorders = APIRouter(prefix='/api/v1',tags=["支付订单模块"])
from apis.payorders.api import doctor_reserve_order
from apis.payorders.api import payback_reserve_order
from apis.payorders.api import reserve_order_info
from apis.payorders.api import doctor_reserve_reorder
from apis.payorders.api import doctor_order_check