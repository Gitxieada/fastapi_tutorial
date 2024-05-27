from dataclasses import dataclass
from pydantic import BaseModel
from starlette.websockets import WebSocket

@dataclass
class User:
    phone_number: str
    username: str
    websocket:WebSocket


class RegisterAaction(BaseModel):
    phone_number: str
    username: str
    password: str

class LoginAaction(BaseModel):
    phone_number: str
    password: str



@dataclass
class UserDistribute :
    phone_number: str
    username: str

@dataclass
class WebSocketDistribute :
    websocket:WebSocket
