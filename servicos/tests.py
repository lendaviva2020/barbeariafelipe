import pytest
from rest_framework import status


@pytest.mark.django_db
class TestServicos:
    def test_list_servicos_public(self, api_client, servico):
        """Teste de listagem pública de serviços"""
        response = api_client.get("/api/servicos/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 1

    def test_list_only_active_servicos(self, api_client, servico, db):
        """Teste que apenas serviços ativos são listados"""
        from servicos.models import Servico

        # Criar serviço inativo
        Servico.objects.create(
            name="Serviço Inativo",
            price=30.00,
            duration=20,
            category="haircut",
            active=False,
        )

        response = api_client.get("/api/servicos/")
        servicos = response.data["results"]

        # Verificar que nenhum serviço inativo aparece
        for s in servicos:
            assert s.get("active") is not False


@pytest.mark.django_db
class TestServicosAdmin:
    def test_create_servico_admin(self, admin_client):
        """Teste de criação de serviço por admin"""
        data = {
            "name": "Corte Premium",
            "description": "Corte diferenciado",
            "price": 80.00,
            "duration": 45,
            "category": "haircut",
            "active": True,
        }
        response = admin_client.post("/api/admin/servicos/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Corte Premium"

    def test_update_servico_admin(self, admin_client, servico):
        """Teste de atualização de serviço por admin"""
        data = {"name": "Corte Atualizado", "price": 50.00}
        response = admin_client.patch(f"/api/admin/servicos/{servico.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Corte Atualizado"

    def test_delete_servico_admin(self, admin_client, servico):
        """Teste de exclusão de serviço por admin"""
        response = admin_client.delete(f"/api/admin/servicos/{servico.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_servico_non_admin(self, authenticated_client):
        """Teste que usuário comum não pode criar serviço"""
        data = {"name": "Test", "price": 50.00}
        response = authenticated_client.post("/api/admin/servicos/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestServicoModel:
    def test_servico_str_representation(self, servico):
        """Teste da representação string do serviço"""
        assert "Corte Social" in str(servico)
        assert "45" in str(servico)

    def test_servico_ordering(self, db):
        """Teste da ordenação de serviços por categoria e nome"""
        from servicos.models import Servico

        servico1 = Servico.objects.create(
            name="Z Corte", price=40, category="haircut", active=True
        )
        servico2 = Servico.objects.create(
            name="A Barba", price=30, category="beard", active=True
        )

        servicos = list(Servico.objects.all())
        # Barba vem antes de Corte (ordem por categoria)
        assert servicos[0].category == "beard"
