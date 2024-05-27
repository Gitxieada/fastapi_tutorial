# 创建引擎对象
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine,update,delete
engine = create_engine("sqlite:///user.db")
from sqlmodel import Field, SQLModel

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name:str
    nikename:str
    password :str
    email:str

from sqlmodel import Session,select
with Session(engine) as session:

    allusers = select(Users)
    results = session.exec(allusers)
    for user in results:
        print(user)
    print('>'*5)
    userresult = select(Users).where(Users.name == "xiaozhong1")
    user = session.exec(userresult).first()
    print(user)
    print('>' * 5)
    userresult = select(Users).where(Users.name == "xiaozhong1").where(Users.nikename == "zyx")
    users = session.exec(userresult).all()
    print(users)
    print('>' * 5)
    userresult = select(Users).where(Users.name == "xiaozhong1",Users.nikename == "zyx")
    users = session.exec(userresult).all()
    print(users)

with Session(engine) as session:
    results = session.exec(select(Users).where(Users.name == "xiaozhong1"))
    user = results.first()
    print("user:", user)
    user.email = 'zyx1232@qq.com'
    session.add(user)
    session.commit()
    session.refresh(user)

with Session(engine) as session:
    updateusers = update(Users).where(Users.name == "xiaozhong1")
    results = session.exec(updateusers.values(email='xiaozhong@qw.com'))
    session.commit()

with Session(engine) as session:
    user = session.exec(select(Users).where(Users.name == "xiaozhong1")).first()
    session.delete(user)
    session.commit()

with Session(engine) as session:
    user = session.exec(delete(Users).where(Users.name == "xiaozhong1"))
    session.commit()