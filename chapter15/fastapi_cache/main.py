import aioredis
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder
from typing import Optional
app = FastAPI()


@app.on_event("startup")
async def startup():
    # 开始初始化缓存对象
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    # 缓存库的插件实例化，传入的是要的是RedisBackend后端实例
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/cache1")
@cache(expire=60)
async def index():
    return dict(code=200,message="响应成功")

@app.get("/cache2")
@cache(namespace='test',expire=60)
async def index():
    return JSONResponse(content={"code":200,"message":"设置命名空间"})

@app.get("/cache_jsoncode")
@cache(expire=60,coder=JsonCoder)
async def cache_jsoncode():
    return dict(code=200, message="自定义编码器")

# 自定义生成缓存的KEY的方法
def my_key_builder(func,namespace: Optional[str] = "",request: Request = None,response: Response = None,*args,**kwargs,):
    prefix = FastAPICache.get_prefix()
    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{kwargs}"
    return cache_key

@app.get("/customer_key")
@cache(expire=60,coder=JsonCoder,key_builder=my_key_builder)
async def index():
    return dict(code=200, message="自定义生成缓存KEY示例")


if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
