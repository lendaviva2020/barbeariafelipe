import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    def test_register_user_success(self, api_client, user_data):
        """Teste de registro de usuário bem-sucedido"""
        response = api_client.post("/api/users/register/", user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data
        assert "tokens" in response.data
        assert response.data["user"]["email"] == user_data["email"]

    def test_register_user_duplicate_email(self, api_client, user, user_data):
        """Teste de registro com email duplicado"""
        response = api_client.post("/api/users/register/", user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:
    def test_login_success(self, api_client, user):
        """Teste de login bem-sucedido"""
        response = api_client.post(
            "/api/users/login/",
            {"email": "test@example.com", "password": "testpass123"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "tokens" in response.data
        assert "user" in response.data

    def test_login_invalid_credentials(self, api_client, user):
        """Teste de login com credenciais inválidas"""
        response = api_client.post(
            "/api/users/login/", {"email": "test@example.com", "password": "wrongpass"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, api_client):
        """Teste de login com usuário inexistente"""
        response = api_client.post(
            "/api/users/login/",
            {"email": "nonexistent@example.com", "password": "somepass"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserDetail:
    def test_get_user_detail_authenticated(self, authenticated_client, user):
        """Teste de obter detalhes do usuário autenticado"""
        response = authenticated_client.get("/api/users/me/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email

    def test_get_user_detail_unauthenticated(self, api_client):
        """Teste de obter detalhes sem autenticação"""
        response = api_client.get("/api/users/me/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self, db):
        """Teste de criação de usuário"""
        user = User.objects.create_user(
            email="newuser@example.com", password="pass123", name="New User"
        )
        assert user.email == "newuser@example.com"
        assert user.name == "New User"
        assert user.role == "user"
        assert user.is_active is True
        assert user.is_staff is False

    def test_create_superuser(self, db):
        """Teste de criação de superusuário"""
        admin = User.objects.create_superuser(
            email="admin@example.com", password="admin123", name="Admin"
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.role == "admin"

    def test_user_properties(self, user):
        """Teste das propriedades do usuário"""
        assert user.is_admin is False
        assert user.is_barber is False

    def test_admin_properties(self, admin_user):
        """Teste das propriedades do admin"""
        assert admin_user.is_admin is True
