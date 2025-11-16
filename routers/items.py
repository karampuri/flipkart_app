"""
Amazon items CRUD routes with performance optimizations
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from math import ceil

from database import get_db
from schemas import (
    AmazonItemCreate,
    AmazonItemUpdate,
    AmazonItemResponse,
    AmazonItemListResponse,
    MessageResponse
)
from auth import get_current_active_user
from models import User
from crud import ItemRepository

router = APIRouter(prefix="/api/v1/items", tags=["Items"])


@router.post("", response_model=AmazonItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: AmazonItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new Amazon item"""
    item_repo = ItemRepository(db)
    return item_repo.create(item_data)


@router.post("/bulk", response_model=List[AmazonItemResponse], status_code=status.HTTP_201_CREATED)
async def bulk_create_items(
    items_data: List[AmazonItemCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Bulk create Amazon items for better performance"""
    if len(items_data) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create more than 1000 items at once"
        )
    
    item_repo = ItemRepository(db)
    return item_repo.bulk_create(items_data)


@router.get("", response_model=AmazonItemListResponse)
async def get_items(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    search: Optional[str] = Query(None, description="Search in title"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all items with filtering and pagination"""
    item_repo = ItemRepository(db)
    skip = (page - 1) * page_size
    
    items, total = item_repo.get_all(
        skip=skip,
        limit=page_size,
        category=category,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        search=search
    )
    
    total_pages = ceil(total / page_size) if total > 0 else 0
    
    return AmazonItemListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/stream", response_model=List[AmazonItemResponse])
async def stream_items(
    batch_size: int = Query(100, ge=1, le=500, description="Batch size"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Stream items in batches using generator for memory efficiency"""
    item_repo = ItemRepository(db)
    
    # Get first batch
    items_generator = item_repo.get_items_generator(batch_size=batch_size, category=category)
    first_batch = next(items_generator, [])
    
    return first_batch


@router.get("/statistics")
async def get_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get aggregated statistics"""
    item_repo = ItemRepository(db)
    return item_repo.get_statistics()


@router.get("/category/{category}", response_model=List[AmazonItemResponse])
async def get_items_by_category(
    category: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get items by category"""
    item_repo = ItemRepository(db)
    items = item_repo.get_by_category(category)
    return items


@router.get("/search", response_model=List[AmazonItemResponse])
async def search_items(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Search items by title"""
    item_repo = ItemRepository(db)
    items = item_repo.search_items(q, limit=limit)
    return items


@router.get("/{item_id}", response_model=AmazonItemResponse)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get item by ID"""
    item_repo = ItemRepository(db)
    item = item_repo.get_by_id(item_id)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    return item


@router.put("/{item_id}", response_model=AmazonItemResponse)
async def update_item(
    item_id: int,
    item_data: AmazonItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an item"""
    item_repo = ItemRepository(db)
    item = item_repo.update(item_id, item_data)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    return item


@router.delete("/{item_id}", response_model=MessageResponse)
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete an item"""
    item_repo = ItemRepository(db)
    success = item_repo.delete(item_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    return MessageResponse(message=f"Item with id {item_id} deleted successfully")

