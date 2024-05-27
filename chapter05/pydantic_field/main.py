#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from decimal import Decimal
from typing import Union, Optional, List

from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., title='姓名', description='姓名字段需要长度大于6且小于等于12', max_length=12, min_length=6, example="Foo")
    age: int = Field(..., title='年龄', description='年龄需要大于18岁', ge=18, example=12)
    password: str = Field(..., title='密码', description='密码需要长度大于6', gl=6, example=6)
    tax: Optional[float] = Field(None, example=3.2)

if __name__ == '__main__':
    user=User(name='xiaozhong',age=18,password='xxxxxxxxxxx')
    print(user.name)
    print(user.age)
    print(user.password)
