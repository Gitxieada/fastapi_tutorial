
from fastapi import  HTTPException,status
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from jose import jwt

SECRET_KEY = "la3rwLn7VA%A9v*NC^$FX5J5QtW^T!B4"
ALGORITHM = "HS256"



class AuthToeknHelper:

    @staticmethod
    def token_encode(data):
        jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def token_decode(token):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": f"Bearer"},
        )
        try:
            # 开始反向解析我们的TOKEN.,解析相关的信息
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except (JWTError, ValidationError):
            raise credentials_exception
        return payload

if __name__ == '__main__':
    print(AuthToeknHelper.token_encode({"user":"XZSD"}))
    print(AuthToeknHelper.token_decode(AuthToeknHelper.token_encode({"user":"XZSD"})))