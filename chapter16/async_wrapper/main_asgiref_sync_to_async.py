import cProfile
from functools import wraps

from fastapi import FastAPI,Request

from fastapi.responses import PlainTextResponse,HTMLResponse
from asgiref.sync import sync_to_async
import requests
# 定义我们的APP服务对象
app = FastAPI()

def getdata():
    return requests.get('http://www.baidu.com').text




def async_decorator_with_argument(time_to_eat):
    """async decorator w/ an arg
    We use a closure to capture the argument in the decorator
    Await the returned async function
    """

    def actual_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):




            print(time_to_eat)
            print(args)
            print(kwargs)
            return await func(*args, **kwargs)


        print("输出结果")
        return wrapper

    return actual_decorator

@app.get("/get/access_token")
# @async_decorator_with_argument(time_to_eat='555555')
def access_token(request:Request,dsa:str):
    pr = cProfile.Profile()
    pr.enable()  # 开始收集性能分析数据
    # asds= await sync_to_async(func=getdata)()
    pr.disable()  # 停止收集性能分析数据
    pr.dump_stats(".runtest.prof")  # 把当前性能分析的内容写入一个文件
    return HTMLResponse(getdata())


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1',port=5667, reload=True)


