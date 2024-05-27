from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db_session
from db.database import AsyncSession
from servies.user import UserServeries
from servies.short import ShortServeries
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from utils.passlib_hepler import PasslibHelper
from utils.auth_helper import AuthToeknHelper
from utils.random_helper import generate_short_url
from schemas import SingleShortUrlCreate
from fastapi import File, UploadFile

router_uesr = APIRouter(prefix="/api/v1", tags=["用户创建短链管理"])
# 注意需要请求的是完整的路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/oauth2/authorize")


@router_uesr.post("/oauth2/authorize", summary="请求授权URL地址")
async def login(user_data: OAuth2PasswordRequestForm = Depends(), db_session: AsyncSession = Depends(get_db_session)):
    if not user_data:
        raise HTTPException(status_code=400, detail="请输入用户账号及密码等信息")
    # 查询用户是否存在
    userinfo = await UserServeries.get_user_by_name(db_session, user_data.username)
    if not userinfo:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="不存在此用户信息", headers={"WWW-Authenticate": "Basic"})

    # 验证用户密码和哈希密码值是否保持一直
    if not PasslibHelper.verity_password(user_data.password, userinfo.password):
        raise HTTPException(status_code=400, detail="用户密码不对")

    # 签发JWT有效负载信息
    data = {
        'iss ': userinfo.username,
        'sub': 'xiaozhongtongxue',
        'username': userinfo.username,
        'admin': True,
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }
    # 生成Token
    token = AuthToeknHelper.token_encode(data=data)

    return {"access_token": token, "token_type": "bearer"}


@router_uesr.post("/creat/single/short", summary="创建单一短链请求")
async def creat_single(creatinfo: SingleShortUrlCreate, token: str = Depends(oauth2_scheme),
                       db_session: AsyncSession = Depends(get_db_session)):
    payload = AuthToeknHelper.token_decode(token=token)
    # 定义认证异常信息
    username = payload.get('username')
    creatinfo.short_tag = generate_short_url()
    creatinfo.short_url = f"{creatinfo.short_url}{creatinfo.short_tag}"
    creatinfo.created_by = username
    creatinfo.msg_context = f"{creatinfo.msg_context},了解详情请点击 {creatinfo.short_url} ！"
    result = await ShortServeries.create_short_url(db_session, **creatinfo.dict())
    return {"code": 200, "msg": "创建短链成功", "data": {
        "short_url": result.short_url
    }}


@router_uesr.post("/creat/batch/short", summary="通过上传文件方式,批量创建短链")
async def creat_batch(*, file: UploadFile = File(...),
                      token: str = Depends(oauth2_scheme),
                      db_session: AsyncSession = Depends(get_db_session)):
    payload = AuthToeknHelper.token_decode(token=token)
    # 定义认证异常信息
    username = payload.get('username')
    contents = await file.read()
    shorl_msg = contents.decode(encoding='utf-8').split("\n")

    def make_short_url(item):
        split_item = item.split("#")
        short_tag = generate_short_url()
        short_url = f"http://127.0.0.1:8000/{short_tag}"
        return SingleShortUrlCreate(
            long_url=f"{split_item[2]}{split_item[0]}",
            short_tag=short_tag,
            short_url=short_url,
            created_by=username,
            msg_context=f"{split_item[1].replace('chanename', split_item[0]).replace('url', 'short_url')}")

    result = await ShortServeries.create_batch_short_url(db_session, [make_short_url(item) for item in shorl_msg])
    return {"code": 200, "msg": "批量创建短链成功", "data":None}

