#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI

app = FastAPI(
    title="文档的标题",
    description='关于该API文档一些描述信息补充说明',
    version='v1.0.0',
    openapi_prefix='',
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    swagger_ui_init_oauth=None,
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url="/openapi/openapi_json.json",
    terms_of_service="https://terms/团队的官网网站/",
    deprecated=True,
    contact={
        "name": "邮件接收者信息",
        "url": "https://xxx.cc",
        "email": "308711822@qq.com",
    },
    license_info={
        "name": "版权信息说明 License v3.0",
        "url": "https://xxxxxxx.com",
    },
    openapi_tags=[
        {
            "name": "接口分组",
            "description": "接口分组信息说明",
        },
    ],
    # 配置服务请求地址相关的参数信息
    servers=[
        {"url": "/", "description": "本地调试环境"},
        {"url": "https://xx.xx.com", "description": "线上测试环境"},
        {"url": "https://xx2.xx2.com", "description": "线上生产环境"},
    ]
)

@app.get(path="/index")
async def index():
    return {"index": "index"}

if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
