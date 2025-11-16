# Project Structure

```
flipkart_app/
│
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management (environment variables)
├── database.py            # Database connection, session management, connection pooling
├── models.py              # SQLAlchemy ORM models (User, AmazonItem)
├── schemas.py             # Pydantic schemas for request/response validation
├── auth.py                # JWT authentication utilities and dependencies
├── crud.py                # CRUD operations with performance optimizations
├── seed_data.py           # Database seeding script with sample Amazon items
├── setup_database.py      # Database initialization script
├── run.py                 # Simple script to run the application
│
├── routers/               # API route handlers
│   ├── __init__.py
│   ├── auth.py           # Authentication routes (register, login, me)
│   └── items.py          # Items CRUD routes
│
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── conftest.py       # Pytest fixtures and configuration
│   ├── test_auth.py      # Authentication endpoint tests
│   └── test_items.py     # Items CRUD endpoint tests
│
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # Comprehensive documentation
├── QUICKSTART.md         # Quick start guide
└── PROJECT_STRUCTURE.md  # This file
```

## Key Features Implemented

### Performance Optimizations
- ✅ Connection pooling for database connections
- ✅ Generators for memory-efficient batch processing
- ✅ Bulk operations for better performance
- ✅ Database indexes on frequently queried columns
- ✅ Async/await for non-blocking operations
- ✅ Efficient query filtering using SQLAlchemy

### Advanced Python Concepts
- ✅ OOP: Repository pattern, service classes
- ✅ Generators: Memory-efficient data processing
- ✅ Map/Filter: Functional programming patterns
- ✅ Context managers: Resource management
- ✅ Type hints: Full type annotations
- ✅ Dependency injection: FastAPI's dependency system

### Security
- ✅ JWT token-based authentication
- ✅ Password hashing with bcrypt
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Token expiration

### Testing
- ✅ Comprehensive test suite with pytest
- ✅ Test fixtures for database and authentication
- ✅ Coverage reporting
- ✅ Unit tests for all endpoints

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Items (Protected)
- `POST /api/v1/items` - Create item
- `POST /api/v1/items/bulk` - Bulk create items
- `GET /api/v1/items` - List items (paginated, filtered)
- `GET /api/v1/items/{id}` - Get item by ID
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item
- `GET /api/v1/items/statistics` - Get statistics
- `GET /api/v1/items/search?q={query}` - Search items
- `GET /api/v1/items/category/{category}` - Get by category
- `GET /api/v1/items/stream` - Stream items in batches

## Database Schema

### Users Table
- id (PK)
- username (unique, indexed)
- email (unique, indexed)
- hashed_password
- is_active
- created_at
- updated_at

### Amazon Items Table
- id (PK)
- title (indexed)
- price (indexed)
- rating (indexed)
- reviews_count
- category (indexed)
- subcategory (indexed)
- brand
- description
- image_url
- product_url
- availability
- seller
- created_at
- updated_at

## Technology Stack

- **Framework**: FastAPI 0.104.1
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic
- **Testing**: pytest, pytest-asyncio, httpx
- **Server**: Uvicorn

