
from fastapi import  HTTPException,status
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from jose import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
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
