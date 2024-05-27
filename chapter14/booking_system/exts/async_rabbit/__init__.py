from aio_pika import ExchangeType
from fastapi import FastAPI
from pika.exceptions import UnroutableError
import pika

import threading
import aio_pika
import asyncio
from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractIncomingMessage


class AsyncRabbitMQClint:
    pass

    def __init__(self, app: FastAPI = None):
        # 如果有APPC传入则直接的进行初始化的操作即可
        if app is not None:
            self.init_app(app, None, None)

    def init_app(self, app: FastAPI, rabbitconf, startup_callback):
        self.app = app

        @app.on_event("startup")
        async def startup_event():
            await self.init_sync_rabbit(rabbitconf)
            # 初始化回调
            await startup_callback()

        @app.on_event("shutdown")
        async def shutdown_event():
            await self._clear_all()

    async def init_sync_rabbit(self, rabbitconf):
        self.connection = await aio_pika.connect_robust(host=rabbitconf.RABBIT_HOST,
                                                        port=rabbitconf.RABBIT_PORT,
                                                        virtualhost=rabbitconf.VIRTUAL_HOST,
                                                        login=rabbitconf.RABBIT_USERNAME,
                                                        loop=asyncio.get_event_loop(),
                                                        password=rabbitconf.RABBIT_PASSWORD
                                                        )
        # channel_number: int = None,
        # publisher_confirms: bool = True,
        # on_return_raises: bool = False,
        self.channel: aio_pika.abc.AbstractChannel = await self.connection.channel(publisher_confirms=False)

    async def make_exchange_declare(self, exchange_name, exchange_type='fanout', durable=True):
        '''创建交换机'''
        #  if auto_delete and durable is None:
        #             durable = False
        self.exchange = await self.channel.declare_exchange(name=exchange_name, type=exchange_type,auto_delete=False,durable=durable)


    async def make_queue_declare(self, queue_name, durable=True, auto_delete=False, arguments=None):
        self.queue = await self.channel.declare_queue(name=queue_name, durable=durable, auto_delete=auto_delete,arguments=arguments, exclusive=True)

    async def make_queue_bind(self, exchange_name, routing_key):
        '''同伙routing_key把交换机和队列的绑定'''
        await self.queue.bind(exchange=exchange_name, routing_key=routing_key)


    async def send_basic_publish(self, routing_key, body, content_type="text/plain", content_encoding='utf-8',
                                 message_ttl=3, delivery_mode=2, is_delay=False):
        """生产数据"""
        # 使用简单的所发的方式来避免多线程的不安全引发的问题
        try:
            if is_delay:
                await self.exchange.publish(
                    Message(
                        bytes(body, "utf-8"),
                        expiration=message_ttl * 1000,
                        content_type=content_type,
                        content_encoding=content_encoding,
                        delivery_mode=delivery_mode
                    ),
                    routing_key=routing_key,
                )
            else:
                await self.exchange.publish(
                    Message(
                        bytes(body, "utf-8"),
                        delivery_mode=delivery_mode
                    ),
                    routing_key=routing_key,
                )
        except UnroutableError:
            print('消息发送失败')

    async def _close_connect(self):
        """
        # 关闭tcp连接
        :return:
        """

        await self.connection.close()

    async def _close_channel(self):
        """
        # 关闭信道
        :param channel:
        :return:
        """
        if not hasattr(self, 'channel'):
            raise ValueError("the object of SenderClient has not attr of channel.")

        await self.channel.close()

    async def _clear_all(self):
        """ 清理连接与信道 """
        await self._close_connect()
        self.connection = None

        await self._close_channel()
        self.channel = None


async_rabbit_client = AsyncRabbitMQClint()
