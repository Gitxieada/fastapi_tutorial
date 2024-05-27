#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional, Set
from fastapi import FastAPI, Query, Path, Body, Header, Cookie
from starlette import status
from enum import Enum

from starlette.responses import Response
from fastapi import Request

app = FastAPI()

@app.get("/xml/")
def get_xml_data():
    data = """<?xml version="1.0" ?> 
    <note>
    <to>George</to> 
    <from>John</Ffrom> 
    <heading>Reminder</heading> 
    <body>Don't forget the meeting!</body> 
    </note>
    """
    return Response(content=data, media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
