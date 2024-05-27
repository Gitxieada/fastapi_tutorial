#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional
from fastapi import FastAPI, Query, Path
from starlette import status
from enum import Enum

app = FastAPI()


@app.get("/query/")
async def callback(user_id: int, user_name: Optional[str] = None, user_token: str = 'token'):
    return {
        'user_id': user_id,
        'user_name': user_name,
        'user_token': user_token
    }

@app.get("/query/bool/")
async def callback(isbool: bool = False):
    return {
        'isbool': isbool
    }

@app.get("/query/morequery")
async def callback(
        user_id: int = Query(..., ge=10, le=100),
        user_name: str = Query(None, min_length=1, max_length=50, regex="^fixedquery$"),
        user_token: str = Query(default='token', min_length=1, max_length=50),
):
    return {
        'user_id': user_id,
        'user_name': user_name,
        'user_token': user_token
    }

@app.get("/query/list/")
async def query_list(q: List[str] = Query(["test1", "test2"])):
    return {
        'q': q
    }

if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
