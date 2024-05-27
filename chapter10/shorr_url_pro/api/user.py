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
@Create_Time: 2022/4/3 22:13
@version: v1.0.0
@Contact: 308711822@qq.com
@File: user.py.py
@文件功能描述:------
"""
from fastapi import APIRouter
from schemas.user import UserCreate,UserUpdate
from servies.user import UserServeries
from db.database import AsyncSession
from dependencies import get_db_session
from fastapi import Depends

router_uesr = APIRouter(prefix="/api/v1/user", tags=["用户管理"])


@router_uesr.post("/user/creat")
async def creat(user:UserCreate,db_session: AsyncSession = Depends(get_db_session)):
    result= await UserServeries.create_user(db_session,**user.dict())
    return {"code": "200", "msg": "用户创建成功！","data":result}


@router_uesr.get("/user/info")
async def info(user_id:int,db_session: AsyncSession = Depends(get_db_session)):
    result = await UserServeries.get_user(db_session,user_id=user_id)
    return {"code": "200", "msg": "查询用户信息成功！","data":result}


@router_uesr.get("/user/list")
async def list(db_session: AsyncSession = Depends(get_db_session)):
    result = await UserServeries.get_users(db_session)
    return {"code": "200", "msg": "查询用户列表信息成功！","data":result}


@router_uesr.put("/user/edit")
async def edit(user:UserUpdate,db_session: AsyncSession = Depends(get_db_session)):
    result = await UserServeries.update_user(db_session,user_id=user.id,name=user.name)
    return {"code": "200", "msg": "修改用户信息成功！","data":None}


@router_uesr.delete("/user/delete")
async def delete(user_id:int,db_session: AsyncSession = Depends(get_db_session)):
    result = await UserServeries.delete_user(db_session, user_id=user_id)
    return {"code": "200", "msg": "删除用户信息成功！"}
