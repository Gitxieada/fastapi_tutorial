#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional, Set
from fastapi import FastAPI, Query, Path, Body, Header, Cookie
from pydantic.main import BaseModel
from starlette import status
from enum import Enum

from starlette.responses import Response, JSONResponse, PlainTextResponse, FileResponse
from fastapi import Request

app = FastAPI()


@app.post("/dwonfile1")
def sync_dwonfile():
    return FileResponse(path='./data.bat',filename='data.bat',media_type="application/octet-stream")



@app.post("/dwonfile1")
def sync_dwonfile():
    return FileResponse(path='./data.bat',filename='data.bat',media_type="application/octet-stream")

@app.post("/dwonfile2")
async def async_dwonfile():
    return FileResponse(path='./data.bat',filename='data.bat',media_type="application/octet-stream")

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
