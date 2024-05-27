#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from starlette.responses import JSONResponse

async def exception_not_found(request, exc):
    return JSONResponse({
        "code": exc.status_code,
        "error": "没有定义这个请求地址"},
        status_code=exc.status_code)

exception_handlers = {
    404: exception_not_found,
}

app = FastAPI(exception_handlers=exception_handlers)


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
