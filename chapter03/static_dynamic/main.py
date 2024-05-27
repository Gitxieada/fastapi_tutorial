#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi import APIRouter
from starlette.responses import JSONResponse

app = FastAPI(routes=None)


# ============一个URL配置多个HTTP请求方法==========
# =========================================
@app.api_route(path="/index", methods=["GET", "POST"])
async def index():
    return {"index": "index"}


async def index2():
    return JSONResponse({"index": "index"})


app.add_api_route(path="/index2", endpoint=index2, methods=["GET", "POST"])

router_uesr = APIRouter(prefix="/user", tags=["用户模块"])


@router_uesr.get("/user/login")
def user_login():
    return {"ok": "登入成功！"}


@router_uesr.api_route("/user/api/login", methods=['GET', 'POST'])
def user_api_route_login():
    return {"ok": "登入成功！"}


def add_user_api_route_login():
    return {"ok": "登入成功！"}


router_uesr.add_api_route("/user/add/api/login", methods=['GET', 'POST'], endpoint=add_user_api_route_login)
app.include_router(router_uesr)

if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
