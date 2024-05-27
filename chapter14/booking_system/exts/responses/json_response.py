#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   文件名称 :     json_response
   文件功能描述 :   功能描述
   创建人 :       小钟同学
   创建时间 :          2021/7/15
-------------------------------------------------
   修改描述-2021/7/15:         
-------------------------------------------------
"""

from typing import Any, Dict, Optional
from fastapi.responses import JSONResponse
import time
import json
import datetime
import decimal
import typing
from sqlalchemy.ext.declarative import DeclarativeMeta


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'keys') and hasattr(obj, '__getitem__'):
            return dict(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        elif isinstance(obj.__class__, DeclarativeMeta):
            # 如果是查询返回所有的那种models类型的，需要处理些
            # 将SqlAlchemy结果序列化为JSON--查询全部的时候的处理返回
            return self.default({i.name: getattr(obj, i.name) for i in obj.__table__.columns})
        elif isinstance(obj, dict):
            for k in obj:
                try:
                    if isinstance(obj[k], (datetime.datetime, datetime.date, DeclarativeMeta)):
                        obj[k] = self.default(obj[k])
                    else:
                        obj[k] = obj[k]
                except TypeError:
                    obj[k] = None
            return obj
        return json.JSONEncoder.default(self, obj)


class ApiResponse(JSONResponse):
    # 定义返回响应码--如果不指定的话则默认都是返回200
    http_status_code = 200
    # 默认成功
    api_code = 0
    # 默认Node.如果是必选的，去掉默认值即可
    result: Optional[Dict[str, Any]] = None  # 结果可以是{} 或 []
    message = '成功'
    success = True
    timestamp = int(time.time() * 1000)

    def __init__(self, success=None, http_status_code=None, api_code=None, result=None, message=None, **options):
        self.message = message or self.message
        self.api_code = api_code or self.api_code
        self.success = success or self.success
        self.http_status_code = http_status_code or self.http_status_code
        self.result = result or self.result

        # 返回内容体
        body = dict(
            message=self.message,
            code=self.api_code,
            success=self.success,
            result=self.result,
            timestamp=self.timestamp
        )
        super(ApiResponse, self).__init__(status_code=self.http_status_code, content=body, **options)

    # 这个render会自动调用，如果这里需要特殊的处理的话，可以重写这个地方
    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=CJsonEncoder
        ).encode("utf-8")


class BadrequestException(ApiResponse):
    http_status_code = 400
    api_code = 10031
    result = None  # 结果可以是{} 或 []
    message = '错误的请求'
    success = False


class LimiterResException(ApiResponse):
    http_status_code = 429
    api_code = 429
    result = None  # 结果可以是{} 或 []
    message = '访问的速度过快'
    success = False


class ParameterException(ApiResponse):
    http_status_code = 400
    result = {}
    message = '参数校验错误,请检查提交的参数信息'
    api_code = 10031
    success = False


class UnauthorizedException(ApiResponse):
    http_status_code = 401
    result = {}
    message = '未经许可授权'
    api_code = 10032
    success = False


class ForbiddenException(ApiResponse):
    http_status_code = 403
    result = {}
    message = '失败！当前访问没有权限，或操作的数据没权限!'
    api_code = 10033
    success = False


class NotfoundException(ApiResponse):
    http_status_code = 404
    result = {}
    message = '访问地址不存在'
    api_code = 10034
    success = False


class MethodnotallowedException(ApiResponse):
    http_status_code = 405
    result = {}
    message = '不允许使用此方法提交访问'
    api_code = 10034
    success = False


class OtherException(ApiResponse):
    http_status_code = 800
    result = {}
    message = '未知的其他HTTPEOOER异常'
    api_code = 10034
    success = False


class InternalErrorException(ApiResponse):
    http_status_code = 200
    result = {}
    message = '程序员哥哥睡眠不足，系统崩溃了！'
    api_code = 200
    success = False


class InvalidTokenException(ApiResponse):
    http_status_code = 401
    api_code = 401
    message = '很久没操作，令牌失效'
    success = False


class ExpiredTokenException(ApiResponse):
    http_status_code = 422
    message = '很久没操作，令牌过期'
    api_code = 10050
    success = False


class FileTooLargeException(ApiResponse):
    http_status_code = 413
    api_code = 413
    result = None  # 结果可以是{} 或 []
    message = '文件体积过大'


class FileTooManyException(ApiResponse):
    http_status_code = 413
    message = '文件数量过多'
    api_code = 10120
    result = None  # 结果可以是{} 或 []


class FileExtensionException(ApiResponse):
    http_status_code = 401
    message = '文件扩展名不符合规范'
    api_code = 10121
    result = None  # 结果可以是{} 或 []


class Success(ApiResponse):
    http_status_code = 200
    api_code = 200
    result = None  # 结果可以是{} 或 []
    message = '获取成功'
    success = True



class Businesserror(ApiResponse):
    http_status_code = 200
    api_code = '0000'
    result = None  # 结果可以是{} 或 []
    message = '业务错误逻辑处理'
    success = False


class Fail(ApiResponse):
    http_status_code = 200
    api_code = -1
    result = None  # 结果可以是{} 或 []
    message = '操作失败'
    success = False
