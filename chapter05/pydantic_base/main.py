#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import Union, Optional, List

from pydantic import BaseModel, \
    DirectoryPath, \
    IPvAnyAddress, \
    FilePath, \
    EmailStr, \
    NameEmail, SecretStr, SecretBytes, ValidationError, HttpUrl
from datetime import date


class Person(BaseModel):
    # 基础类型
    name: str  # 字符串类型
    age: int  # 整形类型
    enable: bool  # 布尔类型
    hobby: list  # 列表类型
    adress: dict  # 字典类型
    birthday: date  # datetime中的时间类型

    # 其他复杂的对象类型
    filePath: FilePath  # 文件路径类型
    directoryPath: DirectoryPath  # 文件目录类型
    ip: IPvAnyAddress  # IP地址类型
    emailStr: EmailStr  # 电子邮件地址类型
    nameEmail: NameEmail  # 有效格式的电子邮件地址类型
    secretStr: SecretStr  # 敏感信息数据类型，最终会被格式化为'**'进行代替覆盖
    secretBytes: SecretBytes  # 同步是敏感数据类型
    website: HttpUrl


if __name__ == '__main__':
    try:
        user = Person(name='xiaozhong')
    except ValidationError as e:
        print(e.errors())
        print(e.json())
    else:
        print(user.name, user.age)
