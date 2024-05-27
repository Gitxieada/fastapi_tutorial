import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Depends

app = FastAPI()


class AuthCheck:
    def __init__(self, role_name: str):
        self.role_name = role_name

    def __call__(self,):
        print("当前角色是：",self.role_name)
        if self.role_name =='admin':
            return "管理员"
        return "普通用户"

@app.get("/auth_check")
def auth_check(role: str = Depends(AuthCheck(role_name="admin"))):
    return role

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
