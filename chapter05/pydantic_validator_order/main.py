#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import Dict

from pydantic import BaseModel, validator, ValidationError


class Person(BaseModel):
    username: str
    address: Dict

    @validator("address",pre=True)
    def adress_rule(cls, address):
        # 如果地址长度小于6，那么则返回
        if len(address) < 6:
            raise ValueError("地址长度不能小于6")
        elif len(address) > 12:
            raise ValueError("地址长度不能大于12")
        return address

if __name__ == '__main__':
    try:
        user = Person(username='xiaozhong', address='12345')
    except ValidationError as e:
        print(e.errors())
    else:
        print(user.username, user.address)