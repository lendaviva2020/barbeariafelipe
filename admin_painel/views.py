from datetime import datetime, timedelta

from django.core.cache import cache
from django.db.models import Avg, Sum
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from agendamentos.models import Agendamento
from barbeiros.models import Barbeiro
from servicos.models import Servico
from users.models import User


class DashboardStatsView(APIView):
    """Estatísticas do dashboard administrativo

    Cache: 5 minutos para otimizar performance
    """

    permission_classes = (IsAdminUser,)

    def get(self, request):
        start_date = request.query_params.get(
            "start_date", (timezone.now() - timedelta(days=30)).date()
        )
        end_date = request.query_params.get("end_date", timezone.now().date())

        # Converter strings para datas se necessário
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Cache key único por período
        cache_key = f"dashboard_stats_{start_date}_{end_date}"
        cached_stats = cache.get(cache_key)

        if cached_stats:
            return Response(cached_stats)

        # Query otimizada com select_related
        agendamentos = Agendamento.objects.filter(
            appointment_date__range=[start_date, end_date]
        ).select_related("service", "barber")

        # Estatísticas básicas
        stats = {
            "total_appointments": agendamentos.count(),
            "completed_appointments": agendamentos.filter(status="completed").count(),
            "pending_appointments": agendamentos.filter(status="pending").count(),
            "cancelled_appointments": agendamentos.filter(status="cancelled").count(),
            "confirmed_appointments": agendamentos.filter(status="confirmed").count(),
            "total_revenue": agendamentos.filter(status="completed").aggregate(
                total=Sum("price")
            )["total"]
            or 0,
            "average_ticket": agendamentos.filter(status="completed").aggregate(
                avg=Avg("price")
            )["avg"]
            or 0,
            "active_barbers": Barbeiro.objects.filter(active=True).count(),
            "active_services": Servico.objects.filter(active=True).count(),
            "total_users": User.objects.filter(is_active=True).count(),
        }

        # Agendamentos de hoje
        today = timezone.now().date()
        today_appointments = Agendamento.objects.filter(appointment_date=today)

        stats["today"] = {
            "total": today_appointments.count(),
            "completed": today_appointments.filter(status="completed").count(),
            "pending": today_appointments.filter(status="pending").count(),
            "cancelled": today_appointments.filter(status="cancelled").count(),
        }

        # Armazenar em cache por 5 minutos (300 segundos)
        cache.set(cache_key, stats, 300)

        return Response(stats)


class AgendamentosAdminView(generics.ListAPIView):
    """Listar todos os agendamentos (admin)"""

    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Agendamento.objects.all()
        status_filter = self.request.query_params.get("status")

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Otimização: select_related para reduzir queries N+1
        return queryset.select_related(
            "user", "service", "barber", "barber__user", "coupon"
        ).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Serializar dados
        data = []
        for agendamento in queryset:
            data.append(
                {
                    "id": agendamento.id,
                    "customer_name": agendamento.customer_name,
                    "customer_phone": agendamento.customer_phone,
                    "service": agendamento.service.name,
                    "barber": agendamento.barber.name,
                    "date": agendamento.appointment_date,
                    "time": agendamento.appointment_time,
                    "status": agendamento.status,
                    "price": float(agendamento.price),
                    "payment_method": agendamento.payment_method,
                    "created_at": agendamento.created_at,
                }
            )

        return Response(data)


class UpdateAgendamentoStatusView(APIView):
    """Atualizar status do agendamento (admin)"""

    permission_classes = (IsAdminUser,)

    def patch(self, request, pk):
        try:
            agendamento = Agendamento.objects.get(pk=pk)
            new_status = request.data.get("status")

            if new_status not in dict(Agendamento.STATUS_CHOICES):
                return Response(
                    {"error": "Status inválido"}, status=status.HTTP_400_BAD_REQUEST
                )

            agendamento.status = new_status
            if new_status == "completed":
                agendamento.complete()
            elif new_status == "cancelled":
                reason = request.data.get("reason", "Cancelado pelo admin")
                agendamento.cancel(reason)
            else:
                agendamento.save()

            return Response({"message": "Status atualizado com sucesso"})
        except Agendamento.DoesNotExist:
            return Response(
                {"error": "Agendamento não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )
