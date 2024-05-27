#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   文件名称 :     __init__.py
   文件功能描述 :   功能描述
   创建人 :       小钟同学
   创建时间 :          2021/7/15
-------------------------------------------------
   修改描述-2021/7/15:
-------------------------------------------------
"""

from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from exts.responses.json_response import InternalErrorException, \
    MethodnotallowedException, \
    NotfoundException, LimiterResException, BadrequestException, ParameterException, Businesserror

from enum import Enum


class ExceptionEnum(Enum):
    SUCCESS = ("0000", "OK")
    # 参数异常信息错误
    PARAMETER_ERROR = ("10001", "参数处理异常错误")
    FAILED = ("5000", "系统异常")
    USER_NO_DATA = ("10001", "用户不存在")
    USER_REGIESTER_ERROR = ("10002", "注册异常")
    PERMISSIONS_ERROR = ("2000", "用户权限错误")


class BusinessError(Exception):
    __slots__ = ['err_code', 'err_code_des']

    def __init__(self, result: ExceptionEnum = None, err_code: str = "0000", err_code_des: str = ""):
        if result:
            self.err_code = result.value[0]
            self.err_code_des = err_code_des or result.value[1]
        else:
            self.err_code = err_code
            self.err_code_des = err_code_des
        super().__init__(self)


class ApiExceptionHandler:
    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if app is not None:
            self.init_app(app)

    def init_app(self, app: FastAPI):
        app.add_exception_handler(Exception, handler=self.all_exception_handler)
        app.add_exception_handler(StarletteHTTPException, handler=self.http_exception_handler)
        app.add_exception_handler(BusinessError, handler=self.all_businesserror_handler)
        app.add_exception_handler(RequestValidationError, handler=self.validation_exception_handler)

    async def validation_exception_handler(self, request: Request, exc: RequestValidationError):
        return ParameterException(http_status_code=400, api_code=400, message='参数校验错误', result={
            "detail": exc.errors(),
            "body": exc.body
        })

    async def all_businesserror_handler(self, request: Request, exc: BusinessError):
        return Businesserror(http_status_code=200, api_code=exc.err_code, message=exc.err_code_des)

    async def all_exception_handler(self, request: Request, exc: Exception):

        return InternalErrorException()

    async def http_exception_handler(self, request: Request, exc: StarletteHTTPException):
        if exc.status_code == 405:
            return MethodnotallowedException()
        if exc.status_code == 404:
            return NotfoundException()
        elif exc.status_code == 429:
            return LimiterResException()
        elif exc.status_code == 500:
            return InternalErrorException()
        elif exc.status_code == 400:
            return BadrequestException(msg=exc.detail)
