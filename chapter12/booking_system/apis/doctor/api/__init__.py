from fastapi import APIRouter
router_docrot = APIRouter(prefix='/api/v1',tags=["医生信息模块"],include_in_schema=True)
from ..api import  doctor_api