"""
Template tags customizadas para componentes UI
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('components/ui/button.html')
def ui_button(text='', variant='default', size='default', type='button', **kwargs):
    """
    Renderiza um botão
    
    Uso:
    {% ui_button text="Clique" variant="primary" size="lg" %}
    """
    return {
        'text': text,
        'variant': variant,
        'size': size,
        'type': type,
        **kwargs
    }


@register.inclusion_tag('components/ui/badge.html')
def ui_badge(text='', variant='default', **kwargs):
    """
    Renderiza um badge
    
    Uso:
    {% ui_badge text="Novo" variant="default" %}
    """
    return {
        'text': text,
        'variant': variant,
        **kwargs
    }


@register.inclusion_tag('components/ui/alert.html')
def ui_alert(title='', description='', variant='default', **kwargs):
    """
    Renderiza um alerta
    
    Uso:
    {% ui_alert title="Atenção" description="Mensagem importante" variant="destructive" %}
    """
    return {
        'title': title,
        'description': description,
        'variant': variant,
        **kwargs
    }


@register.inclusion_tag('components/ui/card.html')
def ui_card(title='', description='', **kwargs):
    """
    Renderiza um card
    
    Uso:
    {% ui_card title="Card Title" description="Description" %}
    """
    return {
        'title': title,
        'description': description,
        **kwargs
    }


@register.inclusion_tag('components/ui/progress.html')
def ui_progress(value=0, max=100, **kwargs):
    """
    Renderiza barra de progresso
    
    Uso:
    {% ui_progress value=75 max=100 %}
    """
    return {
        'value': value,
        'max': max,
        **kwargs
    }


@register.inclusion_tag('components/ui/skeleton.html')
def ui_skeleton(width='100%', height='20px', rounded='md', **kwargs):
    """
    Renderiza skeleton loading
    
    Uso:
    {% ui_skeleton width="200px" height="30px" %}
    """
    return {
        'width': width,
        'height': height,
        'rounded': rounded,
        **kwargs
    }


@register.inclusion_tag('components/ui/separator.html')
def ui_separator(orientation='horizontal', **kwargs):
    """
    Renderiza separador
    
    Uso:
    {% ui_separator orientation="horizontal" %}
    """
    return {
        'orientation': orientation,
        **kwargs
    }


@register.inclusion_tag('components/ui/avatar.html')
def ui_avatar(src='', name='', fallback='', alt='', **kwargs):
    """
    Renderiza avatar
    
    Uso:
    {% ui_avatar src="/img/avatar.jpg" name="João Silva" %}
    """
    return {
        'src': src,
        'name': name,
        'fallback': fallback,
        'alt': alt,
        **kwargs
    }


@register.simple_tag
def ui_icon(name, size='4', **kwargs):
    """
    Renderiza um ícone SVG heroicons
    
    Uso:
    {% ui_icon "check" size="5" %}
    """
    icons = {
        'check': f'<svg class="h-{size} w-{size}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>',
        'x': f'<svg class="h-{size} w-{size}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>',
        'chevron-down': f'<svg class="h-{size} w-{size}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>',
        'chevron-right': f'<svg class="h-{size} w-{size}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>',
        'chevron-left': f'<svg class="h-{size} w-{size}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>',
        'search': f'<svg class="h-{size} w-{size}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>',
        'user': f'<svg class="h-{size} w-{size}" fill="currentColor" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>',
        'calendar': f'<svg class="h-{size} w-{size}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>',
    }
    
    return mark_safe(icons.get(name, ''))


@register.filter
def add_class(field, css_class):
    """
    Adiciona classe CSS a um campo de formulário
    
    Uso:
    {{ form.email|add_class:"input" }}
    """
    return field.as_widget(attrs={'class': css_class})


@register.filter
def split(value, separator=' '):
    """
    Divide string em lista
    
    Uso:
    {{ "a b c"|split:" " }}
    """
    return value.split(separator) if value else []


@register.filter
def mul(value, arg):
    """
    Multiplica valores
    
    Uso:
    {{ 5|mul:3 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

