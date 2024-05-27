from fastapi import APIRouter, Depends, HTTPException
from starlette.endpoints import WebSocketEndpoint
from typing import Any, Dict, List, Optional
from schemas import UserDistribute

from starlette.responses import FileResponse
from utils.auth_helper import AuthToeknHelper
from fastapi import WebSocket, status
from utils.room_connection_helper_distributed import RoomConnectionManager
from faker import Faker

fake = Faker(locale='zh_CN')
router_char = APIRouter(tags=["聊天室"])


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
        self.curr_user: Optional[UserDistribute] = None


    async def curr_user_login_init(self, websocket:WebSocket):
        # 当前房间对象

        token = websocket.query_params.get('token')

        if not token:
            # 由于收到不符合约定的数据而断开连接. 这是一个通用状态码,
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        if not self.curr_user and token:
            try:
                AuthToeknHelper.token_decode(token)
                payload = AuthToeknHelper.token_decode(token=token)
                # 解析token信息
                phone_number = payload.get('phone_number')
                username = payload.get('username')
                # 初始化当前连接用户信息
                self.curr_user = UserDistribute(phone_number=phone_number, username=username)
            except:
                pass
                await self.close_clean_user_websocket(code=status.WS_1000_NORMAL_CLOSURE,websocket=websocket)

        if self.room.check_user_logic(self.curr_user):
            # 由于收到不符合约定的数据而断开连接. 这是一个通用状态码,
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            # raise RuntimeError("当前用户已登过了！")

    async def check_user_in_logic(self):
        pass
        if self.curr_user:
            pass

    async def on_connect(self, _websocket):
        # 初始化当前连接到服务端的用户信息
        self.room =_websocket.app.state.room_connection
        # 确认链接
        await _websocket.accept()
        # 初始化当前用户信息
        await self.curr_user_login_init(_websocket)
        # 把用户加入到当前用户列表中，
        self.room.user_add_login_room(self.curr_user)
        # 把客户端连接添加到列表中
        self.room.websocket_add_login_room(self.curr_user,_websocket)
        # 添加连接
        # 广播用户加入聊天室的消息
        await self.room.pubsub_room_user_login(self.curr_user)

    async def close_clean_user_websocket(self,code,websocket):
        # 资源释放处理
        await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
        if self.room:
            self.room.user_out_logout_room(self.curr_user)
            # 删除连接
            self.room.websocket_out_logout_room(self.curr_user, websocket=websocket)

    async def clean_user_websocket(self, code, websocket):
        # 资源释放处理
        await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
        if self.room:
            self.room.user_out_logout_room(self.curr_user)
            # 删除连接
            self.room.websocket_out_logout_room(self.curr_user, websocket=websocket)

    async def on_receive(self, _websocket: WebSocket, msg: str):
        # 根据_websocket找到具体的用户
        if self.curr_user is None:
            # 由于收到不符合约定的数据而断开连接. 这是一个通用状态码,
            # await _websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            await self.close_clean_user_websocket(code=status.WS_1008_POLICY_VIOLATION,websocket=_websocket)


        if not isinstance(msg, str):
            # 由于接收到不允许的数据类型而断开连接 (如仅接收文本数据的终端接收到了二进制数据).
            # await _websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
            await self.close_clean_user_websocket(code=status.WS_1003_UNSUPPORTED_DATA, websocket=_websocket)

        # 广播消息
        await self.room.pubsub_user_send_message(self.curr_user,message=msg)
        # await self.room.broadcast_user_send_message(self.curr_user, msg)


    async def on_disconnect(self, _websocket: WebSocket, _close_code: int):
        pass
        # 要及时删除已关闭的连接
        self.room.user_out_logout_room(self.curr_user)
        # 删除连接
        self.room.websocket_out_logout_room(self.curr_user, websocket=_websocket)

        await self.room.pubsub_room_user_logout(self.curr_user, message=None)


        # # 广播某用户退出房间的消息
        # await self.room.broadcast_room_user_logout(self.curr_user)
        # # 更新在线用户列表信息
        # await self.room.broadcast_system_room_update_userlist()
        # 删除引用
        del self.curr_user

