#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional, Set
from fastapi import FastAPI, Query, Path, Body, Header, Cookie
from pydantic.main import BaseModel
from starlette import status
from enum import Enum

from starlette.responses import Response, JSONResponse
from fastapi import Request

app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: str = None


class UserOut(BaseModel):
    username: str
    email: str
    full_name: str = None


@app.post("/user/", response_model=UserOut)
async def create_user(*, user: UserIn):
    return user
@app.post("/user/", response_model=UserOut)
async def create_user(*, user: UserIn):
    return user


if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
