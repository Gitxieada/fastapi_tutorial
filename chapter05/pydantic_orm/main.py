from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel,  Field

# ORM模型基类
Base = declarative_base()
# ORM模型类定义
class UserSqlalchemyOrmModel(Base):
    # 表名称
    __tablename__ = 'user'
    # 表字段
    id = Column(Integer, primary_key=True, nullable=False) # 定义ID
    userid = Column(String(20), index=True, nullable=False, unique=True)  # 创建索引
    username = Column(String(32), index=True,unique=True)


class UserPydanticModel(BaseModel):
    id: int
    userid:str = Field(..., title='用户ID', description='用户ID字段需要长度大于6且小于等于20', max_length=20, min_length=6, example="0000001")
    username: str = Field(..., title='用户名称', description='用户名称字段需要长度大于6且小于等于32', max_length=20, min_length=6,example="0000001")

    class Config:
        # 表示可以-模型类可以从ROM中创建，没有这个话则会报错哦！
        orm_mode = True


# 创建ORM类的对象
user_orm = UserSqlalchemyOrmModel(id=123,userid='1000001001',username='xiaozhong')
# 从ORM类的对象实例化UserPydanticModel的模型对象
print(UserPydanticModel.from_orm(user_orm))
#输出结果：id=123 userid='1000001001' username='xiaozhong'
