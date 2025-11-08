from datetime import date, time

import pytest
from rest_framework import status

from agendamentos.models import Agendamento


@pytest.mark.django_db
class TestDashboardStats:
    def test_dashboard_stats_admin(self, admin_client):
        """Teste de estatísticas do dashboard para admin"""
        response = admin_client.get("/api/admin/dashboard/stats/")
        assert response.status_code == status.HTTP_200_OK
        assert "total_appointments" in response.data
        assert "total_revenue" in response.data
        assert "active_barbers" in response.data
        assert "today" in response.data

    def test_dashboard_stats_non_admin(self, authenticated_client):
        """Teste que usuário comum não acessa dashboard stats"""
        response = authenticated_client.get("/api/admin/dashboard/stats/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_dashboard_stats_with_date_range(self, admin_client):
        """Teste de estatísticas com filtro de data"""
        response = admin_client.get(
            "/api/admin/dashboard/stats/?start_date=2025-01-01&end_date=2025-12-31"
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestAgendamentosAdmin:
    def test_list_all_agendamentos_admin(self, admin_client, user, servico, barbeiro):
        """Teste de listagem de todos agendamentos por admin"""
        # Criar agendamento
        Agendamento.objects.create(
            user=user,
            service=servico,
            barber=barbeiro,
            appointment_date=date.today(),
            appointment_time=time(10, 0),
            customer_name="Test Customer",
            customer_phone="45999999999",
            price=45.00,
        )

        response = admin_client.get("/api/admin/agendamentos/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_filter_agendamentos_by_status(self, admin_client, user, servico, barbeiro):
        """Teste de filtro de agendamentos por status"""
        # Criar agendamento pendente
        Agendamento.objects.create(
            user=user,
            service=servico,
            barber=barbeiro,
            appointment_date=date.today(),
            appointment_time=time(10, 0),
            customer_name="Test",
            customer_phone="45999999999",
            price=45.00,
            status="pending",
        )

        response = admin_client.get("/api/admin/agendamentos/?status=pending")
        assert response.status_code == status.HTTP_200_OK
        assert all(a["status"] == "pending" for a in response.data)

    def test_update_agendamento_status_admin(
        self, admin_client, user, servico, barbeiro
    ):
        """Teste de atualização de status de agendamento"""
        agendamento = Agendamento.objects.create(
            user=user,
            service=servico,
            barber=barbeiro,
            appointment_date=date.today(),
            appointment_time=time(10, 0),
            customer_name="Test",
            customer_phone="45999999999",
            price=45.00,
            status="pending",
        )

        response = admin_client.patch(
            f"/api/admin/agendamentos/{agendamento.id}/status/",
            {"status": "confirmed"},
        )
        assert response.status_code == status.HTTP_200_OK

        agendamento.refresh_from_db()
        assert agendamento.status == "confirmed"

    def test_complete_agendamento(self, admin_client, user, servico, barbeiro):
        """Teste de conclusão de agendamento"""
        agendamento = Agendamento.objects.create(
            user=user,
            service=servico,
            barber=barbeiro,
            appointment_date=date.today(),
            appointment_time=time(10, 0),
            customer_name="Test",
            customer_phone="45999999999",
            price=45.00,
            status="confirmed",
        )

        response = admin_client.patch(
            f"/api/admin/agendamentos/{agendamento.id}/status/", {"status": "completed"}
        )
        assert response.status_code == status.HTTP_200_OK

        agendamento.refresh_from_db()
        assert agendamento.status == "completed"
        assert agendamento.completed_at is not None

    def test_cancel_agendamento_admin(self, admin_client, user, servico, barbeiro):
        """Teste de cancelamento de agendamento por admin"""
        agendamento = Agendamento.objects.create(
            user=user,
            service=servico,
            barber=barbeiro,
            appointment_date=date.today(),
            appointment_time=time(10, 0),
            customer_name="Test",
            customer_phone="45999999999",
            price=45.00,
        )

        response = admin_client.patch(
            f"/api/admin/agendamentos/{agendamento.id}/status/",
            {"status": "cancelled", "reason": "Cliente cancelou"},
        )
        assert response.status_code == status.HTTP_200_OK

        agendamento.refresh_from_db()
        assert agendamento.status == "cancelled"
        assert agendamento.cancelled_at is not None


@pytest.mark.django_db
class TestAdminPermissions:
    def test_admin_endpoints_require_admin_permission(self, authenticated_client):
        """Teste que endpoints admin requerem permissão de admin"""
        endpoints = [
            "/api/admin/dashboard/stats/",
            "/api/admin/agendamentos/",
            "/api/admin/servicos/",
            "/api/admin/barbeiros/",
            "/api/admin/cupons/",
        ]

        for endpoint in endpoints:
            response = authenticated_client.get(endpoint)
            assert response.status_code == status.HTTP_403_FORBIDDEN
