from typing import Tuple

from fastapi import FastAPI, Request, Body
from fastapi import Query, Depends
from fastapi.exceptions import HTTPException

app = FastAPI()


def username_check(username:str=Query(...)):
    if username != 'zhong':
        raise HTTPException(status_code=403, detail="用户名错误！没有权限访问！")
    return username

def age_check(username:str=Depends(username_check),age:int=Query(...)):
    if age <18:
        raise HTTPException(status_code=403, detail="用户名未满18岁!禁止吸烟！")
    return username,age


@app.get("/user/login/")
def user_login(username_and_age: Tuple = Depends(age_check)):
    return {
        'username': username_and_age[0],
        'age': username_and_age[1],
    }


@app.get("/user/info")
def user_info(username_and_age: Tuple = Depends(age_check)):
    return {
        'username':username_and_age[0],
        'age': username_and_age[1],
    }


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
