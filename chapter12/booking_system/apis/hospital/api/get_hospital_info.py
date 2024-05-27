from fastapi import Depends
from apis.hospital.repository import HospitalServeries
from db.async_database import depends_get_db_session
from db.async_database import AsyncSession
from exts.responses.json_response import Success
from ..api import router_hospital


@router_hospital.get("/hospital_info", summary='获取医院信息')
async def callbadk(db_session: AsyncSession = Depends(depends_get_db_session)):
    info = await HospitalServeries.get_hospital_info(db_session, id=1)
    return Success(result=info)
