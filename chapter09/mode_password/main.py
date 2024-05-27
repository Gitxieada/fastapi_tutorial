from fastapi import FastAPI, Request, Depends, HTTPException, Security, status
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from datetime import timedelta
from jose import jwt
from datetime import datetime

app = FastAPI(
    title="oauth2密码模式",
    description='oauth2密码模式示例项目演示例子',
    version='v1.1.0',
)

# 微信资源服务器上用户数据表信息
fake_users_db = {
    "xiaozhong": {
        "username": "xiaozhong",
        "full_name": "xiaozhong tongxue",
        "email": "xiaozhong@example.com",
        "password": "123456",
        "disabled": False,
    },
}

# 微信第三方客户端数据表信息
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/connect/oauth2/authorize")


@app.post("/connect/oauth2/authorize", summary="请求授权URL地址")
async def login(user_form_data: OAuth2PasswordRequestForm = Depends()):
    if not user_form_data:
        raise HTTPException(status_code=400, detail="请输入用户账号及密码等信息")

    if not user_form_data.client_id and not user_form_data.client_secret:
        raise HTTPException(status_code=400, detail="请输入分配给第三方APPID及秘钥等信息")

    userinfo = fake_users_db.get(user_form_data.username)
    if user_form_data.username not in fake_users_db:
        raise HTTPException(status_code=400, detail="不存在此用户信息", headers={"WWW-Authenticate": f"Bearer"})

    if user_form_data.password != userinfo.get('password'):
        raise HTTPException(status_code=400, detail="用户密码不对")

    clientinfo = fake_client_db.get(user_form_data.client_id)
    if user_form_data.client_id not in fake_client_db:
        raise HTTPException(status_code=400, detail="非法第三方客户端APPID", headers={"WWW-Authenticate": f"Bearer"})

    if user_form_data.client_secret != clientinfo.get('client_secret'):
        raise HTTPException(status_code=400, detail="第三方客户端部秘钥不正确!")

    data = {
        'iss ': user_form_data.username,
        'sub': 'xiaozhongtongxue',
        'username': user_form_data.username,
        'admin': True,
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }

    token = TokenUtils.token_encode(data=data)

    return {"access_token": token, "token_type": "bearer"}


# token依赖的接口，需要用户名和密码验证
@app.get("/connect/user/password", summary="请求用户信息地址（受保护资源）")
async def get_user_password(token: str = Depends(oauth2_scheme)):
    payload = TokenUtils.token_decode(token=token)
    # 定义认证异常信息
    username = payload.get('username')
    if username not in fake_users_db:
        raise HTTPException(status_code=400, detail="不存在此用户信息", headers={"WWW-Authenticate": f"Bearer"})

    userinfo = fake_users_db.get(username)

    return {'info': {
        'username': username,
        'password': userinfo.get('password')
    }}

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
