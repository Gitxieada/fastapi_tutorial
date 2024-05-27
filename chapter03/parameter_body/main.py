#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from typing import List, Optional, Set
from fastapi import FastAPI, Query, Path, Body
from starlette import status
from enum import Enum

app = FastAPI()

from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    user_id: str
    token: str
    timestamp: str
    article_id: Optional[str] = None


@app.post("/action/")
def callback(item: Item):
    return {
        'user_id': item.user_id,
        'article_id': item.article_id,
        'token': item.token,
        'timestamp': item.timestamp
    }


@app.post("/action/body")
def callbackbody(
        token: str = Body(...),
        user_id: int = Body(..., gt=10),
        timestamp: str = Body(...),
        article_id: str = Body(default=None),
):
    return {
        'user_id': user_id,
        'article_id': article_id,
        'token': token,
        'timestamp': timestamp
    }


@app.post("/action/body2")
def callbackbody(
        token: str = Body(default=None),
        user_id: int = Body(default=None, gt=10),
        timestamp: str = Body(default=None),
        article_id: str = Body(default=None),
):
    return {
        'user_id': user_id,
        'article_id': article_id,
        'token': token,
        'timestamp': timestamp
    }


class Itement(BaseModel):
    user_id: int = Body(..., gt=10, embed=True)
    token: str
    timestamp: str
    article_id: Optional[str] = None


@app.post("/action/body3")
def callbackbody(item: Itement = Body(default=None, embed=False)):
    return {
        'body': item
    }


# =================
class ItemUser(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


class User(BaseModel):
    username: str
    full_name: str = None


@app.put("/items/")
async def update_item1111(item: ItemUser, user: User):
    results = {"item": item, "user": user}
    return results


@app.put("/items/more")
async def update_item(item: Item, user: User, importance: int = Body(..., gt=0)
                      ):
    results = {"item": item, "user": user, "importance": importance}
    return results


class ItemUser2(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    user: User


@app.put("/items/body4")
async def update_item(item: ItemUser2, importance: int = Body(..., gt=0)
                      ):
    results = {"item": item, "user": item.user, "importance": importance}
    return results


class ItemUser3(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    user: User
    # 新增模型嵌套并设置为集合类型
    tags: Set[str] = []
    users: List[User] = None


@app.put("/items/body5")
async def update_item(item: ItemUser3, importance: int = Body(..., gt=0)):
    results = {"item": item, "user": item.user, "importance": importance}
    return results


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
