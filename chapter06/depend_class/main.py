from fastapi import FastAPI, Request, Body
from fastapi import Query, Depends
from fastapi.exceptions import HTTPException

from fastapi import FastAPI
from fastapi import Query, Depends
from fastapi.exceptions import HTTPException


app = FastAPI()

class UsernameCheck:
    def __init__(self, username:str=Query(...)):
        if username != 'zhong':
            raise HTTPException(status_code=403, detail="没有权限访问")
        self.username = username


@app.get("/user/login/")
def user_login(username: UsernameCheck  = Depends(UsernameCheck)):
    return username


@app.get("/user/info")
def user_info(username: UsernameCheck = Depends(UsernameCheck)):
    return username


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
