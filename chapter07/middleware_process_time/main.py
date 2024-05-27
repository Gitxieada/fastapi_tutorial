from fastapi import FastAPI, Request
import time

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 定义请求处理时间
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # 添加响应头
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/index")
async def index():
    return {
        'code': 200
    }


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
