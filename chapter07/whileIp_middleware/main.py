from fastapi import FastAPI, Request
import time

from starlette.middleware.base import BaseHTTPMiddleware

from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import HTTPConnection
import typing

app = FastAPI()


class WhileIpMiddleware:
    def __init__(self, app: ASGIApp,
                 allow_ip: typing.Sequence[str] = (),
                 ) -> None:
        self.app = app
        self.allow_ip = allow_ip or "*"

        async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
            if scope["type"] in ("http", "websocket") and scope["scheme"] in ("http", "ws"):
                conn = HTTPConnection(scope=scope)
                if self.allow_ip and conn.client.host not in self.allow_ip:
                    response = PlainTextResponse(content="不在IP白名单内", status_code=403)
                    await response(scope, receive, send)
                    return
                await self.app(scope, receive, send)
            else:
                await self.app(scope, receive, send)


app.add_middleware(WhileIpMiddleware, allow_ip=['127.0.0.2'])


@app.get("/index")
async def index():
    return {
        'code': 200
    }


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
