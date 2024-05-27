from fastapi import FastAPI, Request, Body
from fastapi import Query, Depends
from fastapi.exceptions import HTTPException

from fastapi import FastAPI
from fastapi import Query, Depends
from fastapi.exceptions import HTTPException


app = FastAPI()

def username_check(username:str=Query(...)):
    if username != 'zhong':
        raise HTTPException(status_code=403, detail="没有权限访问")
    return username


@app.get("/user/login/")
def user_login(username: str = Depends(username_check)):
    return username


@app.get("/user/info")
def user_info(username: str = Depends(username_check)):
    return username


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
