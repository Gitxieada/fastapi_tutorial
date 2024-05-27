#!/usr/bin/evn python
# coding=utf-8
# + + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + +
#        ┏┓　　　┏┓+ +
# 　　　┏┛┻━━━┛┻┓ + +
# 　　　┃　　　　　　 ┃ 　
# 　　　┃　　　━　　　┃ ++ + + +
# 　　 ████━████ ┃+
# 　　　┃　　　　　　 ┃ +
# 　　　┃　　　┻　　　┃
# 　　　┃　　　　　　 ┃ + +
# 　　　┗━┓　　　┏━┛
# 　　　　　┃　　　┃　　　　　　　　　　　
# 　　　　　┃　　　┃ + + + +
# 　　　　　┃　　　┃　　　　Codes are far away from bugs with the animal protecting　　　
# 　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug　　
# 　　　　　┃　　　┃
# 　　　　　┃　　　┃　　+　　　　　　　　　
# 　　　　　┃　 　　┗━━━┓ + +
# 　　　　　┃ 　　　　　　　┣┓
# 　　　　　┃ 　　　　　　　┏┛
# 　　　　　┗┓┓┏━┳┓┏┛ + + + +
# 　　　　　　┃┫┫　┃┫┫
# 　　　　　　┗┻┛　┗┻┛+ + + +
# + + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + ++ + + +"""
"""
Author = zyx
@Create_Time: 2022/4/4 19:31
@version: v1.0.0
@Contact: 308711822@qq.com
@File: main.py
@文件功能描述:------
"""

from fastapi import Depends
from fastapi import FastAPI, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPAuthorizationCredentials
from fastapi.security.http import HTTPBase, HTTPBaseModel, get_authorization_scheme_param
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from hashlib import md5
from typing import Optional
from random import SystemRandom, Random

app = FastAPI(
    title="HTTPBasic认证示例",
    description='HTTPBasic认证示例项目演示例子',
    version='v1.1.0',
)




class HTTPDigest(HTTPBase):

    def __init__(
            self,
            *,
            scheme_name: Optional[str] = None,
            description: Optional[str] = None,
            auto_error: bool = True,
            #  表示Web服务器中受保护文档的安全域（比如公司财务信息域和公司员工信息域），用来指示需要哪个域的用户名和密码
            realm: Optional[str] = None,
            # 保护质量，包含auth（默认的）和auth-int（增加了报文完整性检测）两种策略，（可以为空，但是）不推荐为空值
            qop: Optional[str] = "auth, auth-int",
            # 由服务器指定的字符串，客户端在后续指向同一个受保护区间的请求中应该在 Authorization 头中原样返回，建议使用 base64 或者 16 进制数
            opaque: Optional[str] = None,
    ):
        self.model = HTTPBaseModel(scheme="digest", description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error
        self.realm = realm
        self.qop = qop
        self.opaque = opaque
        self.nonce = None
        self.random = SystemRandom()
        try:
            self.random.random()
        except NotImplementedError:  # pragma: no cover
            self.random = Random()

    def _generate_random(self):
        return md5(str(self.random.random()).encode('utf-8')).hexdigest()

    @property
    def default_generate_nonce(self):
        return self._generate_random()

    async def __call__(
            self, request: Request
    ):
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)

        # 第一次请求，在没有进行认证或认证失败时，服务端需要返回401 Unauthorized，并对客户端发出质询，需要输入用户名和密码等信息
        self.request = request

        if not (authorization and scheme and credentials):
            if self.auto_error:
                if self.realm and self.qop:
                    self.nonce = self.default_generate_nonce
                    self.unauthorized_headers = {
                        "WWW-Authenticate": f'Digest realm="{self.realm}",qop="{self.qop}",nonce="{self.nonce}'}
                else:
                    self.unauthorized_headers = {"WWW-Authenticate": f'Digest realm="{self.realm}",'}
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                    headers=self.unauthorized_headers,
                )
            else:
                return None

        # 如果认证的是已经通过了那么判断收是摘要认证的模式
        if scheme.lower() != "digest":
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
            )
        self.request.state.auth_seeions = {}
        self.request.state.auth_seeions['realm'] = self.realm
        self.request.state.auth_seeions['qop'] = self.qop
        self.request.state.auth_seeions['nonce'] = self.nonce
        # self

        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


def default_verify_password(password, credentials, request: Request):
    # 参数校验是否非法，如果非法的话，那么需要重新的发起一下需要重新的输入用户名称和密码

    realm = request.state.auth_seeions['realm']
    qop = request.state.auth_seeions['qop']
    nonce = request.state.auth_seeions['nonce']
    unauthorized_headers = {
        "WWW-Authenticate": f'Digest realm="{realm}",qop="{qop}",nonce="{nonce}'}
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers=unauthorized_headers,
    )
    datas = {item[0]: item[1] for item in
             [iten.split('=') for iten in credentials.replace('"', '').split(', ')]}
    # 验证值信息，验证账号密码信息，验证用户信息，验证报文信息
    if datas:
        ha1 = generate_ha1(username=datas.get('username'), realm=realm, password=password)
        ha2 = generate_ha2(request)
        # 计算摘要的公式MD5(MD5(A1):<nonce>:<nc>:<conce>:<qop>:MD5(A2))
        response = md5(
            f"{ha1}:{datas.get('nonce')}:{datas.get('nc')}:{datas.get('cnonce')}:{datas.get('qop')}:{ha2}".encode(
                'utf-8')).hexdigest()

        if response != datas.get('response'):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
                headers=unauthorized_headers,
            )
        else:
            return True
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers=unauthorized_headers,
        )


def generate_ha1(username, realm, password):
    a1 = username + ":" + realm + ":" + password
    a1 = a1.encode('utf-8')
    return md5(a1).hexdigest()


def generate_ha2(requet: Request):
    a2 = requet.method + ":" + requet.url.path
    a2 = a2.encode('utf-8')
    return md5(a2).hexdigest()


security = HTTPDigest(realm="nihao.baiwu.net", qop="auth")


@app.get("/digest")
async def digest(request: Request, auth: HTTPAuthorizationCredentials = Depends(security)):
    # print(credentials)
    if default_verify_password(password='123456', credentials=auth.credentials, request=request):
        return PlainTextResponse('登入成功')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main2:app', host="127.0.0.1", port=8000, debug=True, reload=True)
