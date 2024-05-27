from aioredis import Redis, ConnectionPool
from fastapi import FastAPI
import aioredis
from fastapi import Request

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # app.state.redis_client = aioredis.from_url("redis://localhost")
    # app.state.redis_client = aioredis.Redis(host='localhost')
    # pool = ConnectionPool(host='localhost',)
    # app.state.redis_client = aioredis.Redis(connection_pool=pool)
    pool = ConnectionPool(host='localhost', encoding="utf-8", decode_responses=True)
    app.state.redis_client = aioredis.Redis(connection_pool=pool)
    # redis_client:Redis =  app.state.redis_client
    await app.state.redis_client.flushall()
    await app.state.redis_client.set("test_key",'testdata')
    print(await app.state.redis_client.get("test_key"))
    await app.state.redis_client.set("test_zh", '我是谁')
    print(await app.state.redis_client.get("test_zh"))


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis_client.close()

@app.get("/index")
async def index():
    key = 'xiaozhong'
    # 设置缓存数据
    await app.state.redis_client.set(key=key,value="测试数据")
    # 读取缓存数据
    cache1 = await app.state.redis_client.get(key=key)

    key_2 = 'xiaozhong_2'
    # 添加数据，5秒后自动清除
    await app.state.redis_client.setex(key=key_2, seconds=5, value="测试数据2")
    # 测试2缓存数据的获取
    cache2 = await app.state.redis_client.get(key=key_2)
    return {
        "cache1":cache1,
        "cache2": cache2,
    }

@app.get("/index2")
async def index2(request: Request):
    async with request.app.state.redis_client.pipeline(transaction=True) as pipe:
        ok1, ok2 = await (pipe.set("xiaozhong", "测试数据").set("xiaozhong_2", "测试数据2").execute())
        pass
    async with request.app.state.redis_client.pipeline(transaction=True) as pipe:
        cache1, cache2 = await (pipe.get("xiaozhong").get("xiaozhong_2").execute())
        print(cache1, cache2)
    return {
        "cache1":cache1,
        "cache2": cache2,
    }

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
