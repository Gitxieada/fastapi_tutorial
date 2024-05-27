# 导入异步引擎的模块
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from contextlib import asynccontextmanager
from sqlalchemy import MetaData
from sqlalchemy.engine.url import URL
# URL地址格式
from config.config import get_settings

# 创建异步引擎对象
settings = get_settings()
async_engine = create_async_engine(url=URL.create(settings.ASYNC_DB_DRIVER,
                                                  settings.DB_USER,
                                                  settings.DB_PASSWORD,
                                                  settings.DB_HOST,
                                                  settings.DB_PORT,
                                                  settings.DB_DATABASE),
                                   echo=settings.DB_ECHO,
                                   pool_size=settings.DB_POOL_SIZE,
                                   max_overflow=settings.DB_MAX_OVERFLOW,
                                   future=True)

metadata = MetaData()
# 创建ORM模型基类
Base = declarative_base(metadata=metadata)
# 创建异步的会话管理对象
AsyncSessionLocal = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession,autocommit=False,autoflush=False, future=False)


async def depends_get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db_session = None
    try:
        db_session = AsyncSessionLocal()
        print("获取会话！！！！")
        yield db_session
        await db_session.commit()
    except SQLAlchemyError as ex:
        await db_session.rollback()
        raise ex
    finally:
        await db_session.close()


# 需要使用这个来装饰一下，才可以使用with
@asynccontextmanager
async def async_context_get_db() -> AsyncGenerator:
    '''
        async def init() -> None:
        pass
        async with get_db() as session:
            result = await session.execute(select(Hospital))
            listsd = result.scalars().fetchall()
            print([itm.name for itm in listsd])
            # import asyncio
            # # asyncio.run(init())
            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(init())
    :return:
    '''
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except SQLAlchemyError as ex:
        await session.rollback()
        raise ex
    finally:
        await session.close()
