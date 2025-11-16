# Configuration Guide

## Where to Change DB Configuration and .env File Path

### 1. Database Configuration

Database settings can be configured in **two ways**:

#### Option A: Using .env File (Recommended)

Create a `.env` file in the project root directory (`c:\git_projects\flipkart_app\.env`) with the following content:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=amazon_items_db

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Optional: Use SQLite for local development
USE_SQLITE=false
```

#### Option B: Directly in Config Files

Edit the default values in:
- `config.py` - For production/MySQL setup
- `config_local.py` - For local development with SQLite

**Location in config files:**
```python
# Database settings (lines 15-19 in config.py or config_local.py)
DB_HOST: str = "localhost"
DB_PORT: int = 3306
DB_USER: str = "root"
DB_PASSWORD: str = ""
DB_NAME: str = "amazon_items_db"
```

### 2. Changing .env File Path

The `.env` file path can be customized in **three ways**:

#### Method 1: Environment Variable (Recommended)

Set the `ENV_FILE` environment variable before running the application:

**Windows (PowerShell):**
```powershell
$env:ENV_FILE="C:\path\to\your\.env"
python run.py
```

**Windows (Command Prompt):**
```cmd
set ENV_FILE=C:\path\to\your\.env
python run.py
```

**Linux/Mac:**
```bash
export ENV_FILE=/path/to/your/.env
python run.py
```

#### Method 2: Modify Config Files Directly

Edit `config.py` or `config_local.py`:

**Line 8-10:**
```python
# Change this line:
env_file_path = os.getenv("ENV_FILE", ".env")  # Default: ".env"
# To:
env_file_path = os.getenv("ENV_FILE", "/path/to/your/.env")
```

**Line 36 (in Config class):**
```python
class Config:
    env_file = os.getenv("ENV_FILE", "/path/to/your/.env")  # Change here
    case_sensitive = True
```

#### Method 3: Absolute Path in load_dotenv()

Edit `config.py` or `config_local.py`:

**Line 10:**
```python
# Change from:
load_dotenv(env_file_path)
# To:
load_dotenv("/absolute/path/to/your/.env")
```

### 3. Configuration File Priority

The application uses the following priority order:

1. **Environment variables** (highest priority)
2. **Values from .env file**
3. **Default values in config files** (lowest priority)

### 4. Quick Setup Steps

1. **Copy the example file:**
   ```bash
   copy .env.example .env
   ```

2. **Edit `.env` file** with your MySQL credentials:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=amazon_items_db
   ```

3. **Generate a secure SECRET_KEY:**
   ```bash
   # Windows (PowerShell)
   [Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
   
   # Linux/Mac
   openssl rand -hex 32
   ```

4. **Update SECRET_KEY in .env:**
   ```env
   SECRET_KEY=your-generated-secret-key-here
   ```

### 5. File Locations Summary

| File | Purpose | Location |
|------|---------|----------|
| `.env` | Your actual configuration (create this) | `c:\git_projects\flipkart_app\.env` |
| `.env.example` | Template/example file | `c:\git_projects\flipkart_app\.env.example` |
| `config.py` | Production config (MySQL) | `c:\git_projects\flipkart_app\config.py` |
| `config_local.py` | Local config (SQLite) | `c:\git_projects\flipkart_app\config_local.py` |

### 6. Important Notes

- **Never commit `.env` file** to version control (it's in `.gitignore`)
- Always use `.env.example` as a template
- For production, use environment variables or a secure secrets manager
- The `.env` file should be in the **project root directory** by default

### 7. Troubleshooting

**If .env file is not being loaded:**
1. Check the file path is correct
2. Verify the file exists: `dir .env` (Windows) or `ls -la .env` (Linux/Mac)
3. Check file permissions
4. Verify you're running from the project root directory

**To verify which config is being used:**
```python
from config import settings
print(f"Database URL: {settings.database_url}")
print(f"DB Host: {settings.DB_HOST}")
```

