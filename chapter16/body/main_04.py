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
from starlette.types import ASGIApp, Scope, Receive, Send

app = FastAPI()


class LogerMiddleware1:
    def __init__(
            self,
            app: ASGIApp,

    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # pragma: no cover
            await self.app(scope, receive, send)
            return
        receive_ = await receive()

        async def receive():
            return receive_

        # 创建需要解析的参数
        request = Request(scope, receive)
        _body = await request.body()
        print("Loger中间件解析读取：消费request.body()", _body)

        await self.app(scope, receive, send)


class LogerMiddleware2:
    def __init__(
            self,
            app: ASGIApp,

    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # pragma: no cover
            await self.app(scope, receive, send)
            return
        # 接收一次
        receive_ = await receive()
        async def receive():
            return receive_

        # 创建需要解析的参数
        request = Request(scope, receive)
        _body = await request.body()
        print("Loger中间件解析读取：消费request.body()", _body)

        await self.app(scope, receive, send)


app.add_middleware(LogerMiddleware1)
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
