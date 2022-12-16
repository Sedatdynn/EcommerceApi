from pydantic import BaseModel, Field
from typing import List
from db.mongoIdobject import PyObjectId

class Product(BaseModel):
    id: int
    title: str
    description: str
    price: int
    discountPercentage: float
    rating: float
    stock: int
    brand: str
    category: str
    thumbnail: str
    images: List[str]

class ListProduct(BaseModel):
    products: List[Product]

class BasketInRequest(BaseModel):
    product_id: int

