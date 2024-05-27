from datetime import datetime
from loguru import logger
from fastapi import FastAPI


def setup_ext_loguru(app: FastAPI, log_pro_path: str = None):
    '''
    :param pro_path:  当前需要生产的日志文件的存在路径
    :return:
    '''

    @app.on_event("startup")
    async def startup():
        # 日志文件初始化处理
        init_loguru_handlers(log_pro_path)


def init_loguru_handlers(log_pro_path: str = None):
    '''
    :param pro_path:  当前需要生产的日志文件的存在路径
    :return:
    '''
    import os
    if not log_pro_path:
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_pro_path = os.path.split(os.path.realpath(__file__))[0]
    # 定义info_log文件名称
    log_file_path = os.path.join(log_pro_path, 'log/info_{time:YYYYMMDD}.log')
    # 定义err_log文件名称
    err_log_file_path = os.path.join(log_pro_path, 'log/error_{time:YYYYMMDD}.log')

    from sys import stdout
    LOGURU_FORMAT: str = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <16}</level> | <bold>{message}</bold>'
    # 这句话很关键避免多次的写入我们的日志
    logger.configure(handlers=[{'sink': stdout, 'format': LOGURU_FORMAT}])
    # 这个也可以启动避免多次的写入的作用，但是我们的 app:register_logger:40 -无法输出
    # logger.remove()
    # 错误日志不需要压缩
    format = " {time:YYYY-MM-DD HH:mm:ss:SSS} | process_id:{process.id} process_name:{process.name} | thread_id:{thread.id} thread_name:{thread.name} | {level} |\n {message}"
    # enqueue=True表示 开启异步写入
    # 使用 rotation 参数实现定时创建 log 文件,可以实现每天 0 点新创建一个 log 文件输出了
    logger.add(err_log_file_path, format=format, rotation='00:00', encoding='utf-8', level='ERROR', enqueue=True)  # Automatically rotate too big file
    # 对应不同的格式
    format2 = " {time:YYYY-MM-DD HH:mm:ss:SSS} | process_id:{process.id} process_name:{process.name} | thread_id:{thread.id} thread_name:{thread.name} | {level} | {message}"

    # enqueue=True表示 开启异步写入
    # 使用 rotation 参数实现定时创建 log 文件,可以实现每天 0 点新创建一个 log 文件输出了
    logger.add(log_file_path, format=format2, rotation='00:00', compression="zip", encoding='utf-8', level='INFO', enqueue=True)  # Automatically rotate too big file