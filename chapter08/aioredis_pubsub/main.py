
from fastapi import FastAPI,Request
import asyncio
import async_timeout
import aioredis
from aioredis.client import Redis

app = FastAPI()

# 定义事件消息模型
from pydantic import BaseModel
class MessageEvent(BaseModel):
    username: str
    message: dict


async def reader(channel: aioredis.client.PubSub):
    print("当前初始化？")
    while True:
        try:
            async with async_timeout.timeout(1):
                # 执行接收订阅消息
                message = await channel.get_message(ignore_subscribe_messages=True)
                print("jiesh？ssssssssss", message)
                if message is not None:
                    pass
                    message_event = MessageEvent.parse_raw(message["data"].decode('utf-8'))
                    print("订阅接收到消息为：",message_event)
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass


@app.on_event("startup")
async def startup_event():
    # 创建Redis对象
    redis:Redis = aioredis.from_url("redis://localhost")
    # 创建消息发布定义对象获取到发布订阅对象
    pubsub = redis.pubsub()
    # 把当前的对象添加到全局APP上下中
    app.state.redis = redis
    app.state.pubsub = pubsub
    # 开始订阅相关频道
    await pubsub.subscribe("channel:1", "channel:2")
    # 消息模型的创建
    event = MessageEvent(username="xiaozhongtongxue", message={"msg": "在startup_event发布的事件消息"})
    # 消息发布0发布到channel:1频道上
    await redis.publish(channel="channel:1", message=event.json())
    # 执行消息订阅循环监听
    asyncio.create_task(reader(pubsub))
    # future = asyncio.create_task(reader(pubsub))
    # 不能加这个等待结果返回，因为里面是一个while 循环，等待返回就会一直阻塞
    # await future


@app.on_event("shutdown")
async def shutdown_event():
    pass
    # 解除相关频道订阅
    app.state.pubsub.unsubscribe("channel:1", "channel:2")
    # 关闭redis连接
    app.state.redis.close()

@app.get('/index')
async def get(re:Request):
    # 手动执行其他消息的发布
    event = MessageEvent(username="xiaozhongtongxue", message={"msg": "我是来自API接口发布的消息！"})
    await re.app.state.redis.publish(channel="channel:1", message=event.json())
    return "ok"

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
