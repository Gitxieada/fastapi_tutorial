from fastapi import FastAPI
from fastapi.security import SecurityScopes
from fastapi import Security

app = FastAPI()


class AuthCheck:
    def __init__(self, security_scopes: SecurityScopes, role: str):
        print("传入的参数：", security_scopes.scopes)
        self.role = role


@app.get("/auth_check2")
def auth_check(role: str = Security(AuthCheck, scopes=["admin"])):
    return role


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
