#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import Dict

from pydantic import BaseModel, validator, ValidationError, PydanticValueError

from pydantic import BaseModel, ValidationError, root_validator


class User(BaseModel):
    username: str
    password_old: str
    password_new: str

    @root_validator
    def check_passwords(cls, values):
        password_old, password_new = values.get('password_old'), values.get('password_new')
        # 新旧号码的确认匹配处理
        if password_old and password_new and password_old != password_new:
            raise ValueError('passwords do not match')
        return values

if __name__ == '__main__':
    try:
        user = User(username='xiaozhong', password_old='123456', password_new='123456_')
    except ValidationError as e:
        print(e.errors())
    else:
        print(user.username, user.password_old)
