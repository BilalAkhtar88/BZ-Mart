import logging
from datetime import datetime, timezone, timedelta
from typing import Annotated
from passlib.context import CryptContext
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from user_svc.db import get_session
from user_svc.models import User
# from user_service.models import RefreshTokenData, TokenData, User, Token, Profile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes="bcrypt")

# function to create password hash
def hash_password(password) -> str:
    return pwd_context.hash(password)

#function to get user from db
def get_user_from_db(
        session: Annotated[Session, Depends(get_session)],
        username: str | None = None,
        email: str | None = None
) -> User | None:
    # session.query(User).filter(User.username == username).first()
    user: User | None = session.exec(select(User).where(User.username == username)).first()
    if user:
        logger.warning(f'User with username {User.username} already exists.')
        return user
    else:
        user: User | None = session.exec(select(User).where(User.email == email)).first()
        if user:
            logger.warning(f'User with email {User.email} already exists with a username {user.username}.')
            return user
    return user


    