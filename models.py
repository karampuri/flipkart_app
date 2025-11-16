"""
SQLAlchemy models for the application
Uses declarative base for OOP approach
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index, Boolean
from sqlalchemy.sql import func
from database import Base
from datetime import datetime


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_username', 'username'),
        Index('idx_email', 'email'),
    )


class AmazonItem(Base):
    """Amazon items model for CRUD operations"""
    __tablename__ = "amazon_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    rating = Column(Float, nullable=True, index=True)
    reviews_count = Column(Integer, default=0, index=True)
    category = Column(String(100), nullable=False, index=True)
    subcategory = Column(String(100), nullable=True, index=True)
    brand = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    product_url = Column(String(500), nullable=True)
    availability = Column(String(50), default="In Stock")
    seller = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_title', 'title'),
        Index('idx_price', 'price'),
        Index('idx_category', 'category'),
        Index('idx_rating', 'rating'),
        Index('idx_category_price', 'category', 'price'),
    )


class FlipkartOrder(Base):
    """Flipkart sales order model based on flipkart_sales.csv"""
    __tablename__ = "flipkart_orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, unique=True, nullable=False, index=True)
    order_date = Column(DateTime, nullable=False, index=True)
    customer_id = Column(String(50), nullable=False, index=True)
    customer_name = Column(String(200), nullable=False)
    segment = Column(String(50), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=False, index=True)
    country = Column(String(50), nullable=False, default="India")
    region = Column(String(50), nullable=False, index=True)
    product_id = Column(String(50), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    subcategory = Column(String(100), nullable=False, index=True)
    product_name = Column(String(500), nullable=False, index=True)
    sales = Column(Float, nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    discount = Column(Float, nullable=False, default=0.0)
    profit = Column(Float, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_order_date', 'order_date'),
        Index('idx_customer_id', 'customer_id'),
        Index('idx_product_id', 'product_id'),
        Index('idx_order_category', 'category'),  # Renamed to avoid conflict with AmazonItem
        Index('idx_region', 'region'),
        Index('idx_city', 'city'),
        Index('idx_order_date_region', 'order_date', 'region'),
        Index('idx_order_category_sales', 'category', 'sales'),  # Renamed to avoid conflict
    )

