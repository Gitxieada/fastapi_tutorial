#!/usr/bin/evn python
# coding=utf-8
# + + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + +
#        ┏┓　　　┏┓+ +
# 　　　┏┛┻━━━┛┻┓ + +
# 　　　┃　　　　　　 ┃ 　
# 　　　┃　　　━　　　┃ ++ + + +
# 　　 ████━████ ┃+
# 　　　┃　　　　　　 ┃ +
# 　　　┃　　　┻　　　┃
# 　　　┃　　　　　　 ┃ + +
# 　　　┗━┓　　　┏━┛
# 　　　　　┃　　　┃　　　　　　　　　　　
# 　　　　　┃　　　┃ + + + +
# 　　　　　┃　　　┃　　　　Codes are far away from bugs with the animal protecting　　　
# 　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug　　
# 　　　　　┃　　　┃
# 　　　　　┃　　　┃　　+　　　　　　　　　
# 　　　　　┃　 　　┗━━━┓ + +
# 　　　　　┃ 　　　　　　　┣┓
# 　　　　　┃ 　　　　　　　┏┛
# 　　　　　┗┓┓┏━┳┓┏┛ + + + +
# 　　　　　　┃┫┫　┃┫┫
# 　　　　　　┗┻┛　┗┻┛+ + + +
# + + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + +"""
"""
Author = zyx
@Create_Time: 2022/4/3 20:18
@version: v1.0.0
@Contact: 308711822@qq.com
@File: confiig.py
@文件功能描述:------
"""

from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # 定义连接数据库的URL地址
    ASYNC_DATABASE_URI: str = "sqlite+aiosqlite:///user.db"

@lru_cache()
def get_settings():
    return Settings()
