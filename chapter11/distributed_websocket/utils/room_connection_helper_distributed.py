from typing import Dict, Optional
from schemas import UserDistribute
import aioredis
from aioredis import Redis
from aioredis.client import PubSub
import async_timeout
import asyncio
import datetime
# from faker import Faker
from typing import List
from fastapi import WebSocket
from pydantic import BaseModel
from fastapi.concurrency import run_until_first_complete


# fake = Faker(locale='zh_CN')


class MessageEvent(BaseModel):
    user: UserDistribute
    channel: str
    message: str = None


class RoomConnectionManager:
    pass

    def __init__(self):
        # 仅仅存储是用户信息不保存对应WebSocket对象
        self._users_socket: Dict[str, UserDistribute] = {}
        # 连接对象单独的划分存贮
        self.active_connections: List[WebSocket] = []
        # self.active_connections: Dict[str,WebSocket] = {}
        # 当前服务启动的时候reids客户端对象
        self.redis: Optional[Redis] = None
        self.pubsub: Optional[PubSub] = None

    async def register_pubsub(self):
        # 监听频道消息
        if not self.redis:
            self.redis: Redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
        # 返回发布/订阅对象,使用pubsub才可以订阅频道并收听发布到的消息
        self.pubsub = self.redis.pubsub()

    async def do_listacton(self):

        await self.pubsub.subscribe("chat：system_room_update_userlist",
                                    "chat：system_msg_user_login",
                                    "chat：system_msg_user_logout",
                                    "chat：user_send_msg"
                                    )

        async def reader(channel: aioredis.client.PubSub):
            while True:
                try:
                    async with async_timeout.timeout(1):
                        message = await channel.get_message(ignore_subscribe_messages=True)
                        if message is not None:
                            pass

                            message_event: MessageEvent = MessageEvent.parse_raw(message["data"])

                            # 判断消息频道=====根据不同的频道
                            if message_event.channel == 'chat：system_msg_user_login':
                                # 广播用户在线列表信息
                                await self.broadcast_system_room_update_userlist()
                                # 广播有用加入信息UserDistribute
                                await self.broadcast_room_user_login(curr_user=message_event.user)
                            if message_event.channel == 'chat：system_msg_user_logout':
                                pass
                                # await self.broadcast_user_send_message(self.curr_user, msg)
                                # # 更新在线用户列表信息

                                # # 广播某用户退出房间的消息
                                await self.broadcast_room_user_logout(leave_user=message_event.user)
                                await self.broadcast_system_room_update_userlist()

                            if message_event.channel == 'chat：user_send_msg':
                                pass
                                await self.broadcast_user_send_message(curr_user=message_event.user,msg=message_event.message)

                        await asyncio.sleep(0.01)
                except asyncio.TimeoutError:
                    pass


        # await asyncio.create_task(reader(self.pubsub))
        asyncio.create_task(reader(self.pubsub))

    def close_pubsub(self):
        pass
        if self.redis:
            self.redis.close()

    def user_add_login_room(self, user: UserDistribute):
        # 添加当前连接到客户端用户到当前字典中
        if user.phone_number not in self._users_socket:
            self._users_socket[user.phone_number] = user

    def websocket_add_login_room(self, user: UserDistribute, websocket: WebSocket):
        # 添加当前连接到客户端用户到当前字典中
        self.active_connections.append(websocket)
        # self.active_connections[user.phone_number] = websocket

    def user_out_logout_room(self, user: UserDistribute):
        # 在当前的字典从删除退出房间用户
        if user.phone_number in self._users_socket:
            del self._users_socket[user.phone_number]

    def websocket_out_logout_room(self, user: UserDistribute, websocket: WebSocket):
        # 添加当前连接到客户端用户到当前字典中
        self.active_connections.remove(websocket)
        # self.active_connections.pop(user.phone_number)

    def check_user_logic(self, userlogin: UserDistribute):
        if userlogin.phone_number in self._users_socket:
            return True
        return False

    # async def pubsub_system_room_update_userlist(self, user: UserDistribute, message: str):
    #     if self.redis:
    #         enevt = MessageEvent(user=user, message=message)
    #         # 发布消息新增用户进入房间的消息
    #         await self.redis.publish("chat：system_room_update_userlist", enevt.json())

    async def pubsub_room_user_login(self, user: UserDistribute, channel: str = "chat：system_msg_user_login"):
        pass
        if self.redis:
            enevt = MessageEvent(user=user, channel=channel,message=None)
            # print("消息了吗？", enevt)
            # 发布消息新增用户进入房间的消息
            await self.redis.publish(channel=channel, message=enevt.json())

    async def pubsub_room_user_logout(self, user: UserDistribute, channel: str="chat：system_msg_user_logout",message:str=None):
        pass
        if self.redis:
            enevt = MessageEvent(user=user, channel=channel,message=message)
            # 发布消息新增用户进入房间的消息
            await self.redis.publish(channel=channel, message=enevt.json())

    async def pubsub_user_send_message(self, user: UserDistribute, channel: str="chat：user_send_msg",message:str=None):
        if self.redis:
            enevt = MessageEvent(user=user, channel="chat：user_send_msg",message=message)
            # 发布消息新增用户进入房间的消息
            await self.redis.publish(channel=channel, message=enevt.json())

    async def broadcast_system_room_update_userlist(self):
        # 循环调用用户里面的连接对象发送广播
        user_online_list = [f"{user.username}({user.phone_number})" for userid, user in self._users_socket.items()]
        # for key,websocket in self.active_connections.items():
        for websocket in self.active_connections:
            await websocket.send_json(
                {"type": "system_room_update_userlist",
                 "data": {'users_list': user_online_list}})

    async def broadcast_room_user_login(self, curr_user: UserDistribute):
        # 循环调用用户里面的连接对象发送广播
        for websocket in self.active_connections:
            # 广播当前登入的用户的信息
            await websocket.send_json(
                {"type": "system_msg_user_login",
                 "data": {'phone_number': self._users_socket[curr_user.phone_number].phone_number,
                          'username': self._users_socket[curr_user.phone_number].username}})

    async def broadcast_room_user_logout(self, leave_user):
        for websocket in self.active_connections:
            await websocket.send_json(
                {"type": "system_msg_user_logout", "data": {'phone_number': leave_user.phone_number,
                                                            'username': leave_user.username}})

    async def broadcast_user_send_message(self, curr_user: UserDistribute, msg: str):
        # 提取是否属于我自己的发言信息
        for websocket in self.active_connections:
            # 判断处理是否我自己发出的消息
            sendmsg = f"{curr_user.username}说：{msg}"
            await websocket.send_json(
                {"type": "user_send_msg", "data": {'phone_number': curr_user.phone_number,
                                                   'username': curr_user.username, "msg": sendmsg,
                                                   "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
