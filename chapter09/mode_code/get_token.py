from fastapi import FastAPI

# 定义我们的APP服务对象
app = FastAPI()


@app.get("/get/access_token")
async def access_token(code: str):
    import requests
    # 第三方服务端请求授权服务器获取access_token的地址
    rsp = requests.get(f"http://127.0.0.1:8000/oauth2/authorize/access_token?client_id=xiaozhong&client_secret=123456&code={code}").json()
    access_token = rsp.get('access_token')
    refresh_token = rsp.get('refresh_token')
    access_token_expires = rsp.get('expires_in')
    username = rsp.get('userid')
    return {
        "access_token": access_token,
        # access_token接口调用凭证超时时间
        "expires_in": access_token_expires,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "userid": username,
        "scope": "SCOPE"
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('get_token:app', host="127.0.0.1", port=8100, debug=True, reload=True)