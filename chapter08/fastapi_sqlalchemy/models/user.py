#!/usr/bin/evn python
# coding=utf-8

from db.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    # 指定本类映射到users表
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    nikename = Column(String(32))
    password = Column(String(32))
    email = Column(String(50))
    # 新增手机号码字段
    mobile = Column(String(50))
    # 新增手机号码字段
