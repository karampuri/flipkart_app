# Flipkart Orders CRUD API Documentation

## Overview
Complete CRUD (Create, Read, Update, Delete) endpoints for Flipkart orders have been created and integrated into the FastAPI application.

## Database Tables

### Tables Created in MySQL Database (`test`)

1. **users** - User authentication table
2. **amazon_items** - Amazon items CRUD operations
3. **flipkart_orders** - Flipkart sales orders (with 12 orders imported)

## API Endpoints

### Orders Endpoints (All require JWT authentication)

#### 1. Create Order
- **POST** `/api/v1/orders`
- **Description**: Create a new Flipkart order
- **Request Body**: `FlipkartOrderCreate` schema
- **Response**: `FlipkartOrderResponse`

#### 2. Bulk Create Orders
- **POST** `/api/v1/orders/bulk`
- **Description**: Create multiple orders at once (max 1000)
- **Request Body**: Array of `FlipkartOrderCreate`
- **Response**: Array of `FlipkartOrderResponse`

#### 3. Get All Orders
- **GET** `/api/v1/orders`
- **Description**: Get paginated list of orders with filtering
- **Query Parameters**:
  - `page` (int): Page number (default: 1)
  - `page_size` (int): Items per page (default: 10, max: 100)
  - `customer_id` (str, optional): Filter by customer ID
  - `category` (str, optional): Filter by category
  - `region` (str, optional): Filter by region
  - `city` (str, optional): Filter by city
  - `min_sales` (float, optional): Minimum sales amount
  - `max_sales` (float, optional): Maximum sales amount
  - `start_date` (datetime, optional): Start date filter
  - `end_date` (datetime, optional): End date filter
  - `search` (str, optional): Search in product name or customer name
- **Response**: `FlipkartOrderListResponse` (paginated)

#### 4. Get Order by ID
- **GET** `/api/v1/orders/{order_id}`
- **Description**: Get a specific order by its ID
- **Response**: `FlipkartOrderResponse`

#### 5. Update Order
- **PUT** `/api/v1/orders/{order_id}`
- **Description**: Update an existing order
- **Request Body**: `FlipkartOrderUpdate` schema (all fields optional)
- **Response**: `FlipkartOrderResponse`

#### 6. Delete Order
- **DELETE** `/api/v1/orders/{order_id}`
- **Description**: Delete an order
- **Response**: `MessageResponse`

#### 7. Get Orders by Region
- **GET** `/api/v1/orders/region/{region}`
- **Description**: Get all orders for a specific region
- **Response**: Array of `FlipkartOrderResponse`

#### 8. Get Orders by Category
- **GET** `/api/v1/orders/category/{category}`
- **Description**: Get all orders for a specific category
- **Response**: Array of `FlipkartOrderResponse`

#### 9. Search Orders
- **GET** `/api/v1/orders/search?q={query}`
- **Description**: Search orders by product name or customer name
- **Query Parameters**:
  - `q` (str, required): Search query
  - `limit` (int, optional): Maximum results (default: 50, max: 100)
- **Response**: Array of `FlipkartOrderResponse`

#### 10. Get Order Statistics
- **GET** `/api/v1/orders/statistics`
- **Description**: Get aggregated statistics for all orders
- **Response**: `FlipkartOrderStatistics` containing:
  - Total orders
  - Total revenue
  - Total profit
  - Average order value
  - Total quantity
  - Average discount
  - Orders by region
  - Orders by category
  - Top cities by revenue

#### 11. Stream Orders
- **GET** `/api/v1/orders/stream`
- **Description**: Stream orders in batches using generator for memory efficiency
- **Query Parameters**:
  - `batch_size` (int, optional): Batch size (default: 100, max: 500)
  - `region` (str, optional): Filter by region
- **Response**: Array of `FlipkartOrderResponse` (first batch)

## Data Models

### FlipkartOrder Model
- `id` (int, PK): Primary key
- `order_id` (int, unique): Unique order identifier
- `order_date` (datetime): Order date
- `customer_id` (str): Customer identifier
- `customer_name` (str): Customer name
- `segment` (str): Customer segment
- `city` (str): City
- `state` (str): State
- `country` (str): Country (default: "India")
- `region` (str): Region
- `product_id` (str): Product identifier
- `category` (str): Product category
- `subcategory` (str): Product subcategory
- `product_name` (str): Product name
- `sales` (float): Sales amount
- `quantity` (int): Quantity ordered
- `discount` (float): Discount percentage
- `profit` (float): Profit amount
- `created_at` (datetime): Record creation timestamp
- `updated_at` (datetime): Record update timestamp

## Database Indexes

The `flipkart_orders` table has the following indexes for optimal performance:
- `idx_order_id`: On `order_id` (unique)
- `idx_order_date`: On `order_date`
- `idx_customer_id`: On `customer_id`
- `idx_product_id`: On `product_id`
- `idx_category`: On `category`
- `idx_region`: On `region`
- `idx_city`: On `city`
- `idx_order_date_region`: Composite on `order_date` and `region`
- `idx_category_sales`: Composite on `category` and `sales`

## Implementation Details

### Repository Pattern
- `FlipkartOrderRepository` class in `crud.py` handles all database operations
- Uses OOP principles for code organization
- Implements generators for memory-efficient batch processing

### Performance Optimizations
- Database indexes on frequently queried columns
- Bulk operations for creating multiple orders
- Generator-based streaming for large datasets
- Efficient query filtering using SQLAlchemy
- Connection pooling for MySQL

### Advanced Python Concepts Used
- **OOP**: Repository pattern with class-based CRUD operations
- **Generators**: `get_orders_generator()` for memory-efficient batch processing
- **Map/Filter**: Functional programming patterns in query filtering
- **Type Hints**: Full type annotations throughout
- **Context Managers**: Database session management

## Current Data

- **Total Orders**: 12 orders imported from `flipkart_sales.csv`
- **Total Revenue**: ₹550,495.00
- **Total Profit**: ₹60,000.00

## Testing the API

1. **Start the server**:
   ```bash
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **Access Swagger UI**: http://127.0.0.1:8000/docs

3. **Authenticate**:
   - Register a user: `POST /api/v1/auth/register`
   - Login: `POST /api/v1/auth/login`
   - Copy the access token

4. **Authorize in Swagger**:
   - Click "Authorize" button
   - Enter: `Bearer {your_access_token}`
   - Click "Authorize"

5. **Test Orders Endpoints**:
   - All orders endpoints are now available under the "Orders" section
   - Try `GET /api/v1/orders` to see all orders
   - Try `GET /api/v1/orders/statistics` to see aggregated statistics

## Files Created/Modified

### New Files
- `routers/orders.py`: Orders CRUD endpoints
- `ORDERS_API_DOCUMENTATION.md`: This documentation file

### Modified Files
- `schemas.py`: Added Flipkart order schemas
- `crud.py`: Added `FlipkartOrderRepository` class
- `main.py`: Registered orders router
- `models.py`: Already had `FlipkartOrder` model (created earlier)

## Example Usage

### Create an Order
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/orders" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1001,
    "order_date": "2024-01-15T10:00:00",
    "customer_id": "C001",
    "customer_name": "John Doe",
    "segment": "Consumer",
    "city": "Mumbai",
    "state": "Maharashtra",
    "region": "West",
    "product_id": "P001",
    "category": "Electronics",
    "subcategory": "Mobile",
    "product_name": "Smartphone",
    "sales": 25000.0,
    "quantity": 1,
    "discount": 0.1,
    "profit": 5000.0
  }'
```

### Get Orders with Filters
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/orders?region=West&category=Electronics&page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Statistics
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/orders/statistics" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

