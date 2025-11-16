"""
Script to set up the database
Run this after creating the MySQL database
"""
from database import init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("Initializing database tables...")
        init_db()
        logger.info("Database tables created successfully!")
        logger.info("You can now run 'python seed_data.py' to populate the database with sample data.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        logger.error("Please make sure:")
        logger.error("1. MySQL is running")
        logger.error("2. Database exists (CREATE DATABASE amazon_items_db;)")
        logger.error("3. .env file is configured with correct credentials")

