import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Depends

app = FastAPI()
# 导入插件类
from plugins.request_hook import HookPluginClient
rehook:HookPluginClient = HookPluginClient()
rehook.init_app(app)

@rehook.on_event(event_type='before_request')
def before_request(reqest):
    print("before_request", reqest)


@rehook.on_event(event_type='after_request')
def after_request(reqest,response):
    print("after_request", reqest,response)


@rehook.on_event(event_type='teardown_appcontext')
def teardown_appcontext(request, response):
    print("teardown_appcontext", request,response)

class AuthCheck:
    def __init__(self, role: str):
        self.role = role

@app.get("/index")
def index():
    return 'index'

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
