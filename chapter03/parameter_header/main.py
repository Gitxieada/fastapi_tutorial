#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional, Set
from fastapi import FastAPI, Query, Path, Body, Header
from starlette import status
from enum import Enum

app = FastAPI()


@app.get("/demo/header/")
async def read_items(user_agent: Optional[str] = Header(None,convert_underscores=True),
                     accept_encoding: Optional[str] = Header(None,convert_underscores=True),
                     accept: Optional[str] = Header(None),
                     accept_token: Optional[str] = Header(...,convert_underscores=False),
                     ):
    return {
        "user_agent": user_agent,
        "accept_encoding": accept_encoding,
        "accept": accept,
        "token": accept_token,

    }

@app.get("/headerlist/")
async def read_headerlist(x_token: List[str] = Header(None)):
    return {"X-Token values": x_token}

if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
