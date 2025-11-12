"""
Script para configurar placeholders de imagens
Até que as imagens reais sejam salvas
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbearia.settings')
django.setup()

from servicos.models import Servico


def setup_placeholders():
    """Configura placeholders até imagens reais serem adicionadas"""
    
    # Usar placeholders de alta qualidade do Unsplash
    placeholders = {
        'Bigode Profissional': 'https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=800&q=80',  # Barber styling mustache
        'Corte Clássico': 'https://images.unsplash.com/photo-1599351431202-1e0f0137899a?w=800&q=80',  # Classic haircut
        'Barba Completa': 'https://images.unsplash.com/photo-1622287162716-f311baa1a2b8?w=800&q=80',  # Beard trimming
        'Corte + Barba Completo': 'https://images.unsplash.com/photo-1503951914875-452162b0f3f1?w=800&q=80',  # Barbershop scene
        'Corte Premium': 'https://images.unsplash.com/photo-1605497788044-5a32c7078486?w=800&q=80',  # Modern fade
        'Barba à Navalha': 'https://images.unsplash.com/photo-1621607512214-68297480165e?w=800&q=80',  # Straight razor
        'Corte Infantil': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&q=80',  # Kids haircut
        'Platinado/Luzes': 'https://images.unsplash.com/photo-1622286342621-4bd786c2447c?w=800&q=80',  # Bleached hair
        'Sobrancelha': 'https://images.unsplash.com/photo-1620331309850-e6c8c5c2e87c?w=800&q=80',  # Eyebrow grooming
        'Pacote VIP Executivo': 'https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=800&q=80',  # Premium service
    }
    
    print("=" * 70)
    print("CONFIGURANDO PLACEHOLDERS DE IMAGENS")
    print("=" * 70)
    print()
    print("IMPORTANTE: Estes sao placeholders temporarios do Unsplash.")
    print("Para usar suas proprias imagens:")
    print("  1. Salve as 5 fotos em static/images/services/")
    print("  2. Execute: python update_services_images.py")
    print()
    print("=" * 70)
    print()
    
    updated = 0
    
    for service_name, image_url in placeholders.items():
        try:
            service = Servico.objects.filter(name=service_name).first()
            if service:
                service.image_url = image_url
                service.save()
                print(f"[OK] {service_name}")
                updated += 1
            else:
                print(f"[SKIP] {service_name} - nao encontrado")
        except Exception as e:
            print(f"[ERRO] {service_name}: {str(e)}")
    
    print()
    print("=" * 70)
    print(f"RESUMO: {updated} servicos atualizados com placeholders")
    print("=" * 70)
    print()
    print("As imagens apareceram no site agora!")
    print("Recarregue a pagina para ver.")
    print()


if __name__ == '__main__':
    setup_placeholders()

