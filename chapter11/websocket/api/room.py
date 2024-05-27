from fastapi import APIRouter, Depends, HTTPException
from starlette.endpoints import WebSocketEndpoint
from typing import Any, Dict, List, Optional


from schemas import UserDistribute, User

from starlette.responses import FileResponse
from utils.auth_helper import AuthToeknHelper
from fastapi import WebSocket, status

from faker import Faker

from utils.room_connection_helper import RoomConnectionManager

fake = Faker(locale='zh_CN')
router_char = APIRouter(tags=["聊天室"])

# 实例化房间连接管理类
room = RoomConnectionManager()

@router_char.get("/api/v1/room/online")
def index():
    return FileResponse("templates/room.html")


@router_char.websocket_route("/api/v1/room/socketws")
@router_char.websocket_route("/api/v1/room/socketws/")
class ChatRoomWebSocket(WebSocketEndpoint):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 每一个客户端请求进来的时候都会执行创建一次，归属当前会话请求
        # 用户登入授权的token
        self.curr_user: Optional[User] = None

    async def curr_user_login_init(self, websocket):

        token = websocket.query_params.get('token')
        if not token:
            # 由于收到不符合约定的数据而断开连接. 这是一个通用状态码,
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise RuntimeError("用户还没有登入！")
        if not self.curr_user and token:
            payload = AuthToeknHelper.token_decode(token=token)
            # 解析token信息
            phone_number = payload.get('phone_number')
            username = payload.get('username')
            # 初始化当前连接用户信息
            self.curr_user = User(phone_number=phone_number, username=username, websocket=websocket)

        if room.check_user_logic(self.curr_user):
            # 由于收到不符合约定的数据而断开连接. 这是一个通用状态码,
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise RuntimeError("当前用户已登过了！")

    async def check_user_in_logic(self):
        pass
        if self.curr_user:
            pass

    async def on_connect(self, websocket):

        # 初始化当前连接到服务端的用户信息
        await self.curr_user_login_init(websocket)

        # 等待连接处理
        await websocket.accept()
        # 把用户加入到当前用户列表中，前端收到这个消息后，主要是把当前服务用户列表信息广播到所有客户端。用于显示在线用户信息
        room.user_add_login_room(self.curr_user)
        # 广播用户加入聊天室的消息
        await room.broadcast_room_user_login(self.curr_user)
        # 添加在线用户列表信息
        await room.broadcast_system_room_update_userlist()

    async def on_receive(self, websocket: WebSocket, msg: str):
        # 根据_websocket找到具体的用户
        if self.curr_user is None:
            # 由于收到不符合约定的数据而断开连接. 这是一个通用状态码,
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise RuntimeError("用户还没有登入！")
        if not isinstance(msg, str):
            # 由于接收到不允许的数据类型而断开连接 (如仅接收文本数据的终端接收到了二进制数据).
            await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
            raise ValueError("发送的消息格式错误")
        await room.broadcast_user_send_message(self.curr_user, msg)

    async def on_disconnect(self, _websocket: WebSocket, _close_code: int):
        pass
        # 要及时删除已关闭的连接
        room.user_out_logout_room(self.curr_user)
        # 广播某用户退出房间的消息
        await room.broadcast_room_user_logout(self.curr_user)
        # 更新在线用户列表信息
        await room.broadcast_system_room_update_userlist()
        # 删除引用
        del self.curr_user
