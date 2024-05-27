from typing import Any, Dict, List, Optional
from fastapi import Body, FastAPI, HTTPException
from starlette.responses import FileResponse
from api import room
from api import user
from utils.room_connection_helper_distributed import RoomConnectionManager

app = FastAPI()  # pylint: disable=invalid-name

import asyncio


@app.on_event("startup")
async def startup_event():
    pass
    from db.database import async_engine, Base
    async def init_create_table():
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    await init_create_table()
    # 实例化房间连接管理类
    app.state.room_connection = RoomConnectionManager()
    # 创建发布定义示例对象
    await app.state.room_connection.register_pubsub()
    # 开始订阅相关的频道消息
    await app.state.room_connection.do_listacton()

 


@app.on_event("shutdown")
async def shutdown_event():
    pass


# 注册路由

app.include_router(user.router_uesr)
app.include_router(room.router_char)




def creat_app():
    return app
