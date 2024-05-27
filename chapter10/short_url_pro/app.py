from fastapi import FastAPI
from api.short import router_short
from api.user import router_uesr
app = FastAPI(title='fastapi集成短链实战案例')

@app.on_event("startup")
async def startup_event():
    pass
    from db.database import async_engine, Base
    from models.model import User,ShortUrl
    async def init_create_table():
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    await init_create_table()

@app.on_event("shutdown")
async def shutdown_event():
    pass

from api.short import router_short
from api.user import router_uesr
app.include_router(router_short)
app.include_router(router_uesr)

print('启动！')
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='app:app', host="127.0.0.1", port=8000, reload=True)