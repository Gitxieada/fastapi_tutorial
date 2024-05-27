from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Hospitalinfo
from db.async_database import async_engine, Base


class HospitalServeries:

    @staticmethod
    async def get_hospital_info(async_session: AsyncSession, id: int):
        _result = await async_session.execute(
            select(Hospitalinfo.name, Hospitalinfo.describe, Hospitalinfo.describeimages).where(Hospitalinfo.id == id))
        scalars_result = _result.first()
        # scalars_result = _result.scalars().first()
        return scalars_result
