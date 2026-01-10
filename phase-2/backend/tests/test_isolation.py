"""User isolation and security tests."""
import pytest
from fastapi import status
from src.core.security import create_access_token
from src.models.user import User
from src.models.todo import TodoTask


class TestUserIsolation:
    """Tests for user data isolation (CRITICAL SECURITY)."""

    def test_user_cannot_access_others_todos_list(
        self, client, db, test_user, auth_headers
    ):
        """Test that User A cannot see User B's todos in list."""
        # Create another user with a todo
        from src.core.security import hash_password

        user_b = User(email="userb@example.com", password_hash=hash_password("password123"))
        db.add(user_b)
        db.commit()
        db.refresh(user_b)

        todo_b = TodoTask(user_id=user_b.id, title="User B's Todo")
        db.add(todo_b)
        db.commit()

        # User A lists todos - should NOT see User B's todo
        response = client.get("/todos", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        todos = response.json()
        todo_ids = [t["id"] for t in todos]
        assert todo_b.id not in todo_ids

    def test_user_cannot_access_others_todo_by_id(
        self, client, db, test_user, auth_headers
    ):
        """Test that User A cannot access User B's specific todo."""
        from src.core.security import hash_password

        user_b = User(email="userb@example.com", password_hash=hash_password("password123"))
        db.add(user_b)
        db.commit()
        db.refresh(user_b)

        todo_b = TodoTask(user_id=user_b.id, title="User B's Private Todo")
        db.add(todo_b)
        db.commit()

        # User A tries to get User B's todo by ID
        response = client.get(f"/todos/{todo_b.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_cannot_update_others_todo(
        self, client, db, test_user, auth_headers
    ):
        """Test that User A cannot update User B's todo."""
        from src.core.security import hash_password

        user_b = User(email="userb@example.com", password_hash=hash_password("password123"))
        db.add(user_b)
        db.commit()
        db.refresh(user_b)

        todo_b = TodoTask(user_id=user_b.id, title="User B's Todo")
        db.add(todo_b)
        db.commit()

        # User A tries to update User B's todo
        response = client.patch(
            f"/todos/{todo_b.id}",
            json={"title": "Hacked!"},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_cannot_delete_others_todo(
        self, client, db, test_user, auth_headers
    ):
        """Test that User A cannot delete User B's todo."""
        from src.core.security import hash_password

        user_b = User(email="userb@example.com", password_hash=hash_password("password123"))
        db.add(user_b)
        db.commit()
        db.refresh(user_b)

        todo_b = TodoTask(user_id=user_b.id, title="User B's Todo")
        db.add(todo_b)
        db.commit()

        # User A tries to delete User B's todo
        response = client.delete(f"/todos/{todo_b.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Verify todo still exists
        todo = db.get(TodoTask, todo_b.id)
        assert todo is not None


class TestAnonymousAccess:
    """Tests for anonymous access rejection."""

    def test_list_todos_requires_auth(self, client):
        """Test that listing todos requires authentication."""
        response = client.get("/todos")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_todo_requires_auth(self, client):
        """Test that creating a todo requires authentication."""
        response = client.post("/todos", json={"title": "New Todo"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_todo_requires_auth(self, client):
        """Test that getting a todo requires authentication."""
        response = client.get("/todos/00000000-0000-0000-0000-000000000000")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_todo_requires_auth(self, client):
        """Test that updating a todo requires authentication."""
        response = client.patch(
            "/todos/00000000-0000-0000-0000-000000000000",
            json={"title": "Updated"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_todo_requires_auth(self, client):
        """Test that deleting a todo requires authentication."""
        response = client.delete("/todos/00000000-0000-0000-0000-000000000000")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
