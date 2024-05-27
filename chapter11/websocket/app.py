from typing import Any, Dict, List, Optional
from fastapi import Body, FastAPI, HTTPException
from api import room
from api import user


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    pass
    from db.database import async_engine, Base
    from models.model import User
    async def init_create_table():
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    await init_create_table()
    # 实例化房间连接管理类


@app.on_event("shutdown")
async def shutdown_event():
    pass


# 注册路由

app.include_router(user.router_uesr)
app.include_router(room.router_char)


def creat_app():
    return app
