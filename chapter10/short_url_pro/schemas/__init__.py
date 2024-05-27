from pydantic import BaseModel

class SingleShortUrlCreate(BaseModel):
    """
    创建新短链记录时候需要传递参数信息
    """
    # 需要生成长链接地址
    long_url:str
    # 群发短信内容
    msg_context:str
    # 短连接生成前缀
    short_url:str = "http://127.0.0.1:8000/"
    # 访问次数-默认值是0
    visits_count:int = 0
    # 短链标签-默认可以不传
    short_tag:str = ""
    # 默认不传-通常后端进行生成处理
    created_by = ""

