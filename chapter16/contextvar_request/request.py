from contextvars import ContextVar
from fastapi import Request
from chapter15.contextvar_request.bind_ import bind_contextvar

request_var: ContextVar[Request] = ContextVar("request")
request:Request = bind_contextvar(request_var)