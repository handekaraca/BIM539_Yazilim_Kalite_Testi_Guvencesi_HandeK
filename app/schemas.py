from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryResponse(CategoryCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    name: str
    price: float
    category_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None

class ProductResponse(ProductCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    status: str = "pending"

class OrderUpdate(BaseModel):
    status: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ReviewCreate(BaseModel):
    product_id: int
    comment: str
    rating: int

class ReviewUpdate(BaseModel):
    comment: Optional[str] = None
    rating: Optional[int] = None

class ReviewResponse(ReviewCreate):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)