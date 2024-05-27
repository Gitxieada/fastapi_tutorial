#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   文件名称 :     hanxuan_rabbit_consumer
   文件功能描述 :   功能描述
   创建人 :       小钟同学
   创建时间 :          2021/10/19
-------------------------------------------------
   修改描述-2021/10/19:         
-------------------------------------------------
"""
import pika
import time
from utils import json_helper
from db.sync_database import sync_context_get_db
from db.models import DoctorSubscribeinfo
from sqlalchemy.sql import and_, asc, desc, or_

# 创建用户登入的凭证，使用rabbitmq用户密码登录
credentials = pika.PlainCredentials("guest", "guest")
# 创建连接http://47.99.189.42:30100/
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, virtual_host='yuyueguahao', credentials=credentials))
# 通过连接创建信道
channel = connection.channel()
# 通过信道创建我们的队列 其中名称是task_queue，并且这个队列的消息是需要持久化的！PS：持久化存储存到磁盘会占空间，
# 队列不能由持久化变为普通队列，反过来也是！否则会报错！所以队列类型创建的开始必须确定的！
order_dead_letter_exchange_name = 'xz-dead-letter-exchange'
order_dead_letter_exchange_type = 'fanout'
order_dead_letter_queue_name = 'xz-dead-letter-queue'
order_dead_letter_routing_key = 'xz-dead-letter-queue'

# 相对比只要交换机名称即可接收到消息的广播模式（fanout），direct模式在其基础上，多加了一层密码限制（routingKey）
channel.exchange_declare(exchange=order_dead_letter_exchange_name, durable=True,
                         exchange_type=order_dead_letter_exchange_type)
channel.queue_declare(queue=order_dead_letter_queue_name, durable=True)
channel.queue_bind(exchange=order_dead_letter_exchange_name, queue=order_dead_letter_queue_name,
                   routing_key=order_dead_letter_routing_key)

print(' [*] 死信队列里面的死信消息的消费. To exit press CTRL+C')


# 初始化数据库的链接处理
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    # 预扣库存回退
    mesgg = json_helper.json_to_dict(body.decode())
    print("死信消息的内容", mesgg)

    # 获取当前的订单支付状态信息，如果当前处于没支付的状态的话，则需要回滚我们的库存
    with sync_context_get_db() as session:
        _result = session.query(DoctorSubscribeinfo).filter(and_(DoctorSubscribeinfo.dno == mesgg.get('dno'),
                                                                 DoctorSubscribeinfo.visit_uopenid == mesgg.get(
                                                                     'visit_uopenid'),
                                                                 DoctorSubscribeinfo.orderid == mesgg.get(
                                                                     'orderid'))).one_or_none()

        if _result:

            #  # 订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单 4：超时未支付订单 5：申请退款状态 6：已退款状态）
            if _result.statue == 2:
                pass
            elif _result.statue == 1:
                pass
                # 更新订单状态
                print("更新状态！！！！！！！！！！！！！")
                session.query(DoctorSubscribeinfo).filter(and_(DoctorSubscribeinfo.dno == mesgg.get('dno'),DoctorSubscribeinfo.orderid == mesgg.get(
                                                                   'orderid'))).update({DoctorSubscribeinfo.statue: 4},
                                                                                       synchronize_session=False)
            elif _result.statue == 3:
                pass
            elif _result.statue == 5:
                pass
            elif _result.statue == 6:
                pass
            else:
                pass
        # 回复确认消息已被消费
        ch.basic_ack(delivery_tag=method.delivery_tag)


# 设置预取消息数量
channel.basic_qos(prefetch_count=1)
# await channel.set_qos(prefetch_count=1)
# 开始进行订阅消费
ack = channel.basic_consume(queue='xz-dead-letter-queue', on_message_callback=callback)
print('s', ack)
# 消费者会阻塞在这里，一直等待消息，队列中有消息了，就会执行消息的回调函数
channel.start_consuming()
