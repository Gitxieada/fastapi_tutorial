import http

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import RequestResponseEndpoint
app = FastAPI()


class LogMiddleware:

    async def __call__(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
            *args,
            **kwargs
    ):
        try:
            # 下一个响应报文内容
            response = await call_next(request)
        except Exception as ex:
            # 解析响应报文的body异常信息
            response_body = bytes(http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode())
            response = Response(
                content=response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
        else:
            response_body = b''
            # 解析读取对应的响应报文内容型芯
            async for chunk in response.body_iterator:
                response_body += chunk
            # 生成最终响应报文内容
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )

        return response


app.middleware('http')(LogMiddleware())
app.add_middleware(LogMiddleware)

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
