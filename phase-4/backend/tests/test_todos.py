"""Todo CRUD endpoint tests."""
import pytest
from fastapi import status


class TestTodoList:
    """Tests for listing todos."""

    def test_list_todos_authenticated(self, client, auth_headers, test_todo):
        """Test listing todos returns user's tasks."""
        response = client.get("/todos", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        todos = response.json()
        assert isinstance(todos, list)
        assert len(todos) >= 1

    def test_list_todos_unauthenticated(self, client):
        """Test listing todos without auth returns 401."""
        response = client.get("/todos")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_todos_empty(self, client, db, auth_headers):
        """Test listing todos when user has none."""
        # Create a new user with no todos
        from src.core.security import hash_password
        from src.models.user import User

        empty_user = User(email="empty@example.com", password_hash=hash_password("password123"))
        db.add(empty_user)
        db.commit()

        # Generate token manually
        from src.core.security import create_access_token
        empty_token = create_access_token(data={"sub": empty_user.id, "email": empty_user.email})
        empty_headers = {"Authorization": f"Bearer {empty_token}"}

        response = client.get("/todos", headers=empty_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []


class TestTodoCreate:
    """Tests for creating todos."""

    def test_create_todo(self, client, auth_headers):
        """Test creating a new todo."""
        response = client.post(
            "/todos",
            json={"title": "New Todo", "description": "New Description"},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "New Todo"
        assert data["description"] == "New Description"
        assert data["completed"] is False

    def test_create_todo_minimal(self, client, auth_headers):
        """Test creating a todo with only title."""
        response = client.post(
            "/todos",
            json={"title": "Minimal Todo"},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Minimal Todo"
        assert data["description"] is None

    def test_create_todo_empty_title(self, client, auth_headers):
        """Test creating a todo with empty title returns 422."""
        response = client.post(
            "/todos",
            json={"title": ""},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_todo_unauthenticated(self, client):
        """Test creating a todo without auth returns 401."""
        response = client.post(
            "/todos",
            json={"title": "New Todo"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTodoGet:
    """Tests for getting a specific todo."""

    def test_get_todo(self, client, auth_headers, test_todo):
        """Test getting a specific todo."""
        response = client.get(f"/todos/{test_todo.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_todo.id
        assert data["title"] == "Test Todo"

    def test_get_todo_not_found(self, client, auth_headers):
        """Test getting a non-existent todo returns 404."""
        response = client.get(
            "/todos/00000000-0000-0000-0000-000000000000",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_todo_unauthenticated(self, client, test_todo):
        """Test getting a todo without auth returns 401."""
        response = client.get(f"/todos/{test_todo.id}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTodoUpdate:
    """Tests for updating todos."""

    def test_update_todo_patch(self, client, auth_headers, test_todo):
        """Test partially updating a todo."""
        response = client.patch(
            f"/todos/{test_todo.id}",
            json={"title": "Updated Title", "completed": True},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["completed"] is True

    def test_update_todo_put(self, client, auth_headers, test_todo):
        """Test replacing a todo."""
        response = client.put(
            f"/todos/{test_todo.id}",
            json={"title": "Replaced Title", "description": "New desc", "completed": False},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Replaced Title"
        assert data["completed"] is False

    def test_update_todo_not_found(self, client, auth_headers):
        """Test updating a non-existent todo returns 404."""
        response = client.patch(
            "/todos/00000000-0000-0000-0000-000000000000",
            json={"title": "Updated"},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_todo_unauthenticated(self, client, test_todo):
        """Test updating a todo without auth returns 401."""
        response = client.patch(
            f"/todos/{test_todo.id}",
            json={"title": "Updated"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTodoDelete:
    """Tests for deleting todos."""

    def test_delete_todo(self, client, auth_headers, test_todo):
        """Test deleting a todo returns 204."""
        response = client.delete(f"/todos/{test_todo.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify todo is deleted
        get_response = client.get(f"/todos/{test_todo.id}", headers=auth_headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_todo_not_found(self, client, auth_headers):
        """Test deleting a non-existent todo returns 404."""
        response = client.delete(
            "/todos/00000000-0000-0000-0000-000000000000",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_todo_unauthenticated(self, client, test_todo):
        """Test deleting a todo without auth returns 401."""
        response = client.delete(f"/todos/{test_todo.id}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
