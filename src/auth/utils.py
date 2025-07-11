from passlib.context import CryptContext
from datetime import datetime , timedelta
import jwt
import uuid
import logging
from itsdangerous import URLSafeTimedSerializer
from src.config import Config


passwd_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600

def generate_passwd_hash(password : str) -> str:
    hash = passwd_context.hash(password)
    return hash

def verify_password(password: str , hash: str) -> bool:
    return passwd_context.verify(password , hash)

def create_access_token(user_data:dict , expiry:timedelta=None , refresh:bool=False):
    print("user_data=",user_data)
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    print("payload=",payload)
    token = jwt.encode(payload=payload , key=Config.JWT_SECRET , algorithm=Config.JWT_ALGORITHM)
    return token

def decode_token(token:str) -> dict :
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
    
def create_url_safe_token(data: dict):
    serializer = URLSafeTimedSerializer(
        secret_key = Config.JWT_SECRET,
        salt = "email-configuration"
    )
    token = serializer.dumps(data, salt = "email-configuration")
    return token

# def decode_url_safe_token(token: str):
#     try:
#         tokenn_data = serializer.loads(token)
#         return tokenn_data
#     except Exception as e:
#         logging.error(str(e))

def decode_url_safe_token(token: str):
    try:
        serializer = URLSafeTimedSerializer(
            secret_key=Config.JWT_SECRET,
            salt="email-configuration"
        )
        token_data = serializer.loads(token, salt="email-configuration")
        return token_data
    except Exception as e:
        logging.error(str(e))
        return None
    