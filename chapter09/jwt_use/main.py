from datetime import timedelta
from jose import jwt
from datetime import datetime


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRRSH_ACCESS_TOKEN_EXPIRE_MINUTES = 70


class TokenUtils:

    @staticmethod
    def token_encode(data):
        jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def token_decode(token):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


data = {
    'iss ': "xiaozhong",
    'sub': 'xiaozhongtongxue',
    'name': 'superadmin',
    'admin': True,
    'exp': datetime.utcnow() + timedelta(minutes=15)
}


token = TokenUtils.token_encode(data=data)
print(token)
payload = TokenUtils.token_decode(token =token)
print(payload)
