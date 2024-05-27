from fastapi import FastAPI, Request, Body
from fastapi import Query, Depends
from fastapi.exceptions import HTTPException

from fastapi import FastAPI
from fastapi import Query, Depends
from fastapi.exceptions import HTTPException
from fastapi import APIRouter


def username_check(username: str = Query(...)):
    if username != 'zhong':
        raise HTTPException(status_code=403, detail="用户名错误！没有权限访问！")
    return username


def age_check(age: int = Query(...)):
    if age < 18:
        raise HTTPException(status_code=403, detail="用户名未满18岁!禁止吸烟！")
    return age


app = FastAPI()

user_group_router = APIRouter(prefix='/user')


@user_group_router.get("/login")
def user_login():
    return {
        'code': 'login_ok'
    }


order_group_router = APIRouter(prefix='/order')


@order_group_router.get("/pay")
def order_pay():
    return {
        'code': 'pay_ok'
    }


app.include_router(user_group_router,dependencies=[Depends(username_check)])
app.include_router(order_group_router,dependencies=[Depends(username_check), Depends(age_check)])


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
