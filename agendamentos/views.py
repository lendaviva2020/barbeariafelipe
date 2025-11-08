from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Agendamento
from .serializers import AgendamentoSerializer, CreateAgendamentoSerializer


class AgendamentoListView(generics.ListAPIView):
    """Listar agendamentos do usuário"""

    serializer_class = AgendamentoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Otimização: select_related para reduzir queries N+1
        return (
            Agendamento.objects.filter(user=self.request.user)
            .select_related("service", "barber", "coupon")
            .order_by("-appointment_date", "-appointment_time")
        )


@method_decorator(ratelimit(key="user", rate="10/h", method="POST"), name="dispatch")
class AgendamentoCreateView(generics.CreateAPIView):
    """Criar novo agendamento

    Rate limit: 10 agendamentos por hora por usuário
    """

    serializer_class = CreateAgendamentoSerializer
    permission_classes = (IsAuthenticated,)


class AgendamentoCancelView(APIView):
    """Cancelar agendamento"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            agendamento = Agendamento.objects.get(pk=pk, user=request.user)
            reason = request.data.get("reason", "Cancelado pelo cliente")
            agendamento.cancel(reason)
            return Response({"message": "Agendamento cancelado com sucesso"})
        except Agendamento.DoesNotExist:
            return Response(
                {"error": "Agendamento não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )


@method_decorator(ratelimit(key="ip", rate="60/m", method="GET"), name="dispatch")
class AvailableSlotsView(APIView):
    """Verificar horários disponíveis

    Rate limit: 60 requisições por minuto por IP
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        date = request.query_params.get("date")
        barber_id = request.query_params.get("barber_id")

        if not date or not barber_id:
            return Response(
                {"error": "Data e barbeiro são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Horários padrão
        all_slots = [
            "08:00",
            "08:30",
            "09:00",
            "09:30",
            "10:00",
            "10:30",
            "11:00",
            "11:30",
            "14:00",
            "14:30",
            "15:00",
            "15:30",
            "16:00",
            "16:30",
            "17:00",
            "17:30",
            "18:00",
            "18:30",
            "19:00",
        ]

        # Otimização: Buscar apenas os horários ocupados (query única com set)
        occupied = set(
            Agendamento.objects.filter(
                appointment_date=date,
                barber_id=barber_id,
                status__in=["pending", "confirmed"],
            ).values_list("appointment_time", flat=True)
        )

        occupied_times = {t.strftime("%H:%M") for t in occupied}

        # Retornar horários disponíveis
        available_slots = [
            {"time_slot": slot, "available": slot not in occupied_times}
            for slot in all_slots
        ]

        return Response(available_slots)
