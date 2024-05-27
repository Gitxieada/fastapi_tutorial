from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # 定义连接异步引擎数据库的URL地址
    ASYNC_DATABASE_URI: str = "sqlite+aiosqlite:///short.db"
    # 定义TOEKN的签名信息值
    TOKEN_SIGN_SECRET:str = 'ZcjT6Rcp1yIFQoS7'

@lru_cache()
def get_settings():
    return Settings()
