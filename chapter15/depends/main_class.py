import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Depends

app = FastAPI()


class AuthCheck:
    def __init__(self, role: str):
        self.role = role

@app.get("/auth_check")
def auth_check(role: dict = Depends(AuthCheck)):
    return role

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
