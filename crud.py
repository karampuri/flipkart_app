"""
CRUD operations with performance optimizations
Uses generators, map, filter, and OOP patterns for efficiency
"""
from typing import List, Optional, Generator, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from sqlalchemy.orm import selectinload

from models import AmazonItem, User, FlipkartOrder
from schemas import AmazonItemCreate, AmazonItemUpdate, UserCreate, FlipkartOrderCreate, FlipkartOrderUpdate


class ItemRepository:
    """Repository class for Amazon items CRUD operations using OOP"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, item_data: AmazonItemCreate) -> AmazonItem:
        """Create a new item"""
        db_item = AmazonItem(**item_data.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def get_by_id(self, item_id: int) -> Optional[AmazonItem]:
        """Get item by ID"""
        return self.db.query(AmazonItem).filter(AmazonItem.id == item_id).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        search: Optional[str] = None
    ) -> tuple[List[AmazonItem], int]:
        """Get all items with filtering and pagination"""
        query = self.db.query(AmazonItem)
        
        # Apply filters using functional programming approach
        filters = []
        
        if category:
            filters.append(AmazonItem.category == category)
        if min_price is not None:
            filters.append(AmazonItem.price >= min_price)
        if max_price is not None:
            filters.append(AmazonItem.price <= max_price)
        if min_rating is not None:
            filters.append(AmazonItem.rating >= min_rating)
        if search:
            filters.append(AmazonItem.title.contains(search))
        
        # Combine filters using and_
        if filters:
            query = query.filter(and_(*filters))
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination and ordering
        items = query.order_by(desc(AmazonItem.created_at)).offset(skip).limit(limit).all()
        
        return items, total
    
    def get_items_generator(
        self,
        batch_size: int = 100,
        category: Optional[str] = None
    ) -> Generator[List[AmazonItem], None, None]:
        """Get items in batches using generator for memory efficiency"""
        query = self.db.query(AmazonItem)
        
        if category:
            query = query.filter(AmazonItem.category == category)
        
        query = query.order_by(desc(AmazonItem.created_at))
        
        offset = 0
        while True:
            items = query.offset(offset).limit(batch_size).all()
            if not items:
                break
            yield items
            offset += batch_size
    
    def update(self, item_id: int, item_data: AmazonItemUpdate) -> Optional[AmazonItem]:
        """Update an item"""
        db_item = self.get_by_id(item_id)
        if not db_item:
            return None
        
        # Use dict comprehension to filter out None values
        update_data = {k: v for k, v in item_data.dict().items() if v is not None}
        
        # Update fields using map for efficiency
        for key, value in update_data.items():
            setattr(db_item, key, value)
        
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def delete(self, item_id: int) -> bool:
        """Delete an item"""
        db_item = self.get_by_id(item_id)
        if not db_item:
            return False
        
        self.db.delete(db_item)
        self.db.commit()
        return True
    
    def bulk_create(self, items_data: List[AmazonItemCreate]) -> List[AmazonItem]:
        """Bulk create items for better performance"""
        db_items = [AmazonItem(**item.dict()) for item in items_data]
        self.db.add_all(db_items)
        self.db.commit()
        
        # Refresh objects to get IDs
        for item in db_items:
            self.db.refresh(item)
        
        return db_items
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get aggregated statistics using SQL functions"""
        stats = self.db.query(
            func.count(AmazonItem.id).label('total_items'),
            func.avg(AmazonItem.price).label('avg_price'),
            func.min(AmazonItem.price).label('min_price'),
            func.max(AmazonItem.price).label('max_price'),
            func.avg(AmazonItem.rating).label('avg_rating')
        ).first()
        
        return {
            'total_items': stats.total_items or 0,
            'avg_price': float(stats.avg_price or 0),
            'min_price': float(stats.min_price or 0),
            'max_price': float(stats.max_price or 0),
            'avg_rating': float(stats.avg_rating or 0)
        }
    
    def get_by_category(self, category: str) -> List[AmazonItem]:
        """Get items by category using index for fast lookup"""
        return self.db.query(AmazonItem).filter(
            AmazonItem.category == category
        ).order_by(desc(AmazonItem.rating)).all()
    
    def search_items(self, search_term: str, limit: int = 50) -> List[AmazonItem]:
        """Search items by title with full-text search optimization"""
        return self.db.query(AmazonItem).filter(
            AmazonItem.title.contains(search_term)
        ).order_by(desc(AmazonItem.rating)).limit(limit).all()


class UserRepository:
    """Repository class for User operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_data: UserCreate, hashed_password: str) -> User:
        """Create a new user"""
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()


class FlipkartOrderRepository:
    """Repository class for Flipkart orders CRUD operations using OOP"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, order_data: FlipkartOrderCreate) -> FlipkartOrder:
        """Create a new Flipkart order"""
        db_order = FlipkartOrder(**order_data.dict())
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def get_by_id(self, order_id: int) -> Optional[FlipkartOrder]:
        """Get order by ID"""
        return self.db.query(FlipkartOrder).filter(FlipkartOrder.id == order_id).first()
    
    def get_by_order_id(self, order_id: int) -> Optional[FlipkartOrder]:
        """Get order by order_id field"""
        return self.db.query(FlipkartOrder).filter(FlipkartOrder.order_id == order_id).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        customer_id: Optional[str] = None,
        category: Optional[str] = None,
        region: Optional[str] = None,
        city: Optional[str] = None,
        min_sales: Optional[float] = None,
        max_sales: Optional[float] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search: Optional[str] = None
    ) -> tuple[List[FlipkartOrder], int]:
        """Get all orders with filtering and pagination"""
        query = self.db.query(FlipkartOrder)
        
        # Apply filters using functional programming approach
        filters = []
        
        if customer_id:
            filters.append(FlipkartOrder.customer_id == customer_id)
        if category:
            filters.append(FlipkartOrder.category == category)
        if region:
            filters.append(FlipkartOrder.region == region)
        if city:
            filters.append(FlipkartOrder.city == city)
        if min_sales is not None:
            filters.append(FlipkartOrder.sales >= min_sales)
        if max_sales is not None:
            filters.append(FlipkartOrder.sales <= max_sales)
        if start_date:
            filters.append(FlipkartOrder.order_date >= start_date)
        if end_date:
            filters.append(FlipkartOrder.order_date <= end_date)
        if search:
            filters.append(
                or_(
                    FlipkartOrder.product_name.contains(search),
                    FlipkartOrder.customer_name.contains(search)
                )
            )
        
        # Combine filters using and_
        if filters:
            query = query.filter(and_(*filters))
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination and ordering
        orders = query.order_by(desc(FlipkartOrder.order_date)).offset(skip).limit(limit).all()
        
        return orders, total
    
    def get_orders_generator(
        self,
        batch_size: int = 100,
        region: Optional[str] = None
    ) -> Generator[List[FlipkartOrder], None, None]:
        """Get orders in batches using generator for memory efficiency"""
        query = self.db.query(FlipkartOrder)
        
        if region:
            query = query.filter(FlipkartOrder.region == region)
        
        query = query.order_by(desc(FlipkartOrder.order_date))
        
        offset = 0
        while True:
            orders = query.offset(offset).limit(batch_size).all()
            if not orders:
                break
            yield orders
            offset += batch_size
    
    def update(self, order_id: int, order_data: FlipkartOrderUpdate) -> Optional[FlipkartOrder]:
        """Update an order"""
        db_order = self.get_by_id(order_id)
        if not db_order:
            return None
        
        # Use dict comprehension to filter out None values
        update_data = {k: v for k, v in order_data.dict().items() if v is not None}
        
        # Update fields using map for efficiency
        for key, value in update_data.items():
            setattr(db_order, key, value)
        
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def delete(self, order_id: int) -> bool:
        """Delete an order"""
        db_order = self.get_by_id(order_id)
        if not db_order:
            return False
        
        self.db.delete(db_order)
        self.db.commit()
        return True
    
    def bulk_create(self, orders_data: List[FlipkartOrderCreate]) -> List[FlipkartOrder]:
        """Bulk create orders for better performance"""
        db_orders = [FlipkartOrder(**order.dict()) for order in orders_data]
        self.db.add_all(db_orders)
        self.db.commit()
        
        # Refresh objects to get IDs
        for order in db_orders:
            self.db.refresh(order)
        
        return db_orders
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get aggregated statistics using SQL functions"""
        from collections import Counter
        
        # Basic statistics
        total_orders = self.db.query(func.count(FlipkartOrder.id)).scalar() or 0
        total_revenue = self.db.query(func.sum(FlipkartOrder.sales)).scalar() or 0
        total_profit = self.db.query(func.sum(FlipkartOrder.profit)).scalar() or 0
        total_quantity = self.db.query(func.sum(FlipkartOrder.quantity)).scalar() or 0
        avg_discount = self.db.query(func.avg(FlipkartOrder.discount)).scalar() or 0
        
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Orders by region
        region_counts = self.db.query(
            FlipkartOrder.region,
            func.count(FlipkartOrder.id).label('count')
        ).group_by(FlipkartOrder.region).all()
        orders_by_region = {region: count for region, count in region_counts}
        
        # Orders by category
        category_counts = self.db.query(
            FlipkartOrder.category,
            func.count(FlipkartOrder.id).label('count')
        ).group_by(FlipkartOrder.category).all()
        orders_by_category = {category: count for category, count in category_counts}
        
        # Top cities by revenue
        top_cities = self.db.query(
            FlipkartOrder.city,
            func.sum(FlipkartOrder.sales).label('total_sales'),
            func.count(FlipkartOrder.id).label('order_count')
        ).group_by(FlipkartOrder.city).order_by(desc('total_sales')).limit(10).all()
        
        top_cities_list = [
            {"city": city, "total_sales": float(sales), "order_count": count}
            for city, sales, count in top_cities
        ]
        
        return {
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'total_profit': float(total_profit),
            'avg_order_value': float(avg_order_value),
            'total_quantity': int(total_quantity) if total_quantity else 0,
            'avg_discount': float(avg_discount),
            'orders_by_region': orders_by_region,
            'orders_by_category': orders_by_category,
            'top_cities': top_cities_list
        }
    
    def get_by_region(self, region: str) -> List[FlipkartOrder]:
        """Get orders by region using index for fast lookup"""
        return self.db.query(FlipkartOrder).filter(
            FlipkartOrder.region == region
        ).order_by(desc(FlipkartOrder.sales)).all()
    
    def get_by_category(self, category: str) -> List[FlipkartOrder]:
        """Get orders by category"""
        return self.db.query(FlipkartOrder).filter(
            FlipkartOrder.category == category
        ).order_by(desc(FlipkartOrder.sales)).all()
    
    def search_orders(self, search_term: str, limit: int = 50) -> List[FlipkartOrder]:
        """Search orders by product name or customer name"""
        return self.db.query(FlipkartOrder).filter(
            or_(
                FlipkartOrder.product_name.contains(search_term),
                FlipkartOrder.customer_name.contains(search_term)
            )
        ).order_by(desc(FlipkartOrder.order_date)).limit(limit).all()

