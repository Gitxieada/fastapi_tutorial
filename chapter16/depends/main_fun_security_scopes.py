from fastapi import FastAPI
from fastapi.security import SecurityScopes
from fastapi import Security

app = FastAPI()


def auth_check(security_scopes: SecurityScopes):
    print("传入的参数：", security_scopes.scopes)
    if security_scopes.scopes[0] == 'admin':
        return "管理者"
    return "普通用户"


@app.get("/auth_check")
def auth_check(role: str = Security(auth_check, scopes=["admin"])):
    return role


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
