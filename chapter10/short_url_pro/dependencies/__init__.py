from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from db.database import SessionLocal

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db_session = None
    try:
        db_session = SessionLocal()
        yield db_session
    finally:
        await db_session.close()

from contextlib import asynccontextmanager
@asynccontextmanager
async def get_db_session_asynccont() -> AsyncGenerator:
    async_session = SessionLocal()
    try:
        yield async_session
        await async_session.commit()
    except SQLAlchemyError as ex:
        await async_session.rollback()
        raise ex
    finally:
        await async_session.close()