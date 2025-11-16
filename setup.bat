@echo off
echo ========================================
echo FastAPI Amazon Items API - Setup Script
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Setup complete!
echo.
echo Next steps:
echo 1. Create MySQL database: CREATE DATABASE amazon_items_db;
echo 2. Copy .env.example to .env and configure it
echo 3. Run: python setup_database.py
echo 4. Run: python seed_data.py
echo 5. Run: python run.py
echo.
echo To activate virtual environment later, run: venv\Scripts\activate.bat
echo.
pause

