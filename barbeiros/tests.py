import pytest
from rest_framework import status


@pytest.mark.django_db
class TestBarbeiros:
    def test_list_barbeiros_public(self, api_client, barbeiro):
        """Teste de listagem pública de barbeiros"""
        response = api_client.get("/api/barbeiros/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 1

    def test_list_only_active_barbeiros(self, api_client, barbeiro, db):
        """Teste que apenas barbeiros ativos são listados"""
        from barbeiros.models import Barbeiro
        from users.models import User

        # Criar barbeiro inativo
        inactive_user = User.objects.create_user(
            email="inactive@test.com",
            password="pass123",
            name="Inactive",
            role="barber",
        )
        Barbeiro.objects.create(
            user=inactive_user, name="Barbeiro Inativo", active=False
        )

        response = api_client.get("/api/barbeiros/")
        barbeiros = response.data["results"]

        # Verificar que nenhum barbeiro inativo aparece
        for b in barbeiros:
            assert b.get("active") is not False


@pytest.mark.django_db
class TestBarbeirosAdmin:
    def test_create_barbeiro_admin(self, admin_client, barber_user):
        """Teste de criação de barbeiro por admin"""
        data = {
            "user": barber_user.id,
            "name": "Novo Barbeiro",
            "specialty": "Barbas",
            "phone": "45999999999",
            "active": True,
            "working_hours": {
                "monday": {"active": True, "start": "09:00", "end": "18:00"}
            },
        }
        response = admin_client.post("/api/admin/barbeiros/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_barbeiro_admin(self, admin_client, barbeiro):
        """Teste de atualização de barbeiro por admin"""
        data = {"name": "Barbeiro Atualizado", "specialty": "Todos os tipos"}
        response = admin_client.patch(f"/api/admin/barbeiros/{barbeiro.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Barbeiro Atualizado"

    def test_delete_barbeiro_admin(self, admin_client, barbeiro):
        """Teste de exclusão de barbeiro por admin"""
        response = admin_client.delete(f"/api/admin/barbeiros/{barbeiro.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_barbeiro_non_admin(self, authenticated_client):
        """Teste que usuário comum não pode criar barbeiro"""
        data = {"name": "Test", "active": True}
        response = authenticated_client.post("/api/admin/barbeiros/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestBarbeiroModel:
    def test_barbeiro_str_representation(self, barbeiro):
        """Teste da representação string do barbeiro"""
        assert barbeiro.name in str(barbeiro)

    def test_barbeiro_working_hours(self, barbeiro):
        """Teste dos horários de trabalho do barbeiro"""
        assert "monday" in barbeiro.working_hours
        assert barbeiro.working_hours["monday"]["active"] is True
        assert barbeiro.working_hours["sunday"]["active"] is False
