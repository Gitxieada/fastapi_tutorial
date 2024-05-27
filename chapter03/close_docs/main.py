#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    # 或者直接设置openapi_url=None
    openapi_url=None,
)
if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
