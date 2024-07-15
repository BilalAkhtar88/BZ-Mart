from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    product_id: str
    name: str
    description: str
    price: float
    category: str
    operation: Optional[str] = None

class ProductUpdate(BaseModel):
    id: Optional[str] = None
    product_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    operation: Optional[str] = None
