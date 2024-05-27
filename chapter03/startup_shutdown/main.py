#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from starlette.background import BackgroundTasks
import time

app = FastAPI()

# 生命周期异步上下文管理器处理程序代替单独的启动和关闭处理程序
@app.on_event("startup")
async def startup_event_async():
    print("服务进程启动成功-async函数")

@app.on_event("startup")
def startup_event_sync():
    print("服务进程启动成功-sync函数")

@app.on_event("shutdown")
async def shutdown_event_async():
    print("服务进程已关闭-async函数")


@app.on_event("shutdown")
def shutdown_event_sync():
    print("服务进程已关闭-sync函数")

if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
