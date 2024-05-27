#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import Dict, Optional

from pydantic import BaseModel, validator, ValidationError, PydanticValueError

class AddressError(PydanticValueError):
    code = '错误类型'
    msg_template = '当前地址长度不对，它应该需要{errmeg}，当前传入的值为：{value}'

class Person(BaseModel):
    username: str
    address: str

    @validator("address",pre=False)
    def adress_rule(cls, address):
        # 如果地址长度小于6，那么则返回
        if len(address) < 6:
            raise AddressError(errmeg='小于6',value=address)
        elif len(address) > 12:
            raise AddressError(errmeg='大于12',value=address)
        return address

if __name__ == '__main__':
    # try:
    #     user = Person(username='xiaozhong', address='12345')
    # except ValidationError as e:
    #     print(e.errors())
    # else:
    #     print(user.username, user.address)


    class Person(BaseModel):
        name: str
        nums: str
        age: Optional[int]


    if __name__ == '__main__':
        try:
            user = Person(name='xiaozhong')
        except ValidationError as e:
            # print(e.errors())
            # print(e.json())
            print(str(e))
        else:
            print(user.name, user.age)