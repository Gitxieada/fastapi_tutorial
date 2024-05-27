import uvicorn
from typing import Optional
from fastapi import FastAPI
from fastapi import Security
from enum import Enum
from typing import Any, Callable, Dict, Optional, Sequence
from fastapi.params import Depends
from fastapi.security import SecurityScopes
from pydantic.fields import FieldInfo, Undefined
from fastapi.security import SecurityScopes
from fastapi import Security
from fastapi import Depends
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import PlainTextResponse

app = FastAPI()


class LogerMiddleware(BaseHTTPMiddleware):

    async def set_body(self, request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive

    async def dispatch(self, request: Request, call_next):
        await self.set_body(request)
        # 需要在日志中间件里读取body数据
        _body = await request.body()
        print("Loger中间件解析读取11111111：消费request.body()",_body)
        response = await call_next(request)
        return response



class LogerMiddleware2(BaseHTTPMiddleware):

    async def set_body(self, request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive

    async def dispatch(self, request: Request, call_next):
        await self.set_body(request)
        # 需要在日志中间件里读取body数据
        _body = await request.body()
        print("Loger中间件解析读取22222222：消费request.body()",_body)
        response = await call_next(request)
        return response

app.add_middleware(LogerMiddleware)
app.add_middleware(LogerMiddleware2)


@app.get("/")
async def index(request: Request):
    _body = await request.body()
    print("路由函数内容部读取：", _body)
    return PlainTextResponse("消费request.body()！")




if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
