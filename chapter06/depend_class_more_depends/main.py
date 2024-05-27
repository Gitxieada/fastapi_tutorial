from fastapi import FastAPI, Request, Body
from fastapi import Query, Depends
from fastapi.exceptions import HTTPException

app = FastAPI()


class UsernameCheck:

    def __init__(self,pwssword:str):
        pass
        self.pwssword = pwssword

    def username_form_query(self, username: str = Query(...)):
        if username != 'zhong':
            raise HTTPException(status_code=403, detail="没有权限访问")
        self.username = username

    def username_form_post(self, username: str = Body(...)):
        if username != 'zhong':
            raise HTTPException(status_code=403, detail="没有权限访问")
        self.username = username

upw= UsernameCheck(pwssword="123456")

@app.get("/user/login/")
def user_login(username: UsernameCheck = Depends(upw.username_form_query)):
    return username


@app.post("/user/info")
def user_info(username: UsernameCheck = Depends(upw.username_form_post)):
    return username


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
