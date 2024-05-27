from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.model import ShortUrl
from db.database import async_engine, Base
from typing import List
from schemas import SingleShortUrlCreate

class ShortServeries:

    @staticmethod
    async def init_create_table():
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def get_short_url(async_session: AsyncSession, short_tag: str)->ShortUrl:
        result = await async_session.execute(select(ShortUrl).where(ShortUrl.short_tag == short_tag))
        return result.scalars().first()

    @staticmethod
    async def create_short_url(async_session: AsyncSession, **kwargs):
        new_short_url = ShortUrl(**kwargs)
        async_session.add(new_short_url)
        await async_session.commit()
        return new_short_url

    @staticmethod
    async def update_short_url(async_session: AsyncSession, short_url_id: int, **kwargs):
        response = update(ShortUrl).where(ShortUrl.id == short_url_id)
        result = await async_session.execute(response.values(**kwargs))
        await async_session.commit()
        return result

    @staticmethod
    async def delete_short_url(async_session: AsyncSession, short_url_id: int):
        response = await async_session.execute(delete(ShortUrl).where(ShortUrl.id == short_url_id))
        await async_session.commit()
        return response


    @staticmethod
    async def create_batch_short_url(async_session: AsyncSession, short_urls:List[SingleShortUrlCreate]):
        short_urls= [ShortUrl(**item.dict()) for item in short_urls]
        async_session.add_all(short_urls)
        await async_session.commit()
        return short_urls