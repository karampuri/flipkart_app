"""
Local configuration for testing without MySQL
Uses SQLite for easier local development
"""
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load .env file from project root (or specify custom path)
# To use a different .env file path, change this line:
# load_dotenv("/path/to/your/.env")
# Or set ENV_FILE environment variable
env_file_path = os.getenv("ENV_FILE", ".env")
load_dotenv(env_file_path)


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database type selection
    # Set USE_MYSQL=true in .env to use MySQL, false (or omit) to use SQLite
    USE_MYSQL: bool = False  # Default to SQLite for local development
    
    # MySQL Database settings (used when USE_MYSQL=True)
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "amazon_items_db"
    
    # SQLite Database settings (used when USE_MYSQL=False)
    SQLITE_DB_PATH: str = "./local_db.sqlite"
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production-local-dev-key-12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    @property
    def database_url(self) -> str:
        """Construct database URL for SQLAlchemy"""
        if self.USE_MYSQL:
            # URL encode password to handle special characters
            from urllib.parse import quote_plus
            encoded_password = quote_plus(str(self.DB_PASSWORD))
            return f"mysql+pymysql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        else:
            return f"sqlite:///{self.SQLITE_DB_PATH}"
    
    class Config:
        # Change this to use a different .env file path
        # Example: env_file = "/path/to/your/.env"
        env_file = os.getenv("ENV_FILE", ".env")
        case_sensitive = True


# Global settings instance
settings = Settings()

