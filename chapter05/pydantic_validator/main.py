#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import Union, Optional, List

from pydantic import BaseModel, validator, ValidationError


class Person(BaseModel):
    username: str
    password: str

    # '*' 在这里是匹配任意字段
    @validator('*', pre=True)
    def split(cls, v,):
        """如果传参是字符串，根据逗号切割成list"""
        if isinstance(v, str):
            return v.split(',')
        return v


if __name__ == '__main__':
    try:
        user = Person(username='xiaozhong', password='123456')
    except ValidationError as e:
        print(e.errors())
        print(e.json())
    else:
        print(user.username, user.password)
