from fastapi import FastAPI, Request
import asyncio


async def startup():
    # 创建数据库连接对象
    from databases import Database
    database = Database('sqlite+aiosqlite:///user.db')
    await database.connect()

    # 创建新的数据库表
    query = '''CREATE TABLE user
       (id INT PRIMARY KEY     NOT NULL,
       username           TEXT    NOT NULL,
       password            TEXT     NOT NULL);'''
    await database.execute(query=query)

    # 单条数据插入
    query = "INSERT INTO user (id,username,password) VALUES (1, 'xiaozhong', '123456')"
    await database.execute(query=query)

    # 批量数据插入
    query = "INSERT INTO user(id,username,password) VALUES (:id,:username,:password)"
    values = [
        {"id":2,"username": "xiaozhong_1", "password": '123456-1'},
        {"id":3,"username": "xiaozhong_2", "password": '123456-2'},
        {"id":4,"username": "xiaozhong_3", "password": '123456-3'},
    ]
    # # 批量执行数据插入
    await database.execute_many(query=query, values=values)
    # # 执行查询全部数据
    query = "SELECT * FROM user"
    rows = await database.fetch_all(query=query,)
    print('user listinfo:', rows)
    await database.disconnect()

import asyncio
asyncio.run(startup())
