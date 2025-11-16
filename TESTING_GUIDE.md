# Testing Guide

## How to Run Tests

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test File
```bash
# Run only authentication tests
python -m pytest tests/test_auth.py -v

# Run only items tests
python -m pytest tests/test_items.py -v
```

### Run Specific Test Function
```bash
# Run a specific test
python -m pytest tests/test_auth.py::test_register_user -v
```

### Run Tests with Coverage
```bash
# Run with coverage report
python -m pytest tests/ --cov=. --cov-report=term-missing

# Generate HTML coverage report
python -m pytest tests/ --cov=. --cov-report=html
# Then open htmlcov/index.html in your browser
```

### Run Tests in Parallel (if pytest-xdist is installed)
```bash
pip install pytest-xdist
python -m pytest tests/ -n auto
```

## Test Configuration

The test configuration is in `pytest.ini`:
- Test paths: `tests/`
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Verbose output: `-v`
- Coverage: Enabled by default

## Test Database

Tests use SQLite in-memory database (`test.db`) for isolation:
- Each test gets a fresh database
- Tables are created before each test
- Tables are dropped after each test
- No interference between tests

## Common Test Commands

### Quick Test Run
```bash
python -m pytest tests/ -v
```

### Run Tests Without Coverage (Faster)
```bash
python -m pytest tests/ -v --no-cov
```

### Run Tests and Stop on First Failure
```bash
python -m pytest tests/ -v -x
```

### Run Tests with Detailed Output
```bash
python -m pytest tests/ -v -s
```

### Run Only Failed Tests (After a failed run)
```bash
python -m pytest tests/ --lf
```

### Run Tests Matching a Pattern
```bash
# Run tests matching "register"
python -m pytest tests/ -k register -v

# Run tests matching "item"
python -m pytest tests/ -k item -v
```

## Test Fixtures

Available fixtures in `tests/conftest.py`:

1. **`db_session`**: Database session for each test
2. **`client`**: FastAPI test client
3. **`test_user`**: Creates a test user
4. **`auth_token`**: JWT token for authenticated requests
5. **`sample_items`**: Sample items for testing

## Writing New Tests

### Example Test Structure
```python
def test_example(client, auth_token):
    """Test description"""
    response = client.get(
        "/api/v1/endpoint",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["key"] == "value"
```

### Test Authentication Endpoints
```python
def test_endpoint_requires_auth(client):
    """Test that endpoint requires authentication"""
    response = client.get("/api/v1/protected")
    assert response.status_code == 401
```

### Test with Database
```python
def test_create_item(db_session, client, auth_token):
    """Test creating an item"""
    from crud import ItemRepository
    from schemas import AmazonItemCreate
    
    item_data = AmazonItemCreate(
        title="Test Item",
        price=99.99,
        category="Electronics"
    )
    
    response = client.post(
        "/api/v1/items",
        json=item_data.dict(),
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 201
    assert response.json()["title"] == "Test Item"
```

## Troubleshooting

### Issue: Index already exists
**Solution**: The test database is cleaned up automatically. If you see this error, delete `test.db`:
```bash
# Windows
del test.db

# Linux/Mac
rm test.db
```

### Issue: Import errors
**Solution**: Make sure all imports are correct in `tests/conftest.py`:
- `UserCreate` from `schemas`
- All models from `models`
- All repositories from `crud`

### Issue: Database connection errors
**Solution**: Tests use SQLite, so no external database is needed. If you see connection errors, check:
1. `test.db` file permissions
2. SQLite is installed (usually comes with Python)

## Test Coverage

Current test coverage can be viewed by:
1. Running tests with coverage: `python -m pytest tests/ --cov=. --cov-report=html`
2. Opening `htmlcov/index.html` in your browser

## Best Practices

1. **Isolation**: Each test should be independent
2. **Cleanup**: Use fixtures for setup and teardown
3. **Naming**: Use descriptive test names
4. **Assertions**: Use specific assertions
5. **Fixtures**: Reuse fixtures for common setup
6. **Mocking**: Mock external services when needed

## Continuous Integration

Tests can be run in CI/CD pipelines:
```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ -v --cov=. --cov-report=xml
```

