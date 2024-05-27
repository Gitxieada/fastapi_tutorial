from fastapi import APIRouter
router_userorders = APIRouter(prefix='/api/v1', tags=["用户订单模块"])
from apis.userorders.api import refund_reserve_order, unpay_reserve_order, user_order_info, user_order_list, \
    wxauth_login
