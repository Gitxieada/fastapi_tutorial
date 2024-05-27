from fastapi import APIRouter, Depends, HTTPException

from servies.user import UserServeries

from dependencies import get_db_session
from db.database import AsyncSession

from fastapi.responses import FileResponse, PlainTextResponse, RedirectResponse
from schemas import RegisterAaction, LoginAaction
from utils.auth_helper import AuthToeknHelper
from datetime import timedelta, datetime

router_uesr = APIRouter(prefix="/api/v1/user", tags=["用户登入API接口"])


@router_uesr.get("/register")
async def index():
    return FileResponse("templates/register.html")


@router_uesr.get("/register_action")
async def register(user: RegisterAaction = Depends(), db_session: AsyncSession = Depends(get_db_session)):
    # 判断是否已经注册
    result = await UserServeries.get_user_by_phone_number(db_session, user.phone_number)
    if not result:
        # 没有注册则注册并写入数据库
        await UserServeries.create_user(db_session, **user.dict())
        return RedirectResponse("/api/v1/user/login")
    else:
        return PlainTextResponse("该用户已注册过了！请重新输入账号信息")


@router_uesr.get("/login")
async def login():
    return FileResponse("templates/login.html")


@router_uesr.get("/login_action")
async def login_action(user: LoginAaction = Depends(), db_session: AsyncSession = Depends(get_db_session)):
    result = await UserServeries.check_user_phone_number_and_password(db_session, password=user.password,
                                                                      phone_number=user.phone_number)
    if result:
        # 生成一个TOKEN值，签发JWT有效负载信息
        data = {
            'iss ': user.phone_number,
            'sub': 'xiaozhongtongxue',
            'phone_number': user.phone_number,
            'username': result.username,
            # 设置token的哟有效期
            'exp': datetime.utcnow() + timedelta(days=2)
        }
        # 生成Token
        token = AuthToeknHelper.token_encode(data=data)
        # 登入成功，跳转到聊天室中
        return RedirectResponse(f"http://127.0.0.1:8000/api/v1/room/online?token={token}")
    else:
        return PlainTextResponse("用户没注册过了！或密码错误，请重新输入账号信息！")
