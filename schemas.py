"""
Pydantic schemas for request/response validation
Uses OOP with inheritance for code reusability
"""
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


class Token(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema"""
    username: Optional[str] = None


class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user creation"""
    password: str = Field(..., min_length=6, max_length=100)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class UserResponse(UserBase):
    """Schema for user response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class AmazonItemBase(BaseModel):
    """Base schema for Amazon items"""
    title: str = Field(..., min_length=1, max_length=500)
    price: float = Field(..., gt=0)
    rating: Optional[float] = Field(None, ge=0, le=5)
    reviews_count: Optional[int] = Field(0, ge=0)
    category: str = Field(..., min_length=1, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    product_url: Optional[str] = Field(None, max_length=500)
    availability: Optional[str] = Field("In Stock", max_length=50)
    seller: Optional[str] = Field(None, max_length=200)


class AmazonItemCreate(AmazonItemBase):
    """Schema for creating Amazon items"""
    pass


class AmazonItemUpdate(BaseModel):
    """Schema for updating Amazon items (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    rating: Optional[float] = Field(None, ge=0, le=5)
    reviews_count: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    product_url: Optional[str] = Field(None, max_length=500)
    availability: Optional[str] = Field(None, max_length=50)
    seller: Optional[str] = Field(None, max_length=200)


class AmazonItemResponse(AmazonItemBase):
    """Schema for Amazon item response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class AmazonItemListResponse(BaseModel):
    """Schema for paginated list response"""
    items: List[AmazonItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class MessageResponse(BaseModel):
    """Generic message response schema"""
    message: str


class FlipkartOrderBase(BaseModel):
    """Base schema for Flipkart orders"""
    order_id: int = Field(..., description="Unique order ID")
    order_date: datetime = Field(..., description="Order date")
    customer_id: str = Field(..., min_length=1, max_length=50)
    customer_name: str = Field(..., min_length=1, max_length=200)
    segment: str = Field(..., min_length=1, max_length=50)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=50)
    country: str = Field("India", max_length=50)
    region: str = Field(..., min_length=1, max_length=50)
    product_id: str = Field(..., min_length=1, max_length=50)
    category: str = Field(..., min_length=1, max_length=100)
    subcategory: str = Field(..., min_length=1, max_length=100)
    product_name: str = Field(..., min_length=1, max_length=500)
    sales: float = Field(..., gt=0, description="Sales amount")
    quantity: int = Field(1, ge=1, description="Quantity ordered")
    discount: float = Field(0.0, ge=0, le=1, description="Discount percentage")
    profit: float = Field(..., description="Profit amount")


class FlipkartOrderCreate(FlipkartOrderBase):
    """Schema for creating Flipkart orders"""
    pass


class FlipkartOrderUpdate(BaseModel):
    """Schema for updating Flipkart orders (all fields optional)"""
    order_id: Optional[int] = None
    order_date: Optional[datetime] = None
    customer_id: Optional[str] = Field(None, min_length=1, max_length=50)
    customer_name: Optional[str] = Field(None, min_length=1, max_length=200)
    segment: Optional[str] = Field(None, min_length=1, max_length=50)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=50)
    country: Optional[str] = Field(None, max_length=50)
    region: Optional[str] = Field(None, min_length=1, max_length=50)
    product_id: Optional[str] = Field(None, min_length=1, max_length=50)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    subcategory: Optional[str] = Field(None, min_length=1, max_length=100)
    product_name: Optional[str] = Field(None, min_length=1, max_length=500)
    sales: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=1)
    discount: Optional[float] = Field(None, ge=0, le=1)
    profit: Optional[float] = None


class FlipkartOrderResponse(FlipkartOrderBase):
    """Schema for Flipkart order response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class FlipkartOrderListResponse(BaseModel):
    """Schema for paginated Flipkart orders list response"""
    orders: List[FlipkartOrderResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class FlipkartOrderStatistics(BaseModel):
    """Schema for Flipkart order statistics"""
    total_orders: int
    total_revenue: float
    total_profit: float
    avg_order_value: float
    total_quantity: int
    avg_discount: float
    orders_by_region: Dict[str, int]
    orders_by_category: Dict[str, int]
    top_cities: List[Dict[str, Any]]

