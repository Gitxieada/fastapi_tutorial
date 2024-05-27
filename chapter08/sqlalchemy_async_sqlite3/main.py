from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_session
from sqlalchemy.orm import declarative_base, sessionmaker

# URL地址格式
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///aiosqlite_user.db"
# 创建异步引擎对象
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# 定义数据库模型
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# 定义业务逻辑表
from sqlalchemy import Column, Integer, String


class User(Base):
    # 指定本类映射到users表
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    nikename = Column(String(32))
    password = Column(String(32))
    email = Column(String(50))


async def init_create():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


import asyncio

asyncio.run(init_create())

# 创建异步会话查询
SessionLocal = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

# 对模型类进行异步CRUD操作
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(async_session: AsyncSession, user_id: int):
    result = await async_session.execute(
        select(User)
            .where(User.id == user_id)
    )
    return result.scalars().first()


async def get_user_by_name(async_session: AsyncSession, name: str):
    result = await async_session.execute(
        select(User)
            .where(User.name == name)
    )
    return result.scalars().first()


async def get_users(async_session: AsyncSession, skip: int = 0, limit: int = 100):
    result = await async_session.execute(select(User).order_by(User.id))
    return result.scalars().fetchall()


async def create_user(async_session: AsyncSession, name, nikename, email, password):
    new_user = User(
        name=name,
        email=email,
        password=password,
        nikename=nikename,
    )
    async_session.add(new_user)
    await async_session.commit()
    return new_user


import asyncio


async def testrun():
    async_session = SessionLocal()
    result = await create_user(async_session=async_session, name='xiaozhong', nikename='Zyx', email='zyx@123.com',
                               password='123456')
    print(result.name)
    await async_session.close()
    async_session = SessionLocal()
    result = await get_user_by_name(async_session=async_session, name='xiaozhong')
    print(result.name)
    await async_session.close()
    async_session = SessionLocal()
    result = await get_users(async_session=async_session)
    print(result)
    for item in result:
        print(item)
    await async_session.close()


asyncio.run(testrun())

#=============================================================
#=============================================================
#=============================================================
#=============================================================

from contextlib import asynccontextmanager
@asynccontextmanager
async def get_db() -> AsyncGenerator:
    async_session = SessionLocal()
    try:
        yield async_session
        await async_session.commit()
    except SQLAlchemyError as ex:
        await async_session.rollback()
        raise ex
    finally:
        await async_session.close()


async def testrun():
    async with get_db() as async_session:
        result = await create_user(async_session=async_session, name='xiaozhong', nikename='Zyx', email='zyx@123.com',password='123456')
        print(result.name)
        result = await get_user_by_name(async_session=async_session, name='xiaozhong')
        print(result.name)

asyncio.run(testrun())