# 创建引擎对象
from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import  SQLModel, Field
from sqlalchemy.orm import declarative_base, sessionmaker

ASYNC_DATABASE_URI = "sqlite+aiosqlite:///aiosqlite_user.db"
async_engine = create_async_engine(ASYNC_DATABASE_URI)
class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name:str
    nikename:str
    password :str
    email:str

async def init_create():
    async with async_engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)




import asyncio
asyncio.run(init_create())



from sqlmodel.ext.asyncio.session import AsyncSession
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession, expire_on_commit=False)

from sqlmodel import select,update,delete
# 创建用户
async def create():
    async with SessionLocal() as async_session:
        pass
        db_obj = Users(name='xiaozhong',nikename='zyx',password='123456',email='zyx@123.com')
        async_session.add(db_obj)
        await async_session.commit()
        await async_session.refresh(db_obj)
        return db_obj

# 获取用户记录信息
async def get_user(user_id: int):
    async with SessionLocal() as async_session:
        response = await async_session.exec(select(Users).where(Users.id == user_id))
        return response.first()

# 批量获取多条用户记录信息
async def get_user_multi(name: str):
    async with SessionLocal() as async_session:
        response = await async_session.exec(select(Users).where(Users.name == name))
        return response.all()

# 批量用户更新
async def update_user(name:str):
    async with SessionLocal() as async_session:
        pass
        updateusers = update(Users).where(Users.name == name)
        results = await async_session.exec(updateusers.values(email='xiaozhong@qw.com'))
        await async_session.commit()

# 单独删除记录
async def remove(user_id:int):
    async with SessionLocal() as async_session:
        pass
        response = await async_session.exec(select(Users).where(Users.id == id))
        obj = response.one()
        await async_session.delete(obj)
        await async_session.commit()
        return obj

# 批量删除
async def removeall(name:str):
    async with SessionLocal() as async_session:
        pass
        response = await async_session.exec(delete(Users).where(Users.name == name))
        await async_session.commit()



import asyncio
asyncio.run(create())
asyncio.run(update_user(name='xiaozhong'))
asyncio.run(get_user(user_id=1))
asyncio.run(get_user_multi(name='xiaozhong'))
asyncio.run(removeall(name='xiaozhong'))