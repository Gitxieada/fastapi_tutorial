#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   文件名称 :     route
   文件功能描述 :   功能描述
   创建人 :       小钟同学
   创建时间 :          2021/12/30
-------------------------------------------------
   修改描述-2021/12/30:
-------------------------------------------------
"""

from time import perf_counter
from fastapi.routing import APIRoute
from typing import Callable, List, Dict,Optional
from fastapi.responses import Response
import shortuuid
from datetime import datetime
from user_agents import parse
from urllib.parse import parse_qs
from utils import json_helper
from fastapi import Request, FastAPI
from loguru import logger
import json
from exts.logururoute.config import setup_ext_loguru

from fastapi.responses import StreamingResponse
from exts.requestvar import request

__all__ = ("setup_ext_loguru",  "ContextLogerRoute")

class ContextLogerRoute(APIRoute):
    # 再静态的里面使用self来查询也可以，遵循从内到外的查询
    nesss_access_heads_keys = []
    # 是否记录用户US信息
    is_record_useragent = True
    # 是否记录用户提交请求头信息
    is_record_headers = True

    def filter_request_url(self):
        path_info = request.url.path
        # 过滤不需要记录日志请求地址URL
        return path_info not in ['/favicon.ico'] and 'websocket' not in path_info and request.method != 'OPTIONS'

    def filter_response_context(self,response: Response):
        # 过滤不需要记录日志响应体内容信息L
        return 'image' not in response.media_type and hasattr(request.state, 'traceid')

    async def make_request_start_time(self):
        pass
        # 过滤不需要记录日志请求地址URL
        if self.filter_request_url():
            pass
            # 计算时间
            request.state.start_time = perf_counter()

    async def make_request_log_msg(self)->Dict:
        log_msg = None
        if self.filter_request_url():
            ip, method, url = request.client.host, request.method, request.url.path
            # 解析请求提交的表单信息
            try:
                body_form = await request.form()
            except:
                body_form = None
            body = None
            try:
                body_bytes = await request.body()
                if body_bytes:
                    try:
                        body = await  request.json()
                    except:
                        pass
                        if body_bytes:
                            try:
                                body = body_bytes.decode('utf-8')
                            except:
                                body = body_bytes.decode('gb2312')
            except:
                pass
            # 在这里记录下当前提交的body的数据，用于下文的提取
            request.state.body = body
            # 从头部里面获取出对应的请求头信息，用户用户机型等信息获取
            user_agent = parse(request.headers["user-agent"])
            browser = user_agent.browser.version
            if len(browser) >= 2:
                browser_major, browser_minor = browser[0], browser[1]
            else:
                browser_major, browser_minor = 0, 0
            # 用户当前系统OS信息提取
            user_os = user_agent.os.version
            if len(user_os) >= 2:
                os_major, os_minor = user_os[0], user_os[1]
            else:
                os_major, os_minor = 0, 0

            log_msg = {
                'headers': None if not self.is_record_headers else
                [request.headers.get(i, '') for i in
                 self.nesss_access_heads_keys] if self.nesss_access_heads_keys else None,
                # 记录请求URL信息
                "useragent": None if not self.is_record_useragent else
                {
                    "os": "{} {}".format(user_agent.os.family, user_agent.os.version_string),
                    'browser': "{} {}".format(user_agent.browser.family, user_agent.browser.version_string),
                    "device": {
                        "family": user_agent.device.family,
                        "brand": user_agent.device.brand,
                        "model": user_agent.device.model,
                    }
                },
                'url': url,
                # 记录请求方法
                'method': method,
                # 记录请求来源IP
                'ip': ip,
                # 'path': gziprequest.path,
                # 记录请求提交的参数信息
                'params': {
                    'query_params': parse_qs(str(request.query_params)),
                    'from': body_form,
                    'body': body
                },
                "ts": f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
            }
            # 对于没有的数据清除
            if not log_msg['headers']:
                log_msg.pop('headers')
            if not log_msg['params']['query_params']:
                log_msg['params'].pop('query_params')
            if not log_msg['params']['from']:
                log_msg['params'].pop('from')
            if not log_msg['params']['body']:
                log_msg['params'].pop('body')

        return log_msg

    async def before_request_record_loger(self,log_msg=None):
        if self.filter_request_url() and log_msg:
            await async_trace_add_log_record(event_type='request', msg=log_msg)

    async def after_request_record_loger(self,  response: Response):
        if self.filter_response_context(response=response):
            start_time = getattr(request.state, 'start_time')
            end_time = f'{(perf_counter() - start_time):.2f}'
            # 获取响应报文信息内容
            rsp = None
            if not isinstance(response, StreamingResponse):
                if isinstance(response, Response):
                    rsp = str(response.body, encoding='utf-8')
                    try:
                        rsp = json_helper.json_to_dict(rsp)
                    except:
                        pass
                log_msg = {
                    # 记录请求耗时
                    "status_code": response.status_code,
                    'cost_time': end_time,
                    #  记录请求响应的最终报文信息--eval的作用是去除相关的 转义符号 "\"ok\""===》ok
                    'rsp': rsp,
                    "ts": f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
                }
                await async_trace_add_log_record(event_type='response', msg=log_msg)

    async def teardown_requestcontext(self, request: Request, response: Response):
        pass

    def get_route_handler(self) -> Callable:

        original_route_handler = super().get_route_handler()

        # 自定义路由的方式内容
        async def custom_route_handler(request: Request) -> Response:
            # 请求前的处理-日志的初始化操作

            response = None
            try:
                # 链路ID信息设置请求
                await self.make_request_start_time()
                # 链路ID信息设置请求
                log_msg = await self.make_request_log_msg()
                # 开始记录日志信息
                await self.before_request_record_loger(log_msg)
                response = await original_route_handler(request)
                # 一个API请求处理完成后的-日志收尾记录
                await self.after_request_record_loger(response)
                return response
            finally:
                await self.teardown_requestcontext(request, response)

        return custom_route_handler





async def async_trace_add_log_record(event_type='', msg={}, remarks=''):
    '''

    :param event_type: 日志记录事件描述
    :param msg: 日志记录信息字典
    :param remarks: 日志备注信息
    :return:
    '''
    # 如果没有这个标记的属性的，说明这个接口的不需要记录啦！
    if request and hasattr(request.state, 'traceid'):
        # 自增编号索引序
        trace_links_index = request.state.trace_links_index = getattr(request.state, 'trace_links_index') + 1
        log = {
            # 自定义一个新的参数复制到我们的请求上下文的对象中
            'traceid': getattr(request.state, 'traceid'),
            # 定义链路所以序号
            'trace_index': trace_links_index,
            # 时间类型描述描述
            'event_type': event_type,
            # 日志内容详情
            'msg': msg,
            # 日志备注信息
            'remarks': remarks,
        }
        #  为少少相关记录，删除不必要的为空的日志内容信息，
        if not remarks:
            log.pop('remarks')
        if not msg:
            log.pop('msg')
        try:
            log_msg = json_helper.dict_to_json_ensure_ascii(log)  # 返回文本
            logger.info(log_msg)
        except:
            logger.info(getattr(request.state, 'traceid') + '：索引：' + str(
                getattr(request.state, 'trace_links_index')) + ':日志信息写入异常')



