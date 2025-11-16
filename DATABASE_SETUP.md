# Database Configuration Guide

## USE_MYSQL Setting

The project now uses `USE_MYSQL` flag to control which database to use.

### Configuration Options

#### Option 1: Use MySQL Database

In your `.env` file, set:
```env
USE_MYSQL=true
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=amazon_items_db
```

#### Option 2: Use SQLite Database (Default for Local Development)

In your `.env` file, set:
```env
USE_MYSQL=false
# Or simply omit the USE_MYSQL line (defaults to false)
```

SQLite database will be created at: `./local_db.sqlite`

### How It Works

1. **When `USE_MYSQL=true`:**
   - Uses MySQL database with connection pooling
   - Requires MySQL server to be running
   - Uses settings: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

2. **When `USE_MYSQL=false` (default):**
   - Uses SQLite database (file-based)
   - No server required
   - Database file: `./local_db.sqlite`

### Example .env File

**For MySQL:**
```env
# Database Type Selection
USE_MYSQL=true

# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=amazon_items_db

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**For SQLite (Local Development):**
```env
# Database Type Selection
USE_MYSQL=false

# MySQL Database Configuration (not used when USE_MYSQL=false)
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=amazon_items_db

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### Setup Steps

#### For MySQL:

1. **Create MySQL Database:**
   ```sql
   CREATE DATABASE amazon_items_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Update .env file:**
   ```env
   USE_MYSQL=true
   DB_PASSWORD=your_mysql_password
   ```

3. **Initialize database:**
   ```bash
   python setup_database.py
   ```

4. **Seed sample data:**
   ```bash
   python seed_data.py
   ```

#### For SQLite:

1. **Update .env file:**
   ```env
   USE_MYSQL=false
   ```

2. **Initialize database:**
   ```bash
   python setup_database.py
   ```

3. **Seed sample data:**
   ```bash
   python seed_data.py
   ```

### Code Changes

The following files have been updated to support `USE_MYSQL`:

1. **config.py** - Production configuration
2. **config_local.py** - Local development configuration
3. **database.py** - Database connection logic

### Verification

To verify which database is being used, check the application logs on startup:
- MySQL: `Using MySQL database: localhost:3306/amazon_items_db`
- SQLite: `Using SQLite database: ./local_db.sqlite`

Or check programmatically:
```python
from config import settings
print(f"Using MySQL: {settings.USE_MYSQL}")
print(f"Database URL: {settings.database_url}")
```

