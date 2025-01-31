import logging
from contextlib import asynccontextmanager
from typing import Annotated, List
# from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from user_svc import auth
from user_svc.db import get_session, create_tables
from user_svc.models import Profile, ProfileData, ProfileResponse, Register_User, Token, TokenData, User
from fastapi.security import OAuth2PasswordBearer
# #Added below
from fastapi.middleware.cors import CORSMiddleware

# As the data in this microservice is critical and needs to be cybersecured, therefore it is stored and read directly from the database.
# Kafka is a distributed event streaming platform, and messages (events) are often stored in plaintext format within the Kafka brokers. 
# This can lead to sensitive user data being exposed if not properly secured.
# Therefore, I directly store and retrieve data from the database in the microservice without any kafka communication.
# Kafka maybe used for token based authentication to communicate with other microservices.
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
EXPIRY_TIME = int(os.getenv('EXPIRY_TIME'))
REFRESH_EXPIRY_DAYS = int(os.getenv('REFRESH_EXPIRY_DAYS'))
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def current_user(
        token: Annotated[str, Depends(oauth_scheme)],
        session: Annotated[Session, Depends(get_session)]
) -> User:

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username: str | None = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = auth.get_user_from_db(session, username=token_data.username)
    if not user:
        raise credential_exception
    return user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Creating Tables')
    create_tables()
    print("Tables Created")
    yield

app: FastAPI = FastAPI(
    lifespan=lifespan, title="User Management Service", version='1.0.0')

# Define the origins that should be allowed to make requests to your API
origins = [
    "http://localhost",
    "http://localhost:8000",
    # "https://8002-cs-892713953527-default.cs-asia-east1-vger.cloudshell.dev",  # Add your specific origin here
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message": "User Management Service"}

# login
@app.post('/token', response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)]
) -> Token:
    user: User | None = auth.authenticate_user(
        form_data.username, form_data.password, session)
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")
    else:
        return auth.token_service(user)

# get access token and refresh token
@app.post("/token/refresh", response_model=Token)
def refresh_token(
    old_refresh_token: str,
    session: Annotated[Session, Depends(get_session)]
) -> Token:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"}
    )
    user: User = auth.validate_refresh_token(old_refresh_token, session)
    if not user:
        raise credential_exception
    return auth.token_service(user)

# register new user
@app.post("/register")
async def regiser_user(
    new_user: Annotated[Register_User, Depends()],
    session: Annotated[Session, Depends(get_session)]
):
    logger.info(f"new_user: {new_user}")
    db_user = auth.get_user_from_db(session, new_user.username, new_user.email)
    if db_user:
        raise HTTPException(
            status_code=409, detail="User with these credentials already exists")
    user = User(username=new_user.username,
                email=new_user.email,
                password=auth.hash_password(new_user.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": f""" User with username:{user.username} successfully registered """}

# create user profile
@app.post('/profile', response_model=ProfileResponse)
async def create_user_profile(
    curr_user: Annotated[User, Depends(current_user)],
    user_data: ProfileData,
    session: Annotated[Session, Depends(get_session)],
) -> Profile:
    print(f"current_user: {curr_user}")
    """ Create user profile """
    try:
        existing_profile: Profile | None = auth.get_user_data_from_db(
            session, curr_user.username)
        if existing_profile:
            raise HTTPException(
                status_code=409, detail="User profile already exists. Try editing it")
        new_profile = Profile(
            username=curr_user.username,
            user_id=curr_user.id,
            email=curr_user.email,
            name=user_data.name,
            phone=user_data.phone,
            shipping_address=user_data.shipping_address
        )
        session.add(new_profile)
        session.commit()
        session.refresh(new_profile)
        print(new_profile)
        return new_profile
    
    except HTTPException as httpexep:
        raise httpexep
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create user profile: {e}")

# store payment token in database and send message to kafka
@app.post("/profile/payment_info")
async def store_payment_token(
    curr_user: Annotated[User, Depends(current_user)],
    payment_token: str,
    session: Annotated[Session, Depends(get_session)]
):
    """ Store payment token in database """
    try:
        existing_profile: Profile | None = auth.get_user_data_from_db(
            session, curr_user.username)
        if not existing_profile:
            raise HTTPException(
                status_code=409, detail="User Profile not found. Try creating it")
        
        # store payment token in database
        existing_profile.payment_token = payment_token
        session.add(existing_profile)
        session.commit()
        session.refresh(existing_profile)

        return {
            "message": "Payment token stored successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


# get user profile
@app.get('/profile/me', response_model=ProfileResponse)
async def get_user_profile(
    curr_user: Annotated[User, Depends(current_user)],
    session: Annotated[Session, Depends(get_session)]
) -> Profile:
    """ Get user profile """
    user_profile: Profile | None = auth.get_user_data_from_db(
        session, curr_user.username)
    if not user_profile:
        raise HTTPException(
            status_code=404, detail="User profile not found")
    return user_profile

# edit user profile
@app.put('/profile', response_model=ProfileResponse)
async def edit_user_profile(
    curr_user: Annotated[User, Depends(current_user)],
    user_data: ProfileData,
    session: Annotated[Session, Depends(get_session)]
) -> Profile:
    """ Edit User Profile """
    try:
        # get existing profile from db
        existing_profile: Profile | None = auth.get_user_data_from_db(
            session, curr_user.username)
        if not existing_profile:
            raise HTTPException(
                status_code=404, detail="User profile not found")
        existing_profile.name = user_data.name
        existing_profile.phone = user_data.phone
        existing_profile.shipping_address = user_data.shipping_address

        # update user profile in database
        session.add(existing_profile)
        session.commit()
        session.refresh(existing_profile)
        return existing_profile
    
    except HTTPException as httexcep:
        raise httexcep
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to edit user profile: {e}")

# update payment_token
@app.put("/profile/payment_info")
async def update_payment_token(
    curr_user: Annotated[User, Depends(current_user)],
    payment_token: str,
    session: Annotated[Session, Depends(get_session)]):
    """ Update payment token """
    try:
        # get existing profile from db
        existing_profile: Profile | None = auth.get_user_data_from_db(
            session, curr_user.username)
        if not existing_profile:
            raise HTTPException(
                status_code=404, detail="User profile not found")
        existing_profile.payment_token = payment_token

        # update user profile in database
        session.add(existing_profile)
        session.commit()
        session.refresh(existing_profile)
        return {
            "message": "Payment token updated successfully"
        }
    
    except HTTPException as httexcep:
        raise httexcep
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update payment token: {e}")

# delete user profile
@app.delete('/profile')
async def delete_user_profile(
    curr_user: Annotated[User, Depends(current_user)],
    session: Annotated[Session, Depends(get_session)]
) -> dict[str, str]:
    """ Delete User Profile """
    try:
        # get existing profile from db
        existing_profile: Profile | None = auth.get_user_data_from_db(
            session, curr_user.username)
        if not existing_profile:
            raise HTTPException(
                status_code=404, detail="User profile not found")

        # delete user profile from database
        session.delete(existing_profile)
        session.commit()
        return {"message": "User profile deleted successfully"}
    
    except HTTPException as httexcep:
        raise httexcep
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete user profile: {e}")
    

@app.get("/users", response_model=List[User])
async def get_all_users(
    session: Annotated[Session, Depends(get_session)]
    # current_user: Annotated[User, Depends(auth.current_user)]
) -> List[User]:
    """
    Development-only endpoint to get all users.
    This should be disabled or removed in production.
    """
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Access forbidden")
    
    users = session.exec(select(User)).all()
    return users

# #*********************************************************************************************************************
# #
# # Comment Everything above for running the below testing code
# #
# #*********************************************************************************************************************

# from fastapi import FastAPI, Depends, HTTPException, status
# from pydantic import BaseModel
# from user_svc.auth import create_access_token, get_current_user, TokenData
# import logging

# app = FastAPI()

# # Sample data for testing
# fake_users_db = {
#     "testuser": {
#         "username": "testuser",
#         "password": "testpassword"
#     }
# }

# class User(BaseModel):
#     username: str
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# @app.post("/token", response_model=Token)
# async def login_for_access_token(user: User):
#     logger.info(f"Received login request for user: {user}")
#     if user.username in fake_users_db and user.password == fake_users_db[user.username]["password"]:
#         access_token = create_access_token(data={"sub": user.username})
#         return {"access_token": access_token, "token_type": "bearer"}
#     else:
#         logger.warning("Invalid username or password")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

# @app.get("/protected-route")
# async def read_protected_route(current_user: TokenData = Depends(get_current_user)):
#     return {"message": f"Hello, {current_user.username}"}
