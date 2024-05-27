#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional, Set
from fastapi import FastAPI, Query, Path, Body, Header, Cookie
from starlette import status
from enum import Enum

from starlette.responses import Response
from fastapi import Request

app = FastAPI()


@app.get("/get_request/")
async def get_request(request: Request):
    form_data= await request.form()
    body_data = await request.body()
    return {
        'url':request.url,
        'base_url': request.base_url,
        'client_host ': request.client.host,
        'query_params': request.query_params,
        'json_data':await request.json() if body_data else None,
        'form_data':form_data,
        'body_data': body_data,
    }

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
