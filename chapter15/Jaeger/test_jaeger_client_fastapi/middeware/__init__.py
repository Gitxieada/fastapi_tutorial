
from typing import List, Any
from fastapi import Request
from jaeger_client import Config
from opentracing import Format, tags
from opentracing.scope_managers.asyncio import AsyncioScopeManager
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from fastapi import FastAPI




class OpentracingJaegerMiddleware(BaseHTTPMiddleware):

    def __init__(self,fastapiapp: FastAPI,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.fastapiapp = fastapiapp
        self.fastapiapp.add_event_handler('startup', self.setup_opentracing)

    def setup_opentracing(self):
        # 配置连接信息
        jaeger_host = '192.168.126.130'
        jaeger_port = 6831
        service_name = "测试2"
        trace_id_header = "X-TRACE-ID"
        jaeger_sampler_type = "const"
        jaeger_sampler_rate = 1
        # 初始化链路对象
        _tracer_config = Config(
            config={
                "local_agent": {
                    "reporting_host": jaeger_host,
                    "reporting_port": jaeger_port
                },
                "sampler": {
                    "type": jaeger_sampler_type,
                    "param": jaeger_sampler_rate,
                },
                "trace_id_header": trace_id_header
            },
            service_name=service_name,
            validate=True,
            scope_manager=AsyncioScopeManager()
        )
        self.fastapiapp.state.tracer = _tracer_config.initialize_tracer()



    async def dispatch(self, request: Request, call_next: Any) -> Response:
        # 获取tracer对象
        tracer = request.app.state.tracer
        # 开始解析上下文（Extract函数）：
        # 该函数主要用于在跨服务进程中，进行解析还原上一个传入Span 信息，通常是通过获取请求的headers进行参数信息提取；
        span_context = tracer.extract(format=Format.HTTP_HEADERS, carrier=request.headers)
        # 开始创建span对象通过span_context，来决定是否存在层级span
        span = tracer.start_span(
            operation_name=f"{request.method} {request.url.path}",
            child_of=span_context,
        )

        # ==================================
        # 如果span_context信息不存在的话，则默认会创建第一个父的span对象
        # Span tag：一组键值对构成的Span标签集合。
        # 键值对中，键必须为String，值可以是字符串、布尔或者数字类型。
        # ==================================
        # 给span设置HTTP.UTL的标签
        span.set_tag(tags.HTTP_URL, str(request.url))
        # 设置client请求协议方式标签
        span.set_tag(tags.PEER_HOST_IPV4, request.client.host or "")
        # 设置client请求来源端口的标签
        span.set_tag(tags.PEER_PORT, request.client.port or "")
        # #Component(字符串)ia模块、库或正在生成跨区的包。
        span.set_tag(tags.COMPONENT, 'Fastapi')
        # 标记表示RPC或其他远程调用的服务器端的范围
        span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
        # (字符串)是请求的HTTP方法。
        span.set_tag(tags.HTTP_METHOD, request.method)




        # Scope 对象 主要是管理Active Span的容器
        # Scope 代表着当前活跃的Span; 是对当前活跃Span的一个抽象
        # ScopeManager 包含一个 Scope, Scope 又包含了 当前Span
        with tracer.scope_manager.activate(span, True) as scope:
            # 设置当前tracer对象，传递上下文中
            request.state.opentracing_tracer = tracer
            # 设置当前激活了的scope对象，它里面包含了所有激活的Span
            request.state.opentracing_scope = scope
            # 设置当前解析出来或创建Span对象，传递上下文中
            request.state.opentracing_span = span
            # 下一个response
            response = await call_next(request)

            # inject span 进 requests header
            headers = {}
            tracer.inject(span, Format.HTTP_HEADERS, headers)
            # inject之后，实际 headers = {'uber-trace-id': '6997ed0a6a74f050:bf49be2de63d86e7:e02975aab05fd358:1'}
            print(headers)
        return response


