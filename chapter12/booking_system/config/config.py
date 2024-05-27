from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    # database = PostgresqlDatabase('guahaoxitong', **{'host': '47.99.189.42', 'port': 5432,
    #                                                     'user': 'postgres',
    #                                                     'password': 'xiao@#SsLIV(&%$cPha*m)+=asoEW-#'})
    # 连接数据库引擎
    ASYNC_DB_DRIVER: str = "postgresql+asyncpg"
    # 连接数据库引擎
    SYNC_DB_DRIVER: str = "postgresql"
    # 数据库HOST
    DB_HOST: str = "47.99.189.42"
    # 数据库端口号
    DB_PORT: int = 5432
    # 数据库用户名
    DB_USER: str = "postgres"
    # 数据库密码
    DB_PASSWORD: str = "xiao@#SsLIV(&%$cPha*m)+=asoEW-#"
    # 需要连接数据库名称
    DB_DATABASE: str = "booking_system2"
    # 是否输出SQL语句
    DB_ECHO: bool = False
    # 默认的连接池的额大小
    DB_POOL_SIZE: int = 60
    DB_MAX_OVERFLOW: int = 0

    #公众号-开发者ID(AppID)
    GZX_ID: str = 'wx91df1c5a300ddc3d' # 微信公众号ID
    #公众号-开发者密码
    GZX_SECRET:str = '1f484aa3403b7c867d13a5e10c193191'
    GZX_PAY_KEY: str = '0wmDjLVuk904Ddyj0fLwpX1ymiBMIkXh' # 微信支付秘钥
    MCH_ID: str = '1613748420' # 微信支付ID
    NOTIFY_URL =   'http://hx.wohuayuan.com/hs/api/v1/doctor/subscribe/paycallback' #支付回调

    #  没有值的情况下的默认值--默认情况下读取的环境变量的值
    # 链接用户名
    RABBIT_USERNAME: str = 'admin'
    # 链接密码
    RABBIT_PASSWORD: str = 'admin'
    # 链接的主机
    RABBIT_HOST: str = 'rabbit'
    # 链接端口
    RABBIT_PORT: int = 5672
    # 要链接租户空间名称
    VIRTUAL_HOST: str = 'yuyueguahao'
    # 心跳检测
    RABBIT_HEARTBEAT = 5


@lru_cache()
def get_settings():
    return Settings()
