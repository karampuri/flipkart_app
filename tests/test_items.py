"""
Tests for items CRUD endpoints
"""
import pytest
from fastapi import status


def test_create_item(client, auth_token):
    """Test creating an item"""
    response = client.post(
        "/api/v1/items",
        json={
            "title": "New Item",
            "price": 99.99,
            "rating": 4.5,
            "reviews_count": 100,
            "category": "Electronics",
            "subcategory": "Laptops",
            "brand": "TestBrand",
            "description": "A new test item"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "New Item"
    assert data["price"] == 99.99
    assert "id" in data


def test_create_item_no_auth(client):
    """Test creating item without authentication"""
    response = client.post(
        "/api/v1/items",
        json={
            "title": "New Item",
            "price": 99.99,
            "category": "Electronics"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_items(client, auth_token, sample_items):
    """Test getting all items"""
    response = client.get(
        "/api/v1/items",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert len(data["items"]) >= 2


def test_get_items_with_pagination(client, auth_token, sample_items):
    """Test getting items with pagination"""
    response = client.get(
        "/api/v1/items?page=1&page_size=1",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    assert data["page"] == 1
    assert data["page_size"] == 1


def test_get_items_with_filters(client, auth_token, sample_items):
    """Test getting items with filters"""
    response = client.get(
        "/api/v1/items?category=Electronics&min_price=500",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    for item in data["items"]:
        assert item["category"] == "Electronics"
        assert item["price"] >= 500


def test_get_item_by_id(client, auth_token, sample_items):
    """Test getting item by ID"""
    item_id = sample_items[0].id
    response = client.get(
        f"/api/v1/items/{item_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == item_id


def test_get_item_not_found(client, auth_token):
    """Test getting non-existent item"""
    response = client.get(
        "/api/v1/items/99999",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_item(client, auth_token, sample_items):
    """Test updating an item"""
    item_id = sample_items[0].id
    response = client.put(
        f"/api/v1/items/{item_id}",
        json={
            "title": "Updated Title",
            "price": 1299.99
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["price"] == 1299.99


def test_update_item_not_found(client, auth_token):
    """Test updating non-existent item"""
    response = client.put(
        "/api/v1/items/99999",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_item(client, auth_token, sample_items):
    """Test deleting an item"""
    item_id = sample_items[0].id
    response = client.delete(
        f"/api/v1/items/{item_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    
    # Verify item is deleted
    get_response = client.get(
        f"/api/v1/items/{item_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_item_not_found(client, auth_token):
    """Test deleting non-existent item"""
    response = client.delete(
        "/api/v1/items/99999",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_bulk_create_items(client, auth_token):
    """Test bulk creating items"""
    items_data = [
        {
            "title": f"Bulk Item {i}",
            "price": 10.0 + i,
            "category": "Electronics",
            "subcategory": "Laptops"
        }
        for i in range(5)
    ]
    
    response = client.post(
        "/api/v1/items/bulk",
        json=items_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert len(data) == 5


def test_get_statistics(client, auth_token, sample_items):
    """Test getting statistics"""
    response = client.get(
        "/api/v1/items/statistics",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_items" in data
    assert "avg_price" in data
    assert "min_price" in data
    assert "max_price" in data
    assert "avg_rating" in data


def test_search_items(client, auth_token, sample_items):
    """Test searching items"""
    response = client.get(
        "/api/v1/items/search?q=Laptop",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


def test_get_items_by_category(client, auth_token, sample_items):
    """Test getting items by category"""
    response = client.get(
        "/api/v1/items/category/Electronics",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert item["category"] == "Electronics"

