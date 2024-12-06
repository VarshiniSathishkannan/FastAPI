from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash(pwd:str):
    return pwd_context.hash(pwd)

def verify(plain_pwd:str,hash_pwd:str):
    return pwd_context.verify(plain_pwd,hash_pwd)