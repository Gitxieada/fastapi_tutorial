# 导入异步引擎的模块

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from sqlalchemy import MetaData
from sqlalchemy.engine.url import URL
# URL地址格式
from config.config import get_settings
from sqlalchemy import create_engine

# 创建异步引擎对象
settings = get_settings()
metadata = MetaData()
# 创建ORM模型基类
Base = declarative_base(metadata=metadata)
sync_engine = create_engine(url=URL.create(settings.SYNC_DB_DRIVER,
                                           settings.DB_USER,
                                           settings.DB_PASSWORD,
                                           settings.DB_HOST,
                                           settings.DB_PORT,
                                           settings.DB_DATABASE),
                            echo=settings.DB_ECHO,
                            pool_size=settings.DB_POOL_SIZE,
                            max_overflow=settings.DB_MAX_OVERFLOW,
                            future=True)

# 创建异步的会话管理对象
SyncSessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False, autocommit=False, autoflush=False,
                                future=False)


def depends_get_db_session():
    db_session = None
    try:
        db_session = SyncSessionLocal()
        yield db_session
    except SQLAlchemyError as ex:
        db_session.rollback()
        raise ex
    finally:
        db_session.close()


# 需要使用这个来装饰一下，才可以使用with
@contextmanager
def sync_context_get_db():
    session = SyncSessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as ex:
        session.rollback()
        raise ex
    finally:
        session.close()


if __name__ == '__main__':
    from db.models import Hospitalinfo,DoctorSubscribeinfo
    from sqlalchemy.sql import and_

    with sync_context_get_db() as session:
        ed_user = Hospitalinfo(name='ed', describe='Ed Jones', describeimages='edsnickname')
        session.add(ed_user)

        _result:DoctorSubscribeinfo = session.query(DoctorSubscribeinfo).filter(and_(DoctorSubscribeinfo.dno == '10001',
                                                             DoctorSubscribeinfo.visit_uopenid == 'orE7I59UwXdWzfSK9QGK2fHGtPZ8',
                                                             DoctorSubscribeinfo.orderid == '2207121523229771546')).one_or_none()
        print(_result.dno)
        session.query(DoctorSubscribeinfo).filter(and_(DoctorSubscribeinfo.dno == '10001',
                                                             DoctorSubscribeinfo.visit_uopenid == 'orE7I59UwXdWzfSK9QGK2fHGtPZ8',
                                                             DoctorSubscribeinfo.orderid == '2207121523229771546')).update(
            {DoctorSubscribeinfo.statue: 4},
            synchronize_session=False)