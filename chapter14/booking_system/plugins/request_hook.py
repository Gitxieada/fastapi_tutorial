
from plugins.base import PluginBase
from fastapi import FastAPI
from pydantic import BaseSettings
from fastapi.middleware.cors import CORSMiddleware
import typing
import asyncio
from fastapi import BackgroundTasks


class HookPluginClient(PluginBase):
    # 设置插件默认的参数信息
    def __init__(self,
                 on_before_request: typing.Sequence[typing.Callable] = None,
                 on_after_request: typing.Sequence[typing.Callable] = None,
                 on_teardown_appcontext: typing.Sequence[typing.Callable] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_before_request = [] if on_before_request is None else list(on_before_request)
        self.on_after_request = [] if on_after_request is None else list(on_after_request)
        self.on_teardown_appcontext = [] if on_teardown_appcontext is None else list(on_teardown_appcontext)

    def init_app(self, app: FastAPI, *args, **kwargs):
        pass

        @app.middleware("http")
        async def event_request(request, call_next):
            response = None
            try:
                await self.before_request(request)
                response = await call_next(request)
                await self.after_request(request, response)
                return response
            finally:
                pass
                await self.teardown_appcontext(request, response)

        return self

    def add_event_handler(self, event_type: str, func: typing.Callable) -> None:
        assert event_type in ("before_request", "after_request", "teardown_appcontext")
        if event_type == "before_request":
            self.on_before_request.append(func)
        elif event_type == "after_request":
            self.on_after_request.append(func)
        else:
            self.on_teardown_appcontext.append(func)

    def on_event(self, event_type: str) -> typing.Callable:
        def decorator(func: typing.Callable) -> typing.Callable:
            self.add_event_handler(event_type, func)
            return func
        return decorator

    async def before_request(self, request) -> None:

        for handler in self.on_before_request:
            if asyncio.iscoroutinefunction(handler):
                await handler(request)
            else:
                handler(request)

    async def after_request(self, request, response) -> None:
        for handler in self.on_after_request:
            if asyncio.iscoroutinefunction(handler):
                await handler(request, response)
            else:
                handler(request, response)

    async def teardown_appcontext(self, request, response) -> None:
        for handler in self.on_teardown_appcontext:
            if asyncio.iscoroutinefunction(handler):
                await handler(request, response)
            else:
                handler(request, response)