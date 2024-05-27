from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasslibHelper:
    pass

    # plain_password 明文密码，hashed_password哈希密码
    @staticmethod
    def verity_password(plain_password: str, hashed_password: str):
        """对密码进行校验"""
        return pwd_context.verify(plain_password, hashed_password)

    # 进行哈希 密码加密
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

if __name__ == '__main__':
    print(PasslibHelper.hash_password("123456"))