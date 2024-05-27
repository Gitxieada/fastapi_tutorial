from typing import Dict, Optional
from schemas import User
import aioredis
from aioredis import Redis
import async_timeout
import asyncio
import datetime
from faker import Faker

fake = Faker(locale='zh_CN')


class RoomConnectionManager:
    pass

    def __init__(self):
        self._users_socket: Dict[str, User] = {}

    def user_add_login_room(self, user: User):
        # 添加当前连接到客户端用户到当前字典中
        if user.phone_number not in self._users_socket:
            self._users_socket[user.phone_number] = user

    def user_out_logout_room(self, user: User):
        # 在当前的字典从删除退出房间用户
        if user.phone_number in self._users_socket:
            del self._users_socket[user.phone_number]

    def check_user_logic(self, userlogin: User):
        if userlogin.phone_number in self._users_socket:
            return True
        return False

    async def broadcast_system_room_update_userlist(self):
        # 循环调用用户里面的连接对象发送广播
        user_online_list = [f"{user.username}({user.phone_number})" for userid, user in self._users_socket.items()]
        for userid, user in self._users_socket.items():
            await user.websocket.send_json(
                {"type": "system_room_update_userlist", "data": {'users_list': user_online_list}})

    async def broadcast_room_user_login(self, curr_user: User):
        # 循环调用用户里面的连接对象发送广播
        for userid, user in self._users_socket.items():
            # 广播当前登入的用户的信息
            await user.websocket.send_json(
                {"type": "system_msg_user_login",
                 "data": {'phone_number': self._users_socket[curr_user.phone_number].phone_number,
                          'username': self._users_socket[curr_user.phone_number].username}})

    async def broadcast_room_user_logout(self, leave_user):
        for userid, user in self._users_socket.items():
            await user.websocket.send_json({"type": "system_msg_user_logout",
                                            "data": {'phone_number': leave_user.phone_number,
                                                     'username': leave_user.username}})

    async def broadcast_user_send_message(self, leave_user: User, msg: str):
        for userid, user in self._users_socket.items():
            # 判断处理是否我自己发出的消息
            if userid == leave_user.phone_number:
                sendmsg = f"我({leave_user.username})说：{msg}"
            else:
                sendmsg = f"{leave_user.username}说：{msg}"
            await user.websocket.send_json(
                {"type": "user_send_msg",
                 "data": {'phone_number': leave_user.phone_number, 'username': leave_user.username, "msg": sendmsg,
                          "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
