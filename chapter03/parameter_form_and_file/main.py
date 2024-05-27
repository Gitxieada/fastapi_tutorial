#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional, Set

import aiofiles
from fastapi import FastAPI, Query, Path, Body, Form, File, UploadFile
from pydantic.main import BaseModel
from starlette import status
from enum import Enum
from fastapi import Depends

app = FastAPI()




@app.post("/demo/login/")
async def login(username: str = Form(...,title="用户名",description="用户名字段描述", max_length=5),
                 password: str = Form(...,title="用户密码",description="用户密码字段描述", max_length=20)):
    return {"username": username, "password": password}


@app.post("/sync_file",summary='File形式的-单文件上传')
def sync_file(file: bytes = File(...)):
    '''
    基于使用File类 文件内容会以bytes的形式读入内存通常主要用于上传小的文件
    :param file:
    :return:
    '''
    with open('./data.bat', 'wb') as f:
        f.write(file)
    return {'file_size': len(file)}

@app.post("/async_file",summary='File形式的-单文件上传')
async def async_file(file: bytes = File(...)):
    '''
    基于使用File类 使用异步的方式进行文件接收处理
    :param file:
    :return:
    '''
    # 异步方式执行with操作,修改为 async with
    async with aiofiles.open("./data.bat", "wb") as fp:
        await fp.write(file)
    return {'file_size': len(file)}


# 多文件的上传
@app.post("/sync_file2",summary='File列表形式的-多文件上传')
def sync_file2(files: List[bytes] = File(...)):
    '''
    基于使用File类 运行多文件上传处理
    :param files:
    :return:
    '''
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles",summary='UploadFile形式的-单文件上传')
async def uploadfiles(file: UploadFile = File(...)):
    result = {
        "filename": file.filename,
        "content-type": file.content_type,
    }
    content = await file.read()
    with open(f"./{file.filename}", 'wb') as f:
        f.write(content)
    return result

if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
