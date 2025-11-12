"""
Template Tags para Componentes UI
Facilita a inclusão de componentes nos templates Django
"""
from django import template
from core.models import Notification
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('components/global_search.html')
def global_search():
    """
    Inclui o componente de busca global
    Usage: {% global_search %}
    """
    return {}


@register.inclusion_tag('components/notification_center.html')
def notification_center(user):
    """
    Inclui o centro de notificações
    Usage: {% notification_center user %}
    """
    if not user or not user.is_authenticated:
        return {'unread_count': 0}
    
    # Contar notificações não lidas
    unread_count = Notification.objects.filter(
        user=user,
        status='pending'
    ).count()
    
    return {
        'unread_count': unread_count
    }


@register.inclusion_tag('components/scroll_to_top.html')
def scroll_to_top():
    """
    Inclui o botão de voltar ao topo
    Usage: {% scroll_to_top %}
    """
    return {}


@register.inclusion_tag('components/cta_banner.html')
def cta_banner(headline=None, subheadline=None, button_text=None, button_link=None, show_contact=False, **kwargs):
    """
    Inclui o banner CTA
    Usage: {% cta_banner headline="Título" subheadline="Subtítulo" show_contact=True %}
    """
    return {
        'headline': headline or "Transforme Seu Visual Hoje",
        'subheadline': subheadline or "Não deixe para amanhã o estilo que você pode ter hoje",
        'button_text': button_text or "Agendar Meu Horário",
        'button_link': button_link or '/agendar/',
        'show_contact': show_contact,
        **kwargs
    }


@register.inclusion_tag('components/team_section.html')
def team_section(barbers=None):
    """
    Inclui a seção de equipe
    Usage: {% team_section barbers=barbers %}
    """
    from barbeiros.models import Barbeiro
    
    if barbers is None:
        barbers = Barbeiro.objects.filter(active=True).order_by('name')
    
    return {
        'barbers': barbers
    }


@register.inclusion_tag('components/photo_upload_dialog.html')
def photo_upload_dialog():
    """
    Inclui o dialog de upload de fotos
    Usage: {% photo_upload_dialog %}
    """
    return {}


@register.inclusion_tag('components/product_selection_dialog.html')
def product_selection_dialog():
    """
    Inclui o dialog de seleção de produtos
    Usage: {% product_selection_dialog %}
    """
    return {}


@register.filter
def mul(value, arg):
    """
    Multiplica dois valores
    Usage: {{ value|mul:0.1 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

