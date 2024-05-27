from fastapi import FastAPI,Request
from fastapi.responses import PlainTextResponse,HTMLResponse
from asyncer import asyncify
import requests
# 定义我们的APP服务对象
app = FastAPI()

def do_sync_work(name):
    return requests.get(f'http://www.baidu.com?name={name}').text

@app.get("/get/access_token")
async def access_token(request:Request):
    message = await asyncify(do_sync_work)(name="World")
    return HTMLResponse(message)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8100, debug=True, reload=True)
