from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class ProductConsumer (BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: str
    name: str
    description: str
    price: float
    category: str
    operation: Optional[str] = None

class ProductStore (SQLModel, table=True):
    #This model is used to reflect the product fetched from or stored in tables in database
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: str
    name: str
    description: str
    price: float
    category: str
