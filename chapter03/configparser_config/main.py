#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
import configparser

config = configparser.ConfigParser()
config.read('conf.ini', encoding='utf-8')

app = FastAPI(
    debug=bool(config.get('fastapi_config', 'debug')),
    title=config.get('fastapi_config', 'title'),
    description=config.get('fastapi_config', 'description'),
    version=config.get('fastapi_config', 'version'),
)

if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
