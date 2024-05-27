import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request

app = FastAPI()


# 基于BaseHTTPMiddleware的中间件实例，
class TimeCcalculateMiddleware(BaseHTTPMiddleware):
    # dispatch 必须实现
    async def dispatch(self, request: Request, call_next):
        print('TimeCcalculateMiddleware-Start')
        start_time = time.time()
        response = await call_next(request)
        process_time = round(time.time() - start_time, 4)
        # 返回接口响应时间
        response.headers["X-Process-Time"] = f"{process_time} (s)"
        print('TimeCcalculateMiddleware-End')
        return response


# 基于BaseHTTPMiddleware的中间件实例，
class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_value='auth'):
        super().__init__(app)
        self.header_value = header_value

        # dispatch 必须实现
        async def dispatch(self, request: Request, call_next):
            print('AuthMiddleware-Start')
            response = await call_next(request)
            response.headers['Custom'] = self.header_value
            print('AuthMiddleware-End')
            return response


app.add_middleware(TimeCcalculateMiddleware)
app.add_middleware(AuthMiddleware, header_value='CustomAuth')


@app.get("/index")
async def index():
    print('index-Start')
    return {
        'code': 200
    }
if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
