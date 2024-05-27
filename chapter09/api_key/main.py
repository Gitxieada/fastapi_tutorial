from fastapi import Depends
from fastapi import FastAPI, Request
from fastapi.security import APIKeyCookie,APIKeyHeader,APIKeyQuery
from fastapi.params import Security
from typing import Optional
from fastapi.exceptions import HTTPException
from starlette import status
from fastapi.responses import PlainTextResponse

app = FastAPI(
    title="基于apikey的特定的密钥的方案",
    description='基于apikey的特定的密钥的方案项目演示例子',
    version='v1.1.0',
)

class APIKey():

    # APIKeyHeader的鉴权方式
    API_KEY_HEADER = "XTOKEN"
    API_KEY_HEADER_NAME = "X-TOKEN"
    api_key_header_token = APIKeyHeader(name=API_KEY_HEADER_NAME, scheme_name="API key header",auto_error=True)

    API_KEY_QUERY = "XQUERY"
    API_KEY_QUERY_NAME = "X-QUERY"
    api_key_query_token = APIKeyQuery(name=API_KEY_HEADER_NAME, scheme_name="API key query", auto_error=True)

    API_KEY_Cookie = "XCOOKIE"
    API_KEY_COOKIE_NAME = "X-COOKIE"
    api_key_cookie_token = APIKeyCookie(name=API_KEY_COOKIE_NAME, scheme_name="API key cookie", auto_error=False)

    async def __call__(self, request: Request,
                       api_key_header: str = Security(api_key_header_token),
                       api_key_query: str = Security(api_key_query_token),
                       api_key_cookie: str = Security(api_key_cookie_token),
                       ) -> Optional[bool]:
        if api_key_header != self.API_KEY_HEADER:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="APIKeyHeader的鉴权方式认证失败！"
            )
        if api_key_query != self.API_KEY_QUERY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="APIKeyQuery的鉴权方式认证失败！"
            )
        if not api_key_cookie:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="APIKeyCookie中的cookie没有值！"
            )
        if api_key_cookie != self.API_KEY_Cookie:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="APIKeyCookie的鉴权方式认证失败！"
            )

        return True

apikeiauth = APIKey()

@app.get("/apikey")
async def digest(request: Request, auth: bool = Depends(apikeiauth)):
    # print(credentials)
    if auth:
        return PlainTextResponse('登入成功')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, debug=True, reload=True)