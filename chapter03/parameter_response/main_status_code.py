#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional, Set
from fastapi import FastAPI, Query, Path, Body, Header, Cookie
from starlette import status
from enum import Enum

from starlette.responses import Response, JSONResponse
from fastapi import Request

app = FastAPI()


@app.get("/set_http_code/demo1/", status_code=500)
async def set_http_code():
    return {
        'message': 'ok',
    }

@app.get("/set_http_code/demo2/", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
async def set_http_code():
    return {
        'message': 'ok',
    }

@app.get("/set_http_code/demo3/")
async def set_http_code(response: Response):
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {
        'message': 'ok',
    }

@app.get("/set_http_code/demo4/")
async def set_http_code():
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
        'message': 'ok',
    })

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
