#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import Union, Optional, List

from pydantic import BaseModel, ValidationError


class Person(BaseModel):
    # 基础类型
    name: str  # 字符串类型
    password: str  # 字符串类型
    age: int  # 整形类型
    enable: bool = True  # 布尔类型



if __name__ == '__main__':
    try:
        user = Person(name='xiaozhong', password='123456', age=15)
    except ValidationError as e:
        print(e.errors())
        print(e.json())
    else:
        # print(user.dict())
        print(user.dict(exclude_unset=True))
        # print(user.dict(exclude={'password'}))
        print(user.json(exclude={'password'},models_as_dict=False))
        # # 进行拷贝==================
        # new_user = user.copy()
        # print("userID", user, id(user))
        # print("new_userID", new_user, id(new_user))
        # # 仅仅包含密码输出===========
        new_user = user.copy(include={'password'})
        # print("new_user", new_user)
        print("new_userID", new_user, id(new_user))
