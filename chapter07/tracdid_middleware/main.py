from fastapi import FastAPI, Request
import time

from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


import uuid
# 基于BaseHTTPMiddleware的中间件实例
import contextvars
request_context = contextvars.ContextVar('request_context')

class TracdIDMiddleware(BaseHTTPMiddleware):
    # dispatch 必须实现
    async def dispatch(self, request:Request, call_next):
        request_context.set(request)
        request.state.traceid = uuid.uuid4()
        responser = await call_next(request)
        # 返回接口响应时间
        return responser

def log_info(mage=None):
    request: Request =request_context.get()
    print('index-requet',request.state.traceid)

app.add_middleware(TracdIDMiddleware)

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
