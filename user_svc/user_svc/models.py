from typing import Annotated, Optional
from sqlmodel import SQLModel, Field
from fastapi import Form
from pydantic import BaseModel

# user model data received from frontend
class UserIP (BaseModel):
    id: Optional[int] = None
    username: str = Field(unique=True)
    email: str 
    is_seller: bool
    name: str
    password: str    
    operation: Optional[str] = None

# user model to store credentials
class User (SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str 
    is_seller: bool
    hashed_password: str
    # password: str

# user profile data in database
class Profile (SQLModel, table=True):
    username: str | None = Field(default = None, primary_key=True)
    user_id: int | None = Field(default = None, foreign_key="user.id")
    name: str
    email: str
    phone: str
    shipping_address: str
    payment_token: str | None = Field(default = None, unique=True)











# #Restart from here
# class Token (SQLModel):
#     access_token: str
#     token_type: str
#     refresh_token: str


# class TokenData (SQLModel):
#     username: str


# class RefreshTokenData (SQLModel):
#     email: str
# # end-of-file (EOF)

# # register user validation model
# class Register_User (SQLModel):
#     username: Annotated[
#         str,
#         Form(),
#     ]
#     email: Annotated[
#         str,
#         Form(),
#     ]
#     password: Annotated[
#         str,
#         Form(),
#     ]

