"""
Script para atualizar serviços com URLs de imagens
Execut ar DEPOIS de salvar as imagens em static/images/services/
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbearia.settings')
django.setup()

from servicos.models import Servico


def update_images():
    """Atualiza serviços com URLs de imagens"""
    
    # Mapeamento de serviços para imagens
    image_mapping = {
        'Bigode Profissional': '/static/images/services/bigode-professional.jpg',
        'Corte Clássico': '/static/images/services/corte-classico.jpg',
        'Barba Completa': '/static/images/services/barba-completa.jpg',
        'Corte + Barba Completo': '/static/images/services/corte-barba-combo.jpg',
        'Corte Premium': '/static/images/services/corte-premium.jpg',
        'Barba à Navalha': '/static/images/services/barba-completa.jpg',  # Reusar imagem
        'Corte Infantil': '/static/images/services/corte-classico.jpg',  # Reusar imagem
        'Platinado/Luzes': '/static/images/services/corte-premium.jpg',  # Reusar imagem
        'Sobrancelha': '/static/images/services/bigode-professional.jpg',  # Reusar imagem
        'Pacote VIP Executivo': '/static/images/services/corte-barba-combo.jpg',  # Reusar imagem
    }
    
    print("=" * 70)
    print("ATUALIZANDO IMAGENS DOS SERVICOS")
    print("=" * 70)
    print()
    
    updated_count = 0
    
    for service_name, image_url in image_mapping.items():
        try:
            service = Servico.objects.filter(name=service_name).first()
            if service:
                service.image_url = image_url
                service.save()
                
                print(f"[OK] {service_name}")
                print(f"     Imagem: {image_url}")
                print()
                updated_count += 1
            else:
                print(f"[AVISO] Servico nao encontrado: {service_name}")
                print()
            
        except Exception as e:
            print(f"[ERRO] {service_name}: {str(e)}")
            print()
    
    print("=" * 70)
    print(f"RESUMO: {updated_count} servicos atualizados com imagens")
    print("=" * 70)
    print()
    print("IMPORTANTE:")
    print("  1. Certifique-se que as imagens estao em static/images/services/")
    print("  2. Execute: python manage.py collectstatic --noinput")
    print("  3. Recarregue as paginas para ver as imagens")
    print()


if __name__ == '__main__':
    # Verificar se diretório existe
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, 'static', 'images', 'services')
    
    if not os.path.exists(images_dir):
        print("CRIANDO DIRETORIOS DE IMAGENS...")
        os.makedirs(images_dir, exist_ok=True)
        
        # Criar também outros diretórios
        os.makedirs(os.path.join(base_dir, 'static', 'images', 'gallery'), exist_ok=True)
        os.makedirs(os.path.join(base_dir, 'static', 'images', 'team'), exist_ok=True)
        os.makedirs(os.path.join(base_dir, 'static', 'images', 'hero'), exist_ok=True)
        
        print("[OK] Diretorios criados!")
        print()
        print("AGORA:")
        print("  1. Salve as 5 imagens em static/images/services/:")
        print("     - bigode-professional.jpg")
        print("     - corte-classico.jpg")
        print("     - barba-completa.jpg")
        print("     - corte-barba-combo.jpg")
        print("     - corte-premium.jpg")
        print()
        print("  2. Execute este script novamente: python update_services_images.py")
        print()
    else:
        update_images()

