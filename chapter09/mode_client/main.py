from fastapi import FastAPI, Depends, status
from typing import Dict
from fastapi.security import OAuth2
from pydantic import BaseModel, ValidationError
from datetime import timedelta
from jose import jwt, JWTError
from datetime import datetime
from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.param_functions import Query
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

app = FastAPI(
    title="oauth2客户端模式",
    description='oauth2客户端模式示例项目演示例子',
    version='v1.1.0',
)

# 阿里云云存储服务商维护的第三方客户端数据表信息
fake_client_db = {
    "xiaozhong": {
        "client_id": "xiaozhong",
        "client_secret": "123456",
    }
}

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


class TokenUtils:

    @staticmethod
    def token_encode(data):
        jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def token_decode(token):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": f"Bearer"},
        )
        try:
            # 开始反向解析我们的TOKEN.,解析相关的信息
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except (JWTError, ValidationError):
            raise credentials_exception
        return payload


class OAuth2ClientCredentialsBearer(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            description: Optional[str] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            clientCredentials={
                "tokenUrl": tokenUrl,
                "scopes": scopes,
            }
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None  # pragma: nocover
        return param


oauth2_scheme = OAuth2ClientCredentialsBearer(tokenUrl="/oauth2/authorize",scheme_name="客户端模式",description="我是描述")


class OAuth2ClientCredentialsRequestForm:

    def __init__(
            self,
            grant_type: str = Query(..., regex="client_credentials"),
            scope: str = Query(""),
            client_id: str = Query(...),
            client_secret: str = Query(...),
            username: Optional[str] = Query(None),
            password: Optional[str] = Query(None),
    ):
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password


@app.post("/oauth2/authorize", summary="请求授权URL地址")
async def authorize(client_data: OAuth2ClientCredentialsRequestForm = Depends()):
    if not client_data:
        raise HTTPException(status_code=400, detail="请输入用户账号及密码等信息")

    if not client_data.client_id and not client_data.client_secret:
        raise HTTPException(status_code=400, detail="请输入分配给第三方APPID及秘钥等信息")

    clientinfo = fake_client_db.get(client_data.client_id)
    if client_data.client_id not in fake_client_db:
        raise HTTPException(status_code=400, detail="非法第三方客户端APPID", headers={"WWW-Authenticate": f"Bearer"})

    if client_data.client_secret != clientinfo.get('client_secret'):
        raise HTTPException(status_code=400, detail="第三方客户端部秘钥不正确!")
    data = {
        'iss ': 'client_id',
        'sub': 'xiaozhongtongxue',
        'client_id': client_data.client_id,
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }
    token = TokenUtils.token_encode(data=data)
    return {"access_token": token, "token_type": "bearer","exires_in":159,"scope":"all"}


# 需要授权才可以
@app.get("/get/clientinfo", summary="请求用户信息地址（受保护资源）")
async def get_clientinfo(token: str = Depends(oauth2_scheme)):
    '''
    定义API接口。改API接口需要token值并校验通过才可以访问
    :param token:
    :return:
    '''
    payload = TokenUtils.token_decode(token=token)
    # 定义认证异常信息
    client_id = payload.get('client_id')
    if client_id not in client_id:
        raise HTTPException(status_code=400, detail="不存在client_id信息", headers={"WWW-Authenticate": f"Bearer"})

    clientinfo = fake_client_db.get(client_id)

    return {'info': {
        'client_id': clientinfo.get('client_id'),
        'client_secret': clientinfo.get('client_secret')
    }}


if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
