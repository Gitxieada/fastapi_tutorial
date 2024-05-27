import asyncio
import aioredis
from aioredis.lock import Lock


async def redis_look():
    # 创建客户端对象
    r = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)

    # 定义获取锁对象，设置锁的超时时间
    def get_lock(redis, lock_name, timeout=10,sleep=0.2,blocking_timeout=None,lock_class=Lock,thread_local=True):
        return redis.lock(name=lock_name, timeout=timeout,sleep=sleep,blocking_timeout=blocking_timeout, lock_class=lock_class,thread_local=thread_local)

    # 实例化一个锁对象
    lock = get_lock(redis=r, lock_name='xiaozhong')
    # 开始获取到锁对象blocking为Flase，则不再阻塞，直接返回结果
    lock_acquire = await lock.acquire(blocking=False,)
    if lock_acquire:
        # 开始上锁---
        is_locked = await lock.locked()
        if is_locked:
            print("执行业务逻辑处理！")
            # 锁的token
            token = lock.local.token
            # 表示当前页面所需时间
            await asyncio.sleep(15)
            # 判断当前锁是否是自己的锁
            await lock.owned()
            # 增加过期时间
            await lock.extend(10)
            # 表示获取锁当前的过期时间
            await r.pttl(name="xiaozhong")
            print("客户端的锁的签名：", token)
            # 表示重新获取锁
            await lock.reacquire()
            # 锁的释放
            await lock.release()


if __name__ == "__main__":
    asyncio.run(redis_look())
