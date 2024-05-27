# 创建引擎对象
from sqlalchemy import create_engine

engine = create_engine('sqlite:///user.db')
# 定义数据库模型
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# 定义业务逻辑表
from sqlalchemy import Column, Integer, String


class User(Base):
    # 指定本类映射到users表
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    nikename = Column(String(32))
    password = Column(String(32))
    email = Column(String(50))


# 执行业务逻辑表的创建
Base.metadata.create_all(engine, checkfirst=True)
# 创建数据库连接会话
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
# 对模型类进行CRUD操作
_user = User(name='xiaozhong', nikename='Zyx', password='123456', email='zyx@qq.com')
session.add(_user)
session.commit()
# 查询数据库记录
from typing import List
result:List[User]=session.query(User).filter_by(name='xiaozhong').all()
for item in result:
    print(item.name,item.password,item.email)
# 仅仅查询提取模型中某些字段信息，
result1:List[User]=session.query(User.name,User.email,User.password).filter_by(name='xiaozhong').all()
for item in result1:
    print(item.name,item.password,item.email)
# 进行模糊匹配的查询
result2:List[User]=session.query(User).filter(User.name.like("xiao%")).all()
for item in result2:
    print(item.name,item.password,item.email)
#字段正则表达式查询
result3:List[User]=session.query(User).filter(User.name.op("regexp")("^xiao")).all()
for item in result2:
    print(item.name,item.password,item.email)
# 查更新
updata_user:User = session.query(User).filter_by(name='xiaozhong').first()
updata_user.email = 'zyx123@qq,com'
session.commit()
session.query(User).filter_by(name='xiaozhong').update({User.email: 'zyx123456@qq,com'})
session.commit()
# 查询并函数
del_user:User = session.query(User).filter_by(name='xiaozhong').first()
if del_user:
    session.delete(del_user)
    session.commit()
session.query(User).filter_by(name='xiaozhong').delete()
session.commit()
# 或者
session.query(User).filter(User.name=='xiaozhong').delete(synchronize_session=False)
session.commit()