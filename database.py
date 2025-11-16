"""
Database connection and session management
Uses connection pooling for optimal performance
"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import logging

try:
    from config_local import settings
except ImportError:
    from config import settings

logger = logging.getLogger(__name__)

# Create engine with connection pooling for better performance
# Use StaticPool for SQLite, QueuePool for MySQL
if settings.USE_MYSQL:
    # MySQL connection with connection pooling
    engine = create_engine(
        settings.database_url,
        poolclass=QueuePool,
        pool_size=10,  # Number of connections to maintain
        max_overflow=20,  # Maximum overflow connections
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,  # Recycle connections after 1 hour
        echo=False,  # Set to True for SQL query logging
        future=True
    )
    logger.info(f"Using MySQL database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
else:
    # SQLite connection (no pooling needed)
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=None,  # SQLite doesn't need pooling
        echo=False,
        future=True
    )
    logger.info(f"Using SQLite database: {settings.SQLITE_DB_PATH}")

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Base class for models
Base = declarative_base()


@event.listens_for(engine, "connect")
def set_mysql_params(dbapi_conn, connection_record):
    """Set MySQL connection parameters for optimal performance"""
    try:
        with dbapi_conn.cursor() as cursor:
            cursor.execute("SET SESSION sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO'")
            cursor.execute("SET SESSION innodb_lock_wait_timeout=50")
    except Exception:
        # Ignore errors for non-MySQL databases (e.g., SQLite in tests)
        pass


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session
    Uses generator pattern for automatic cleanup
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database sessions
    Alternative to dependency injection for non-FastAPI contexts
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


def close_db():
    """Close database connections"""
    engine.dispose()
    logger.info("Database connections closed")

