#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from starlette.background import BackgroundTasks
import time
app = FastAPI(routes=None)
import asyncio
def send_mail(n):
    time.sleep(n)

@app.api_route(path="/index", methods=["GET", "POST"])
async def index(tasks: BackgroundTasks):
    tasks.add_task(send_mail, 10)
    print(id(asyncio.get_event_loop()))
    return {"index": "index"}

if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
