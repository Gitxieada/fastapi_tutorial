#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseSettings, validator
from pydantic.tools import lru_cache


class Settings(BaseSettings):
    debug: bool = False
    title: str
    description: str
    version: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    @validator("version", pre=True)
    def version_len_check(cls, v: str) -> Optional[str]:
        if v and len(v) == 0:
            return None
        return v

@lru_cache()
def get_settings():
    return Settings()

settings = Settings()
print(settings.debug)
print(settings.title)
print(settings.description)
print(settings.version)

settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
app = FastAPI(
    debug=settings.debug,
    title=settings.title,
    description=settings.description,
    version=settings.version,
)


if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
