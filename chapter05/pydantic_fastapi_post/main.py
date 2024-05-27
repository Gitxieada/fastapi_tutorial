from fastapi import FastAPI
from pydantic import BaseModel, root_validator, Field

app = FastAPI()


class User(BaseModel):
    username: str = Field(..., title='姓名', description='姓名字段需要长度大于6且小于等于12', max_length=12, min_length=6, example="Foo")
    age: int = Field(..., title='年龄', description='年龄需要大于18岁', ge=18, example=12)
    password_old: str = Field(..., title='旧密码', description='密码需要长度大于6', gl=6, example=6)
    password_new: str = Field(..., title='新密码', description='密码需要长度大于6', gl=6, example=6)

    @root_validator
    def check_passwords(cls, values):
        password_old, password_new = values.get('password_old'), values.get('password_new')
        # 新旧号码的确认匹配处理
        if password_old and password_new and password_old != password_new:
            raise ValueError('passwords do not match')
        return values


@app.post("/user")
def read_user(user: User):
    return {
        'username': user.username,
        'password_old': user.password_old,
        'password_new': user.password_new,
    }


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
