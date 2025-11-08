from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from barbeiros.models import Barbeiro
from cupons.models import Cupom
from servicos.models import Servico

User = get_user_model()


@pytest.fixture
def api_client():
    """Cliente API REST Framework"""
    return APIClient()


@pytest.fixture
def user_data():
    """Dados para criar usuário"""
    return {
        "email": "test@example.com",
        "password": "testpass123",
        "name": "Test User",
        "phone": "45999999999",
    }


@pytest.fixture
def user(db, user_data):
    """Usuário comum"""
    return User.objects.create_user(
        email=user_data["email"],
        password=user_data["password"],
        name=user_data["name"],
        phone=user_data["phone"],
    )


@pytest.fixture
def admin_user(db):
    """Usuário admin"""
    return User.objects.create_superuser(
        email="admin@example.com", password="adminpass123", name="Admin User"
    )


@pytest.fixture
def barber_user(db):
    """Usuário barbeiro"""
    return User.objects.create_user(
        email="barber@example.com",
        password="barberpass123",
        name="Barber User",
        role="barber",
    )


@pytest.fixture
def servico(db):
    """Serviço de teste"""
    return Servico.objects.create(
        name="Corte Social",
        description="Corte clássico",
        price=45.00,
        duration=30,
        category="haircut",
        active=True,
    )


@pytest.fixture
def barbeiro(db, barber_user):
    """Barbeiro de teste"""
    return Barbeiro.objects.create(
        user=barber_user,
        name=barber_user.name,
        specialty="Cortes clássicos",
        active=True,
        working_hours={
            "monday": {"active": True, "start": "08:00", "end": "18:00"},
            "tuesday": {"active": True, "start": "08:00", "end": "18:00"},
            "wednesday": {"active": True, "start": "08:00", "end": "18:00"},
            "thursday": {"active": True, "start": "08:00", "end": "18:00"},
            "friday": {"active": True, "start": "08:00", "end": "18:00"},
            "saturday": {"active": True, "start": "08:00", "end": "16:00"},
            "sunday": {"active": False},
        },
    )


@pytest.fixture
def cupom_valid(db):
    """Cupom válido"""
    return Cupom.objects.create(
        code="TEST10",
        discount=10,
        discount_type="percentage",
        expiry_date=date.today() + timedelta(days=30),
        active=True,
    )


@pytest.fixture
def cupom_expired(db):
    """Cupom expirado"""
    return Cupom.objects.create(
        code="EXPIRED",
        discount=15,
        discount_type="percentage",
        expiry_date=date.today() - timedelta(days=1),
        active=True,
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Cliente autenticado"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Cliente autenticado como admin"""
    api_client.force_authenticate(user=admin_user)
    return api_client
