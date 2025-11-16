# FastAPI Amazon Items API

A high-performance FastAPI application with JWT authentication, MySQL database, and optimized CRUD operations. This project demonstrates advanced Python concepts including OOP, generators, async/await, and efficient database operations.

## Features

- 🔐 JWT-based authentication
- 🗄️ MySQL database with connection pooling
- ⚡ Optimized CRUD operations using generators, map, filter
- 🧪 Comprehensive test suite with pytest
- 📊 Bulk operations for better performance
- 🔍 Advanced filtering and search capabilities
- 📈 Statistics and aggregation endpoints
- 🚀 Async/await for non-blocking operations

## Project Structure

```
flipkart_app/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── database.py            # Database connection and session management
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas for validation
├── auth.py                # JWT authentication utilities
├── crud.py                # CRUD operations with optimizations
├── seed_data.py           # Database seeding script
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
├── .env.example          # Environment variables template
├── routers/
│   ├── __init__.py
│   ├── auth.py           # Authentication routes
│   └── items.py          # Items CRUD routes
└── tests/
    ├── __init__.py
    ├── conftest.py       # Pytest fixtures
    ├── test_auth.py      # Authentication tests
    └── test_items.py     # Items CRUD tests
```

## Prerequisites

- Python 3.8+
- MySQL 5.7+ or MySQL 8.0+ (optional - SQLite is used by default for local development)
- pip (Python package manager)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd flipkart_app
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your database configuration:

**For MySQL:**
```env
USE_MYSQL=true
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=your_db

SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

HOST=0.0.0.0
PORT=8000
```

**For SQLite (Local Development - Default):**
```env
USE_MYSQL=false
# MySQL settings are ignored when USE_MYSQL=false

SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

HOST=0.0.0.0
PORT=8000
```

**Important:** Generate a secure SECRET_KEY:
```bash
# Using OpenSSL
openssl rand -hex 32
```

### 5. Create MySQL Database (Only if using MySQL)

If you set `USE_MYSQL=true` in your `.env` file, create the MySQL database:

```sql
CREATE DATABASE amazon_items_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Note:** If using SQLite (default), skip this step. SQLite database will be created automatically.

### 6. Seed the Database

Run the seed script to populate the database with sample Amazon items:

```bash
python seed_data.py
```

This will create:
- An admin user (username: `admin`, password: `admin123`)
- Sample Amazon items across multiple categories

### 7. Run the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs (Swagger): http://localhost:8000/docs
- Alternative Docs (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user information

### Items (Requires Authentication)

- `POST /api/v1/items` - Create a new item
- `POST /api/v1/items/bulk` - Bulk create items
- `GET /api/v1/items` - Get all items (with pagination and filters)
- `GET /api/v1/items/{item_id}` - Get item by ID
- `PUT /api/v1/items/{item_id}` - Update an item
- `DELETE /api/v1/items/{item_id}` - Delete an item
- `GET /api/v1/items/statistics` - Get aggregated statistics
- `GET /api/v1/items/search?q={query}` - Search items
- `GET /api/v1/items/category/{category}` - Get items by category
- `GET /api/v1/items/stream` - Stream items in batches

## Usage Examples

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### 3. Create an Item

```bash
curl -X POST "http://localhost:8000/api/v1/items" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Wireless Headphones",
    "price": 79.99,
    "rating": 4.5,
    "reviews_count": 250,
    "category": "Electronics",
    "subcategory": "Headphones",
    "brand": "Sony",
    "description": "High-quality wireless headphones"
  }'
```

### 4. Get Items with Filters

```bash
curl -X GET "http://localhost:8000/api/v1/items?category=Electronics&min_price=100&page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Search Items

```bash
curl -X GET "http://localhost:8000/api/v1/items/search?q=laptop&limit=20" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Running Tests

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=. --cov-report=html
```

Run specific test file:

```bash
pytest tests/test_auth.py
pytest tests/test_items.py
```

Run with verbose output:

```bash
pytest -v
```

## Performance Optimizations

This project implements several performance optimizations:

1. **Connection Pooling**: Database connections are pooled for reuse
2. **Generators**: Used for memory-efficient batch processing
3. **Bulk Operations**: Bulk insert/update for better performance
4. **Database Indexes**: Strategic indexes on frequently queried columns
5. **Async Operations**: Non-blocking I/O operations
6. **Query Optimization**: Efficient SQL queries with proper filtering
7. **Lazy Loading**: Optimized relationship loading

## Advanced Concepts Used

- **OOP**: Repository pattern, service classes
- **Generators**: Memory-efficient data processing
- **Map/Filter**: Functional programming for data transformation
- **Async/Await**: Non-blocking operations
- **Context Managers**: Resource management
- **Dependency Injection**: FastAPI's dependency system
- **Type Hints**: Full type annotations
- **Pydantic Models**: Data validation and serialization

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Token expiration
- Input validation
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration

## Database Schema

### Users Table
- id (Primary Key)
- username (Unique, Indexed)
- email (Unique, Indexed)
- hashed_password
- is_active
- created_at
- updated_at

### Amazon Items Table
- id (Primary Key)
- title (Indexed)
- price (Indexed)
- rating (Indexed)
- reviews_count
- category (Indexed)
- subcategory (Indexed)
- brand
- description
- image_url
- product_url
- availability
- seller
- created_at
- updated_at

## Troubleshooting

### Database Connection Issues

1. Verify MySQL is running:
```bash
# Windows
net start MySQL

# Linux
sudo systemctl status mysql
```

2. Check database credentials in `.env` file
3. Ensure database exists: `CREATE DATABASE amazon_items_db;`

### Import Errors

Make sure you're in the virtual environment and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port Already in Use

Change the port in `.env` or use a different port:
```bash
uvicorn main:app --reload --port 8001
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on the GitHub repository.

---

**Note**: Remember to change the default admin password and SECRET_KEY in production!
