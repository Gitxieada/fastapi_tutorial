#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional, Set
from fastapi import FastAPI, Query, Path, Body, Header, Cookie
from starlette import status
from enum import Enum

from starlette.responses import Response, JSONResponse
from fastapi import Request

app = FastAPI()


from fastapi.responses import HTMLResponse

def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Fastapi框架学习</title>
        </head>
        <body>
            <h1>欢迎学习Fastapi框架！</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/", response_class=HTMLResponse)
async def index():
    return generate_html_response()

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
