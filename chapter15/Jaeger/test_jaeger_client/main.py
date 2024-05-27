import logging
import time
from jaeger_client import Config


def construct_span(tracer):
    # 定义span的名称为TestSpan
    with tracer.start_span('TestSpan') as span:
        # 设置这个span传递的日志信息
        span.log_kv({'event': '父Span', 'other': "我是第一个父的Span"})
        time.sleep(1)
        # 定义AliyunTestSpan的子Span，类似第一个追踪的数据的子层级
        with tracer.start_span('TestSpan-ChildSpan-01', child_of=span) as child_span:
            time.sleep(2)
            # 设置父的span键值对日志信息
            span.log_kv({'event': '我是父Span--日志1'})
            # 设置子child_span的日志
            child_span.log_kv({'event': '父Span--第一层子Span-01'})
        with tracer.start_span('TestSpan-ChildSpan-01', child_of=span) as child_span:
            time.sleep(3)
            span.log_kv({'event': '我是父Span--日志2'})
            child_span.log_kv({'event': '父Span--第一层子Span-02'})

            with tracer.start_span('TestSpanC-hildSpan-01-01', child_of=child_span) as Span3_child_span:
                time.sleep(4)
                span.log_kv({'event': '我是父Span--日志3'})
                Span3_child_span.log_kv({'event': '父Span--第一层子Span-的下一个子Span'})

        return span


if __name__ == "__main__":
    # 定义日志输出的登记
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    # 配置日志默认输出格式
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
    # Jaeger配置信息
    config = Config(
        # 服务信息配置
        config={
            # sampler 采样
            'sampler': {
                'type': 'const',  # 采样类型
                'param': 1,  # 采样开关 1：开启全部采样 0：关闭全部
            },
            # 配置链接到我们的本地的agent，通过agent来上报
            'local_agent': {
                # 注意这里是指定了JaegerAgent的host和port。
                # 根据官方建议为了保证数据可靠性，JaegerClient和JaegerAgent运行在同一台主机内，因此reporting_host填写为127.0.0.1。
                'reporting_host': '192.168.126.130',
                'reporting_port': 6831,
            },
            'logging': True,
        },
        # 这里填写应用名称---服务的名称
        service_name="MyFirstSpan",
        validate=True
    )

    # this call also sets opentracing.tracer
    tracer = config.initialize_tracer()
    # 创建一个自定义的额span
    span = construct_span(tracer)
    # 根据官网提示 这里是必须的存在，因为它是基于tornado的异步的方式来处理数据上报！
    #  # yield to IOLoop to flush the spans - https://github.com/jaegertracing/jaeger-client-python/issues/50
    time.sleep(2)
    tracer.close()  # flush any buffered spans
