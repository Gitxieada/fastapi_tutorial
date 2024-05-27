from db.database import Base
from sqlalchemy import Column, String, DateTime, func,Integer#Integer

class User(Base):
    # 指定本类映射到users表
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 用户姓名
    username = Column(String(20))
    # 用户密码
    password = Column(String(32))
    # 用户创建时间
    created_at = Column(DateTime(), default=func.now())

class ShortUrl(Base):
    # 指定本类映射到users表
    __tablename__ = 'short_url'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 短链标签
    short_tag = Column(String(20),nullable=False)
    # 短连接地址
    short_url = Column(String(20))
    # 长链接地址
    long_url = Column(String, nullable=False)
    # 访问次数
    visits_count= Column(Integer, nullable=True)
    # 短链创建时间
    created_at = Column(DateTime(), default=func.now())
    # 短链创建时间
    created_by = Column(String(20))
    # 短信内容
    msg_context = Column(String, nullable=False)