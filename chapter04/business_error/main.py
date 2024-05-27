#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from fastapi import Request
from fastapi import FastAPI, Query, HTTPException
from starlette.responses import JSONResponse

app = FastAPI()


from enum import Enum
class ExceptionEnum(Enum):
    SUCCESS = ("0000", "OK")
    FAILED = ("9999", "系统异常")
    USER_NO_DATA = ("10001", "用户不存在")
    USER_REGIESTER_ERROR = ("10002", "注册异常")
    PERMISSIONS_ERROR = ("2000", "用户权限错误")

class BusinessError(Exception):
    __slots__ = ['err_code', 'err_code_des']
    def __init__(self,  result: ExceptionEnum = None, err_code: str = "00000", err_code_des: str = ""):
        if result:
            self.err_code = result.value[0]
            self.err_code_des = err_code_des or result.value[1]
        else:
            self.err_code = err_code
            self.err_code_des = err_code_des
        super().__init__(self)

@app.exception_handler(BusinessError)
async def custom_exception_handler(request: Request, exc: BusinessError):
    return JSONResponse(content={
        'return_code':'FAIL',
        'return_msg':'参数错误',
        'err_code': exc.err_code,
        'err_code_des': exc.err_code_des,
    })


@app.get("/custom_exception")
async def custom_exception(name: str = 'zhong'):
    if name == "xiaozhong":
        raise BusinessError(ExceptionEnum.USER_NO_DATA)
    return {"name": name}


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
