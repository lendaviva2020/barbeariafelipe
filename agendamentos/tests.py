from datetime import date, time

import pytest
from rest_framework import status

from .models import Agendamento


@pytest.mark.django_db
class TestAgendamentos:
    def test_create_agendamento(self, authenticated_client, servico, barbeiro):
        """Teste de criação de agendamento"""
        data = {
            "service": servico.id,
            "barber": barbeiro.id,
            "appointment_date": str(date.today()),
            "appointment_time": "10:00",
            "customer_name": "Test Customer",
            "customer_phone": "45999999999",
            "payment_method": "cash",
        }
        response = authenticated_client.post("/api/agendamentos/create/", data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_list_agendamentos(self, authenticated_client, user):
        """Teste de listagem de agendamentos"""
        response = authenticated_client.get("/api/agendamentos/")
        assert response.status_code == status.HTTP_200_OK

    def test_available_slots(self, api_client, barbeiro):
        """Teste de horários disponíveis"""
        response = api_client.get(
            f"/api/agendamentos/available-slots/?date={date.today()}&barber_id={barbeiro.id}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)


@pytest.mark.django_db
class TestAgendamentoModel:
    def test_final_price_calculation(self, user, servico, barbeiro):
        """Teste de cálculo do preço final"""
        agendamento = Agendamento.objects.create(
            user=user,
            service=servico,
            barber=barbeiro,
            appointment_date=date.today(),
            appointment_time=time(10, 0),
            customer_name="Test",
            customer_phone="45999999999",
            price=100,
            discount_amount=10,
        )
        assert agendamento.final_price == 90
