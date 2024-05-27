#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
import threading
import time
import asyncio
app = FastAPI(routes=None)

@app.get(path="/async")
async def asyncdef():
    await asyncio.sleep(10)
    print("当前协程运行的线程ID:", threading.current_thread().ident)
    return {"index": "async"}

@app.get(path="/sync")
def syncdef():
    time.sleep(10)
    print("当前普通函数运行的线程ID:",threading.current_thread().ident)
    return {"index": "sync"}




if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
