from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from core.decorators import admin_required, admin_required_api
from core.models import AuditLog
from datetime import datetime, timedelta
import csv


@admin_required
def audit_logs_view(request):
    """Página de logs de auditoria"""
    return render(request, 'admin/audit_logs.html')


@admin_required_api
def audit_logs_api(request):
    """API: Lista de logs com filtros e paginação"""
    # Filtros
    action = request.GET.get('action', 'all')
    table = request.GET.get('table', 'all')
    search = request.GET.get('search', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    page = int(request.GET.get('page', 1))
    per_page = 50
    
    # Query base
    logs = AuditLog.objects.all().select_related('user')
    
    # Filtros
    if action != 'all':
        logs = logs.filter(action=action)
    
    if table != 'all':
        logs = logs.filter(table_name=table)
    
    if search:
        logs = logs.filter(
            Q(table_name__icontains=search) |
            Q(record_id__icontains=search) |
            Q(user__name__icontains=search)
        )
    
    if start_date:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        logs = logs.filter(created_at__gte=start)
    
    if end_date:
        end = datetime.strptime(end_date, '%Y-%m-%d')
        end = end.replace(hour=23, minute=59, second=59)
        logs = logs.filter(created_at__lte=end)
    
    # Contar total
    total = logs.count()
    
    # Paginação
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    logs = logs[start_idx:end_idx]
    
    # Serializar
    data = []
    for log in logs:
        data.append({
            'id': log.id,
            'action': log.action,
            'table_name': log.table_name,
            'record_id': log.record_id,
            'user_name': log.user.name if log.user else 'Sistema',
            'user_email': log.user.email if log.user else None,
            'old_data': log.old_data,
            'new_data': log.new_data,
            'ip_address': log.ip_address,
            'user_agent': log.user_agent,
            'created_at': log.created_at.isoformat(),
        })
    
    return JsonResponse({
        'logs': data,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })


@admin_required_api
def audit_logs_tables_api(request):
    """API: Lista de tabelas únicas para filtro"""
    tables = AuditLog.objects.values_list('table_name', flat=True).distinct().order_by('table_name')
    return JsonResponse({'tables': list(tables)})


@admin_required
def audit_logs_export_csv(request):
    """Exportar logs de auditoria em CSV"""
    # Aplicar mesmos filtros
    action = request.GET.get('action', 'all')
    table = request.GET.get('table', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    logs = AuditLog.objects.all().select_related('user')
    
    if action != 'all':
        logs = logs.filter(action=action)
    if table != 'all':
        logs = logs.filter(table_name=table)
    if start_date:
        logs = logs.filter(created_at__gte=datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        end = datetime.strptime(end_date, '%Y-%m-%d')
        end = end.replace(hour=23, minute=59, second=59)
        logs = logs.filter(created_at__lte=end)
    
    # Limitar a 10000 registros por segurança
    logs = logs[:10000]
    
    # Criar CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="audit_logs_{datetime.now().strftime("%Y%m%d")}.csv"'
    response.write('\ufeff')  # BOM para Excel reconhecer UTF-8
    
    writer = csv.writer(response)
    writer.writerow(['Data/Hora', 'Ação', 'Tabela', 'Usuário', 'ID do Registro', 'IP', 'Dados Antigos', 'Dados Novos'])
    
    for log in logs:
        writer.writerow([
            log.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            log.get_action_display(),
            log.table_name,
            log.user.name if log.user else 'Sistema',
            log.record_id or '',
            log.ip_address or '',
            str(log.old_data) if log.old_data else '',
            str(log.new_data) if log.new_data else '',
        ])
    
    return response

