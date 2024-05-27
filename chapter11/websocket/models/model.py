from db.database import Base
from sqlalchemy import Column, String, DateTime, func,Integer#Integer

class User(Base):
    # 指定本类映射到users表
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 用户号码
    phone_number = Column(String(20))
    # 用户姓名
    username = Column(String(20))
    # 用户密码
    password = Column(String(32))
    # 用户创建时间
    created_at = Column(DateTime(), default=func.now())


