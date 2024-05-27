from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.model import User
from db.database import async_engine, Base


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
    async def get_user_by_phone_number(async_session: AsyncSession, phone_number: str) -> User:
        result = await async_session.execute(select(User).where(User.phone_number == phone_number))
        return result.scalars().first()

    @staticmethod
    async def check_user_phone_number_and_password(async_session: AsyncSession, password: str,
                                                   phone_number: str) -> User:
        result = await async_session.execute(
            select(User).where(User.phone_number == phone_number, User.password == password))
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
        # result.rowcount 1:成功 0 失败
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
