# Quick Start Guide

## Prerequisites
- Python 3.8+
- MySQL 5.7+ or 8.0+
- pip

## Step-by-Step Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create MySQL Database
```sql
CREATE DATABASE amazon_items_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure Environment
Create `.env` file from `.env.example`:
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your MySQL credentials
```

### 4. Initialize Database Tables
```bash
python setup_database.py
```

### 5. Seed Sample Data
```bash
python seed_data.py
```

This creates:
- Admin user: `admin` / `admin123`
- Sample Amazon items

### 6. Run the Application
```bash
python run.py
```

Or:
```bash
uvicorn main:app --reload
```

### 7. Access the API
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Quick Test

### Get Access Token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### Get Items (use token from above)
```bash
curl -X GET "http://localhost:8000/api/v1/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Run Tests
```bash
pytest
```

## Troubleshooting

**Database Connection Error:**
- Check MySQL is running
- Verify `.env` credentials
- Ensure database exists

**Import Errors:**
- Activate virtual environment
- Run `pip install -r requirements.txt`

**Port Already in Use:**
- Change PORT in `.env`
- Or use: `uvicorn main:app --port 8001`

