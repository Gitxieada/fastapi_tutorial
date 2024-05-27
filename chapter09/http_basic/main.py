from fastapi import Depends
from fastapi import FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse
from starlette.status import HTTP_401_UNAUTHORIZED

app = FastAPI(
    title="HTTPBasic认证示例",
    description='HTTPBasic认证示例项目演示例子',
    version='v1.1.0',
)

security = HTTPBasic()

@app.get("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "xiaozhongtongxue" or credentials.password != "xiaozhongtongxue":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        return PlainTextResponse('登入成功')


if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)