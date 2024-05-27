import time
from uuid import uuid4

from redis import Redis

# 创建连接客户端对象
redis = Redis(host="localhost",port=6379,)
# 封装获取锁的值和删除锁操作的Lua脚本script内容
script = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('DEL', KEYS[1])
else
    return 0
end
"""


def action(lock_name='pay_order',client_signature=str(uuid4())):

    print(client_signature)
    if redis.set(name=lock_name, value=client_signature, nx=True, ex=25):  # 锁不存在才能上锁成功，过期时间应为业务时间的五倍，此处故意写小，模拟过期释放
        print('上锁')
        try:
            print('处理业务', client_signature)
            time.sleep(10)
        except Exception as e:
            print(e)
        finally:
            # 释放锁
            cmd = redis.register_script(script)
            res = cmd(keys=[lock_name], args=[client_signature])  # 执行脚本
            if res:
                print('锁已释放')
            else:
                print('不是自己的锁')
    else:
        print('锁已存在')


if __name__ == '__main__':
    action()
