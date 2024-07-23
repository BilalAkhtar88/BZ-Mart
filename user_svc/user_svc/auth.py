import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Secret key to encode and decode JWT tokens
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer instance to extract token from the request header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    username: str | None = None

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)


# import logging
# from datetime import datetime, timezone, timedelta
# from typing import Annotated
# from passlib.context import CryptContext
# from sqlmodel import Session, select
# from fastapi import Depends, HTTPException, status
# # from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError
# from user_svc.models import RefreshTokenData, TokenData, User, Token, Profile
# from user_svc.db import get_session
# from dotenv import load_dotenv
# import os

# load_dotenv()
# SECRET_KEY = os.getenv('SECRET_KEY')
# ALGORITHM = os.getenv('ALGORITHM')
# EXPIRY_TIME = int(os.getenv('EXPIRY_TIME'))
# REFRESH_EXPIRY_DAYS = int(os.getenv('REFRESH_EXPIRY_DAYS'))

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Print values to debug
# print(f"SECRET_KEY: {SECRET_KEY}")
# print(f"ALGORITHM: {ALGORITHM}")
# print(f"EXPIRY_TIME: {type(EXPIRY_TIME)}, {EXPIRY_TIME}")
# print(f"REFRESH_EXPIRY_DAYS: {REFRESH_EXPIRY_DAYS}")


# pwd_context = CryptContext(schemes="bcrypt")

# def hash_password(password) -> str:
#     return pwd_context.hash(password)

# def verify_password(password, password_hash) -> bool:
#     return pwd_context.verify(password, password_hash)

# def get_user_from_db(
#         session: Annotated[Session, Depends(get_session)],
#         username: str | None = None,
#         email: str | None = None
# ) -> User | None:
#     statement = select(User).where(User.username == username)
#     user: User | None = session.exec(statement).first()
#     if not user:
#         statement = select(User).where(User.email == email)
#         user: User | None = session.exec(statement).first()
#         if user:
#             return user
#     return user

# def get_user_data_from_db(
#         session: Annotated[Session, Depends(get_session)],
#         username: str
# ) -> Profile | None:

#     statement = select(Profile).where(Profile.username == username)
#     user_profile = session.exec(statement).first()
#     logger.info(f" user_profile: {user_profile}")
#     # print (f" user_profile: {user_profile}")
#     if not user_profile:
#         return None

#     return user_profile


# def authenticate_user(
#         username,
#         password,
#         session: Annotated[Session, Depends(get_session)]
# ) -> User | None:

#     db_user = get_user_from_db(session=session, username=username)
#     if not db_user:
#         return None
#     if not verify_password(password, db_user.password):
#         return None
#     return db_user

# def create_access_token(
#         data: dict,
#         expiry_time: timedelta | None
# ):

#     data_to_encode = data.copy()
#     if expiry_time:
#         expire = datetime.now(timezone.utc) + expiry_time
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     data_to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     print("SECRET_KEY is ", SECRET_KEY)
#     return encoded_jwt

# def create_refresh_token(
#         data: dict,
#         expiry_time: timedelta | None
# ) -> str:
#     data_to_encode = data.copy()
#     if expiry_time:
#         expire = datetime.now(timezone.utc) + expiry_time
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     data_to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         data_to_encode, SECRET_KEY, algorithm=ALGORITHM, )
#     return encoded_jwt

# def validate_refresh_token(
#         token: str,
#         session: Annotated[Session, Depends(get_session)]
# ):

#     credential_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid token, Please login again",
#         headers={"www-Authenticate": "Bearer"}
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
#         email: str | None = payload.get("sub")
#         if email is None:
#             raise credential_exception
#         token_data = RefreshTokenData(email=email)
#     except:
#         raise JWTError
#     user = get_user_from_db(session, email=token_data.email)
#     if not user:
#         raise credential_exception
#     return user

# def token_service(user: User) -> Token:
#     expire_time = timedelta(minutes=EXPIRY_TIME)
#     access_token = create_access_token(
#         {"sub": user.username}, expire_time)
#     refresh_expire_time = timedelta(days=REFRESH_EXPIRY_DAYS)
#     refresh_token = create_refresh_token(
#         {"sub": user.email}, refresh_expire_time)
#     return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)