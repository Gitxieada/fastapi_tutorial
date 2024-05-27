#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from fastapi import Request
from fastapi import FastAPI, Query, HTTPException
from starlette.responses import JSONResponse

app = FastAPI()



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 故意直接的抛出异常tr

    raise CustomException(message='抛出自定义异常')

    response = await call_next(request)
    return response


class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message


@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    print("触发全局自定义Exception")
    if isinstance(exc,CustomException):
        print("触发全局自定义CustomException")
    return JSONResponse(content={"message": exc.message}, )

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    print("触发全局自定义CustomException")
    return JSONResponse(content={"message": exc.message}, )


@app.get("/custom_exception")
async def read_unicorn(name: str = 'zhong'):

    return {"name": name}


if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
