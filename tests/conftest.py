"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from models import User, AmazonItem
from auth import AuthenticationService
from crud import UserRepository
from schemas import UserCreate

# Test database URL (using SQLite in-memory for testing)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    # Drop all tables first to ensure clean state
    Base.metadata.drop_all(bind=test_engine)
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Clean up after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session):
    """Create a test user"""
    user_repo = UserRepository(db_session)
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    hashed_password = AuthenticationService.get_password_hash(user_data["password"])
    user = user_repo.create(
        UserCreate(**user_data),
        hashed_password
    )
    return user, user_data["password"]


@pytest.fixture(scope="function")
def auth_token(client, test_user):
    """Get authentication token for test user"""
    user, password = test_user
    response = client.post(
        "/api/v1/auth/login",
        data={"username": user.username, "password": password}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def sample_items(db_session):
    """Create sample items for testing"""
    from crud import ItemRepository
    from schemas import AmazonItemCreate
    
    item_repo = ItemRepository(db_session)
    
    items_data = [
        AmazonItemCreate(
            title="Test Laptop",
            price=999.99,
            rating=4.5,
            reviews_count=100,
            category="Electronics",
            subcategory="Laptops",
            brand="TestBrand",
            description="A test laptop"
        ),
        AmazonItemCreate(
            title="Test Book",
            price=19.99,
            rating=4.0,
            reviews_count=50,
            category="Books",
            subcategory="Fiction",
            brand="TestPublisher",
            description="A test book"
        ),
    ]
    
    return item_repo.bulk_create(items_data)

