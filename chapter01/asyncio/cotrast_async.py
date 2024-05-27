import aiohttp, asyncio, time


def take_up_time(func):
    def wrapper(*args, **kwargs):
        print("开始执行---->")
        now = time.time()
        result = func(*args, **kwargs)
        using = (time.time() - now) * 1000
        print(f"结束执行,消耗时间为：{using}ms")
        return result

    return wrapper


async def request_async():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.baidu.com') as resp:
            pass


@take_up_time
def run():
    tasks = [asyncio.ensure_future(request_async()) for x in range(0, 49)]
    loop = asyncio.get_event_loop()
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)


if __name__ == '__main__':
    run()
