#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional, Set
from fastapi import FastAPI, Query, Path, Body, Header, Cookie
from starlette import status
from enum import Enum

from starlette.responses import Response

app = FastAPI()


@app.get("/set_cookie/")
def setcookie(response: Response):
    response.set_cookie(key="xiaozhong", value="chengxuyuan-xiaozhongtongxue")
    return 'set_cookie ok!'

@app.get("/get_cookie")
async def Cookier_handel(xiaozhong: Optional[str] = Cookie(None)):
    return {
        'xiaozhong':xiaozhong
    }

if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
