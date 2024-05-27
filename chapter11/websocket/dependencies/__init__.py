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