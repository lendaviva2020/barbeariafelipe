import pytest
from rest_framework import status


@pytest.mark.django_db
class TestCupons:
    def test_validate_cupom_valid(self, authenticated_client, cupom_valid):
        """Teste de validação de cupom válido"""
        response = authenticated_client.post(
            "/api/agendamentos/validate-cupom/", {"code": cupom_valid.code}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["valid"] is True

    def test_validate_cupom_expired(self, authenticated_client, cupom_expired):
        """Teste de validação de cupom expirado"""
        response = authenticated_client.post(
            "/api/agendamentos/validate-cupom/", {"code": cupom_expired.code}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # Quando cupom é inválido, a resposta contém 'valid': False ou um erro de validação
        assert (
            response.data.get("valid") is False
            or "message" in response.data
            or "non_field_errors" in response.data
        )

    def test_validate_cupom_not_found(self, authenticated_client):
        """Teste de validação de cupom inexistente"""
        response = authenticated_client.post(
            "/api/agendamentos/validate-cupom/", {"code": "NOTFOUND"}
        )
        # Aceitar tanto 400 (serializer) quanto 404 (view)
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCupomModel:
    def test_cupom_is_valid(self, cupom_valid):
        """Teste de cupom válido"""
        assert cupom_valid.is_valid is True

    def test_cupom_is_invalid_expired(self, cupom_expired):
        """Teste de cupom expirado"""
        assert cupom_expired.is_valid is False
