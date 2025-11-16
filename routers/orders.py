"""
Flipkart orders CRUD routes with performance optimizations
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from math import ceil

from database import get_db
from schemas import (
    FlipkartOrderCreate,
    FlipkartOrderUpdate,
    FlipkartOrderResponse,
    FlipkartOrderListResponse,
    FlipkartOrderStatistics,
    MessageResponse
)
from auth import get_current_active_user
from models import User
from crud import FlipkartOrderRepository

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.post("", response_model=FlipkartOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: FlipkartOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new Flipkart order"""
    order_repo = FlipkartOrderRepository(db)
    
    # Check if order_id already exists
    existing = order_repo.get_by_order_id(order_data.order_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order with order_id {order_data.order_id} already exists"
        )
    
    return order_repo.create(order_data)


@router.post("/bulk", response_model=List[FlipkartOrderResponse], status_code=status.HTTP_201_CREATED)
async def bulk_create_orders(
    orders_data: List[FlipkartOrderCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Bulk create Flipkart orders for better performance"""
    if len(orders_data) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create more than 1000 orders at once"
        )
    
    order_repo = FlipkartOrderRepository(db)
    return order_repo.bulk_create(orders_data)


@router.get("", response_model=FlipkartOrderListResponse)
async def get_orders(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Orders per page"),
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    region: Optional[str] = Query(None, description="Filter by region"),
    city: Optional[str] = Query(None, description="Filter by city"),
    min_sales: Optional[float] = Query(None, ge=0, description="Minimum sales amount"),
    max_sales: Optional[float] = Query(None, ge=0, description="Maximum sales amount"),
    start_date: Optional[datetime] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="End date (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, description="Search in product name or customer name"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all orders with filtering and pagination"""
    order_repo = FlipkartOrderRepository(db)
    skip = (page - 1) * page_size
    
    orders, total = order_repo.get_all(
        skip=skip,
        limit=page_size,
        customer_id=customer_id,
        category=category,
        region=region,
        city=city,
        min_sales=min_sales,
        max_sales=max_sales,
        start_date=start_date,
        end_date=end_date,
        search=search
    )
    
    total_pages = ceil(total / page_size) if total > 0 else 0
    
    return FlipkartOrderListResponse(
        orders=orders,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/stream", response_model=List[FlipkartOrderResponse])
async def stream_orders(
    batch_size: int = Query(100, ge=1, le=500, description="Batch size"),
    region: Optional[str] = Query(None, description="Filter by region"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Stream orders in batches using generator for memory efficiency"""
    order_repo = FlipkartOrderRepository(db)
    
    # Get first batch
    orders_generator = order_repo.get_orders_generator(batch_size=batch_size, region=region)
    first_batch = next(orders_generator, [])
    
    return first_batch


@router.get("/statistics", response_model=FlipkartOrderStatistics)
async def get_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get aggregated statistics for Flipkart orders"""
    order_repo = FlipkartOrderRepository(db)
    stats = order_repo.get_statistics()
    return FlipkartOrderStatistics(**stats)


@router.get("/region/{region}", response_model=List[FlipkartOrderResponse])
async def get_orders_by_region(
    region: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get orders by region"""
    order_repo = FlipkartOrderRepository(db)
    orders = order_repo.get_by_region(region)
    return orders


@router.get("/category/{category}", response_model=List[FlipkartOrderResponse])
async def get_orders_by_category(
    category: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get orders by category"""
    order_repo = FlipkartOrderRepository(db)
    orders = order_repo.get_by_category(category)
    return orders


@router.get("/search", response_model=List[FlipkartOrderResponse])
async def search_orders(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Search orders by product name or customer name"""
    order_repo = FlipkartOrderRepository(db)
    orders = order_repo.search_orders(q, limit=limit)
    return orders


@router.get("/{order_id}", response_model=FlipkartOrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get order by ID"""
    order_repo = FlipkartOrderRepository(db)
    order = order_repo.get_by_id(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    return order


@router.put("/{order_id}", response_model=FlipkartOrderResponse)
async def update_order(
    order_id: int,
    order_data: FlipkartOrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an order"""
    order_repo = FlipkartOrderRepository(db)
    order = order_repo.update(order_id, order_data)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    return order


@router.delete("/{order_id}", response_model=MessageResponse)
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete an order"""
    order_repo = FlipkartOrderRepository(db)
    success = order_repo.delete(order_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    return MessageResponse(message=f"Order with id {order_id} deleted successfully")

