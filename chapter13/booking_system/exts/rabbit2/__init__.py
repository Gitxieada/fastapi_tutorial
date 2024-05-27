from aio_pika import ExchangeType
from fastapi import FastAPI
from pika.exceptions import UnroutableError
import pika

import threading

lock = threading.Lock()
import uuid


class RabbitMQClintWithLock:
    pass

    def __init__(self, app: FastAPI = None):
        # 如果有APPC传入则直接的进行初始化的操作即可
        if app is not None:
            self.init_app(app, None, None)

    def init_app(self, app: FastAPI,rabbitconf,startup_callback):
        self.app = app
        @app.on_event("startup")
        def startup_event():
            self.init_sync_rabbit(rabbitconf)
            # 初始化回调
            startup_callback()
        @app.on_event("shutdown")
        def shutdown_event():
            self._clear_all()


    def init_sync_rabbit(self,rabbitconf):
        credentials = pika.PlainCredentials(rabbitconf.RABBIT_USERNAME, rabbitconf.RABBIT_PASSWORD)
        # 关闭心跳检测
        # virtual_host 类型多租户情况环境隔离的分区，默认使用'/'
        parameters = pika.ConnectionParameters(rabbitconf.RABBIT_HOST, rabbitconf.RABBIT_PORT, rabbitconf.VIRTUAL_HOST,
                                               credentials, heartbeat=0)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    @property
    def _check_alive(self):
        """ 检查连接与信道是否存活 """
        return self.connection and self.connection.is_open and self.channel and self.channel.is_open

    async def make_exchange_declare(self, exchange_name, exchange_type='fanout', durable=True):
        '''创建交换机'''

        self.exchange = await self.channel.declare_exchange(name=exchange_name, type=exchange_type,durable=durable)


    def open_confirm_delivery(self):
        '''开启消息发送到交换机过程监听回调机制，开启后可以在发送消息的时候进行异常的吹'''
        self.channel.confirm_delivery()

    async def make_queue_declare(self, queue_name, durable=True, auto_delete=False, arguments=None):


        self.queue = await self.channel.declare_queue(name=queue_name,durable=durable, auto_delete=auto_delete,arguments=arguments, exclusive=True)


    async def make_queue_bind(self, exchange_name, queue_name, routing_key):
        '''同伙routing_key把交换机和队列的绑定'''
        await self.queue.bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)



    def make_queue_delete(self, queue):
        """删除队列"""
        self.channel.queue_delete(queue)
        print('delete queue:', queue)

    def make_exchange_delete(self, exchange_name):
        self.channel.exchange_delete(exchange_name)

    async def send_basic_publish(self, routing_key, body, content_type="text/plain", exchange_name='',content_encoding='utf-8', message_ttl=3, delivery_mode=2, is_delay=False):
        """生产数据"""

        # 使用简单的所发的方式来避免多线程的不安全引发的问题
        print("开始发送！！")
        with lock:
            try:
                if self._check_alive:
                    if is_delay:
                        #  message: "AbstractMessage",
                        #         routing_key: str,
                        #         *,
                        #         mandatory: bool = True,
                        #         immediate: bool = False,
                        #         timeout: TimeoutType = None
                        await  self.exchange.publish(message, routing_key=routing_key)
                    else:
                       pass
                else:
                    print('连接已断开')
                    # self.init_sync_rabbit()
            except UnroutableError:
                print('消息发送失败')

    def listen_basic_consume(self, queue, func):
        """启动循环监听用于数据消费"""
        self.channel.basic_consume(queue, func)
        self.channel.start_consuming()

    def _close_connect(self):
        """
        # 关闭tcp连接
        :return:
        """
        self.connection.close()

    def _close_channel(self, channel):
        """
        # 关闭信道
        :param channel:
        :return:
        """
        if not hasattr(self, 'channel'):
            raise ValueError("the object of SenderClient has not attr of channel.")

        self.channel.close()

    def _clear_all(self):
        """ 清理连接与信道 """
        if self.connection and self.connection.is_open:
            self.connection.close()
        self.connection = None

        if self.channel and self.channel.is_open:
            self.channel.close()
        self.channel = None


sync_rabbit_client = RabbitMQClintWithLock()