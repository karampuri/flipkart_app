"""
Create MySQL database if it doesn't exist
"""
import pymysql
from config_local import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_database():
    """Create MySQL database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            logger.info(f"Database '{settings.DB_NAME}' created or already exists")
        
        connection.close()
        logger.info("Database creation completed successfully")
        
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise


if __name__ == "__main__":
    create_database()

