import aiohttp
import asyncio
import time


def take_up_time(func):
    # 自定义装饰器，用于计算函数执行时间
    async def wrapper(*args, **kwargs):
        print("开始执行---->")
        now = time.time()
        result = await func(*args, **kwargs)
        using = (time.time() - now) * 1000
        print(f"结束执行,消耗时间为：{using}ms")
        return result

    return wrapper


async def request_async():
    # 异步请求函数
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.baidu.com') as resp:
            pass


@take_up_time
async def run():
    # 主要逻辑函数，使用async关键字定义异步函数
    tasks = [asyncio.create_task(request_async()) for x in range(0, 49)]
    # 创建包含异步任务的列表

    await asyncio.wait(tasks)
    # 使用await等待所有任务完成


def main():
    # 主函数
    asyncio.run(run())
    # 运行异步函数run()
    #  asyncio.run和下面的使用 同理
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(run())
    # loop.close()


import os
if __name__ == '__main__':
    # 需要注意需要在此处设置才可以运行
    if os.name == 'nt':
        # 在Windows系统中设置事件循环策略，解决 "Event loop is closed" 错误
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
    # 调用主函数开始执行异步任务
