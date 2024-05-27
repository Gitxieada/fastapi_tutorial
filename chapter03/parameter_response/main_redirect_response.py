#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI

from starlette.responses import  HTMLResponse, RedirectResponse


app = FastAPI()



@app.get("/baidu", response_class=HTMLResponse)
async def index():
   # 外部地址重定向
   return RedirectResponse("https://wwww.baidu.com")

@app.get("/redirect1")
async def index():
   # 内部地址重定向
   return RedirectResponse("/index",status_code=301)


@app.get("/redirect2")
async def index():
   # 内部地址重定向
   return RedirectResponse("/index",status_code=302)

@app.get("/index")
async def index():
   return {
       'code':200,
       'messgaee':'重定向成功'
   }

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
