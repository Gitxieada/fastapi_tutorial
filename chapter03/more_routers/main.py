#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI()

# ============多重URL地址绑定函数============
# =========================================
@app.get('/', response_class=JSONResponse)
@app.get('/index', response_class=JSONResponse)
@app.post('/index', response_class=JSONResponse)
@app.get("/app/hello", tags=['app实例对象注册接口-示例'])
def app_hello():
    return {"Hello": "app api"}

# ============同一个URL动态和静态路由==========
# =========================================
# 动态路由
@app.get('/user/{userid}')
async def login(userid: str):
    return {"Hello": "dynamic"}


# 静态路由
@app.get('/user/userid')
async def login():
    return {"Hello": "static"}




if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
