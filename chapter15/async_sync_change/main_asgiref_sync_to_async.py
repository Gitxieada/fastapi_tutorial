from functools import wraps

from fastapi import FastAPI,Request

from fastapi.responses import PlainTextResponse,HTMLResponse
from asgiref.sync import sync_to_async
import requests
# 定义我们的APP服务对象
app = FastAPI()

def getdata():
    return requests.get('http://www.baidu.com').text




@app.get("/get/access_token")
async def access_token():
    asds= await sync_to_async(func=getdata)()
    return HTMLResponse(asds)


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)


