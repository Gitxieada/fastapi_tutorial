import requests
import time

def take_up_time(func):
    def wrapper(*args, **kwargs):
        print("开始执行---->")
        now = time.time()
        result = func(*args, **kwargs)
        using = (time.time() - now) * 1000
        print(f"结束执行,消耗时间为：{using}ms")
        return result
    return wrapper

def request_sync(url):
    response = requests.get(url)
    return response

@take_up_time
def run():
    for i in range(0, 50):
        request_sync('https://www.baidu.com')


if __name__ == '__main__':
    run()