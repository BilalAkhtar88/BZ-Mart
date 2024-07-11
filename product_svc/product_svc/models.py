import datetime
from typing import Optional
from pydantic import BaseModel


class Product (BaseModel):
    product_id: str
    name: str
    description: str
    price: float
    category: str


class ProductUpdate(BaseModel):
    product_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None