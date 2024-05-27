# 定义数据库模型
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# 定义业务逻辑表
from sqlalchemy import Column, Integer, String

metadata = sqlalchemy.MetaData()

class User(Base):
    # 指定本类映射到users表
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    nikename = Column(String(32))
    password = Column(String(32))
    email = Column(String(50))

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String(length=100)),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

from databases import Database


database = Database('sqlite+aiosqlite:///user.db')

# Establish the connection pool
await database.connect()

# Execute
query = notes.insert()
values = {"text": "example1", "completed": True}
await database.execute(query=query, values=values)

