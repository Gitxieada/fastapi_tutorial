from typing import Optional
from fastapi import FastAPI, Header
from fastapi import Request
from middeware import OpentracingJaegerMiddleware

app = FastAPI()
app.add_middleware(OpentracingJaegerMiddleware, fastapiapp=app)


@app.get("/tracing")
def tracing(request: Request, x_trace_id: Optional[str] = Header(None, convert_underscores=True)):
    # 拿到当前生效的tracer
    tracer = request.app.state.tracer
    # 判断是否存在对应的上一个层级的span
    span = request.state.opentracing_span

    # 创建新的span
    with tracer.start_span('new—span-test', child_of=span) as child_span_1:
        span.log_kv({'event': '父类的span事件信息1'})
        span.log_kv({'event': '父类的span事件信息2',
                     'request.args': request.query_params, })

        # child_span_1.log_kv({'event': 'child_span-down below'})
        # with tracer.start_span('new—span-test-childspan', child_of=child_span_1) as child_span_2:
        #     child_span_2.log_kv({'event': 'new—span-test-childspan-childspan'})


    return "ok"


if __name__ == "__main__":
    import uvicorn
    import os

    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
