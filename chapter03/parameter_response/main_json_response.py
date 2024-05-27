#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional, Set
from fastapi import FastAPI, Query, Path, Body, Header, Cookie
from starlette import status
from enum import Enum

from starlette.responses import Response, JSONResponse
from fastapi import Request

app = FastAPI()



@app.post("/api/v1/json1/")
async def index():
    # 默认返回类型就是JSONResponse
    return {"code": 0, "msg": "ok", "data": None}

@app.post("/api/v1/json2/")
async def index():
    return JSONResponse(status_code=404, content={"code": 0, "msg": "ok", "data": None})

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
