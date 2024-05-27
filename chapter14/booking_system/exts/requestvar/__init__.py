from contextvars import ContextVar
from fastapi import Request
import shortuuid
from exts.requestvar.bing import bind_contextvar
from starlette.types import ASGIApp, Receive, Scope, Send
request_var: ContextVar[Request] = ContextVar("request")
request: Request = bind_contextvar(request_var)

class BindContextvarMiddleware:
    def __init__(
            self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request = Request(scope, receive=receive)
        request.state.trace_links_index = 0
        request.state.traceid = shortuuid.uuid()
        token = request_var.set(request)
        try:
            response = await self.app(scope, receive, send)
            return response
        finally:
            request.state.trace_links_index = 0
            request_var.reset(token)


__all__ = ("request_var", "request", "BindContextvarMiddleware")
