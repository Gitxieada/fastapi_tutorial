import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from chapter15.contextvar_request.request import request_var, request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    token = request_var.set(request)
    try:
        response = await call_next(request)
        return response
    finally:
        request_var.reset(token)




@app.post('/index')
async def index():
    # 这里应该使用事务处理
    print(request.headers)
    return JSONResponse({
        "code": 200,
        "msg": "成功"
    })

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
