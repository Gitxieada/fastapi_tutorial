#!/usr/bin/evn python
# coding=utf-8
from fastapi import FastAPI
import pathlib
from fastapi import Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="学习Fastapi框架文档",
              description="以下是关于相Fastapi框架文档介绍和描述",
              version="0.0.1",debug=True)



templates = Jinja2Templates(directory=f"{pathlib.Path.cwd()}/templates/")
staticfiles = StaticFiles(directory=f"{pathlib.Path.cwd()}/static/")
app.mount("/static", staticfiles, name="static")


@app.get('/', response_class=HTMLResponse)
@app.get('/index', response_class=HTMLResponse)
@app.post('/index', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request})


def myinex():
    return {"Hello": "myinex api"}

app.get("/myindex", tags=["路由注册方式"], summary="路由注册方式说明")(myinex)


@app.route('/loginjig', methods=['GET', 'POST'], name='loginjig')
def loginjig(req: Request):
    return PlainTextResponse('大爷')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='main:app', host="127.0.0.1", port=65535, reload=True, debug=True)
