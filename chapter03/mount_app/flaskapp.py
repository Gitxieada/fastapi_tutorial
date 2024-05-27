#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title='主应用',description="我是主应用文档的描述",version="v1.0.0")
@app.get('/index',summary='首页')
async def index():
    return JSONResponse({"index": "我是属于主应用的接口！"})

subapp = FastAPI(title='子应用',description="我是子应用文档的描述",version="v1.0.0")
@subapp.get('/index',summary='首页')
async def index():
    return JSONResponse({"index": "我是属于子应用的接口！"})

app.mount(path='/subapp',app=subapp,name='subapp')


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
