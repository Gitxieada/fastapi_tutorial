from fastapi import FastAPI
from exts.exceptions import ApiExceptionHandler
import os
import pathlib
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html, )
from fastapi.staticfiles import StaticFiles
from config.config import get_settings

app = FastAPI(docs_url=None,
              title="XX预约挂号系统",
              description="可以通过关注微信公众号，在公众号内进行预约挂号的系统")

try:
    app.mount("/static", StaticFiles(directory=f"{pathlib.Path.cwd()}/static"), name="static")
except:
    pass

@app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )
# 注册全局异常
ApiExceptionHandler().init_app(app)

# setup_ext_loguru(app, log_pro_path=str(pathlib.Path.cwd()))
# app.router.route_class = ContextLogerRoute
# app.add_middleware(BindContextvarMiddleware)

# 这个中间件会引发异步测试卡顿
# from middlewares.loger.middleware import  LogerMiddleware
# app.add_middleware(LogerMiddleware,log_pro_path=os.path.split(os.path.realpath(__file__))[0])


from apis.hospital.api import router_hospital
from apis.doctor.api import router_docrot
from apis.userorders.api import router_userorders
from apis.payorders.api import router_payorders

app.include_router(router_hospital)
app.include_router(router_docrot)
app.include_router(router_userorders)
app.include_router(router_payorders)


# 初始化同步连接rabbitmq
from exts.async_rabbit import async_rabbit_client
# 启动成功的后的回调
from exts.rabbit import sync_rabbit_client

async def startup_callback_init_data():
    # 为测试方便每次启动都删除
    # sync_rabbit_client.make_exchange_delete('xz-dead-letter-exchange')
    # sync_rabbit_client.make_exchange_delete('xz-order-exchange')
    # # 改队列管理一个死信队列的配置
    order_dead_letter_exchange_name = 'xz-dead-letter-exchange1'
    order_dead_letter_exchange_type = 'fanout'
    order_dead_letter_queue_name = 'xz-dead-letter-queue1'
    order_dead_letter_routing_key = 'xz-dead-letter-queue1'
    await async_rabbit_client.make_exchange_declare(exchange_name=order_dead_letter_exchange_name,exchange_type=order_dead_letter_exchange_type)
    await async_rabbit_client.make_queue_declare(queue_name=order_dead_letter_queue_name)

    await async_rabbit_client.make_queue_bind(exchange_name=order_dead_letter_exchange_name,
                                       routing_key=order_dead_letter_routing_key)

    # # 改队列管理一个死信队列的配置
    order_exchange_name = 'xz-order-exchange1'
    order_exchange_type='direct'
    order_queue_name = 'xz-order-queue1'
    order_routing_key = 'order_handler1'
    order_queue_arguments = {'x-dead-letter-exchange': 'xz-dead-letter-exchange'}
    await async_rabbit_client.make_exchange_declare(exchange_name=order_exchange_name, exchange_type=order_exchange_type)
    await async_rabbit_client.make_queue_declare(queue_name=order_queue_name,arguments=order_queue_arguments)
    await async_rabbit_client.make_queue_bind(exchange_name=order_exchange_name,  routing_key=order_routing_key)

# async_rabbit_client.init_app(app=app,rabbitconf=get_settings(),startup_callback=startup_callback_init_data)


def startup_callback_init_data_sync():
    # 为测试方便每次启动都删除
    # sync_rabbit_client.make_exchange_delete('xz-dead-letter-exchange')
    # sync_rabbit_client.make_exchange_delete('xz-order-exchange')
    # # 改队列管理一个死信队列的配置
    order_dead_letter_exchange_name = 'xz-dead-letter-exchange'
    order_dead_letter_exchange_type = 'fanout'
    order_dead_letter_queue_name = 'xz-dead-letter-queue'
    order_dead_letter_routing_key = 'xz-dead-letter-queue'
    sync_rabbit_client.make_exchange_declare(exchange_name=order_dead_letter_exchange_name,exchange_type=order_dead_letter_exchange_type)
    sync_rabbit_client.make_queue_declare(queue_name=order_dead_letter_queue_name)

    sync_rabbit_client.make_queue_bind(exchange_name=order_dead_letter_exchange_name,
                                       queue_name = order_dead_letter_queue_name,
                                       routing_key=order_dead_letter_routing_key)

    # # 改队列管理一个死信队列的配置
    order_exchange_name = 'xz-order-exchange'
    order_exchange_type='direct'
    order_queue_name = 'xz-order-queue'
    order_routing_key = 'order_handler'
    order_queue_arguments = {'x-dead-letter-exchange': 'xz-dead-letter-exchange'}
    sync_rabbit_client.make_exchange_declare(exchange_name=order_exchange_name, exchange_type=order_exchange_type)
    sync_rabbit_client.make_queue_declare(queue_name=order_queue_name,arguments=order_queue_arguments)
    sync_rabbit_client.make_queue_bind(exchange_name=order_exchange_name,queue_name=order_queue_name,routing_key=order_routing_key)
#try:
#   sync_rabbit_client.init_app(app=app,rabbitconf=get_settings(),startup_callback=startup_callback_init_data_sync)
#except:
#    pass




def creat_app():
    return app
