from fastapi import APIRouter
router_hospital = APIRouter(prefix='/api/v1',tags=["医院信息模块"])
# 導入模塊
from apis.hospital.api import get_hospital_info