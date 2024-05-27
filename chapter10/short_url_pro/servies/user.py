from sqlalchemy import select, update, delete,func
from sqlalchemy.ext.asyncio import AsyncSession

from models.model import User
from db.database import async_engine, Base
from utils.passlib_hepler import PasslibHelper


class UserServeries:

    @staticmethod
    async def init_create_table():
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def get_user(async_session: AsyncSession, user_id: int):
        result = await async_session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def get_user_by_name(async_session: AsyncSession, username: str) -> User:
        result = await async_session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    @staticmethod
    async def get_users(async_session: AsyncSession):
        result = await async_session.execute(select(User).order_by(User.id))
        return result.scalars().fetchall()

    @staticmethod
    async def create_user(async_session: AsyncSession, **kwargs):
        new_user = User(**kwargs)
        async_session.add(new_user)
        await async_session.commit()
        return new_user

    @staticmethod
    async def update_user(async_session: AsyncSession, user_id: int, **kwargs):
        response = update(User).where(User.id == user_id)
        result = await async_session.execute(response.values(**kwargs))
        await async_session.commit()
        return result

    @staticmethod
    async def delete_user(async_session: AsyncSession, user_id: int):
        response = await async_session.execute(delete(User).where(User.id == user_id))
        await async_session.commit()
        return response


if __name__ == '__main__':
    import asyncio

    print(PasslibHelper.hash_password("123456"))
    from dependencies import get_db_session_asynccont
    async def create_admin_user():
        async with get_db_session_asynccont() as async_session:
            await UserServeries.create_user(async_session, username="admin",
                                            password=(PasslibHelper.hash_password("123456")),
                                            created_at=func.now()
                                            )
    asyncio.run(create_admin_user())
