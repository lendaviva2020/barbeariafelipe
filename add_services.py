"""
Script para adicionar serviços profissionais de barbearia
Baseado nas imagens fornecidas pelo cliente
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbearia.settings')
django.setup()

from servicos.models import Servico


def add_services():
    """Adiciona serviços profissionais ao sistema"""
    
    services_data = [
        {
            'name': 'Bigode Profissional',
            'description': 'Aparamento e modelagem profissional de bigode com tesoura e navalha. Inclui finalização com produtos premium e cera modeladora.',
            'price': 35.00,
            'duration': 30,
            'category': 'beard',
            'is_combo': False,
            'badge': 'Popular'
        },
        {
            'name': 'Corte Clássico',
            'description': 'Corte tradicional masculino com máquina e tesoura. Inclui degradê, acabamento na nuca e finalização com secador. Estilo atemporal e elegante.',
            'price': 50.00,
            'duration': 45,
            'category': 'haircut',
            'is_combo': False,
            'badge': 'Mais Vendido'
        },
        {
            'name': 'Barba Completa',
            'description': 'Aparamento completo de barba com máquina e acabamento com navalha. Inclui hidratação, toalha quente e produtos premium para barbas.',
            'price': 40.00,
            'duration': 35,
            'category': 'beard',
            'is_combo': False,
            'badge': 'Popular'
        },
        {
            'name': 'Corte + Barba Completo',
            'description': 'Combo completo: Corte clássico com degradê + Barba aparada e modelada. Tratamento premium com toalha quente, hidratação e produtos de alta qualidade. A experiência completa!',
            'price': 80.00,
            'duration': 75,
            'category': 'combo',
            'is_combo': True,
            'badge': 'Melhor Custo-Benefício',
            'original_price': 90.00
        },
        {
            'name': 'Corte Premium',
            'description': 'Corte moderno com fade alto, desenhos e acabamento impecável. Inclui lavagem, secador, produtos de styling e finalização profissional.',
            'price': 65.00,
            'duration': 60,
            'category': 'haircut',
            'is_combo': False,
            'badge': 'Premium'
        },
        # Serviços adicionais complementares
        {
            'name': 'Barba à Navalha',
            'description': 'Barbear tradicional italiano com navalha. Inclui toalha quente, pré-barba, espuma premium e pós-barba refrescante. Ritual clássico de relaxamento.',
            'price': 55.00,
            'duration': 40,
            'category': 'beard',
            'is_combo': False,
            'badge': 'Clássico'
        },
        {
            'name': 'Corte Infantil',
            'description': 'Corte especial para crianças até 12 anos. Ambiente descontraído, profissionais pacientes e atenção especial aos pequenos.',
            'price': 35.00,
            'duration': 30,
            'category': 'haircut',
            'is_combo': False,
            'badge': 'Kids'
        },
        {
            'name': 'Platinado/Luzes',
            'description': 'Descoloração e aplicação de luzes ou platinado. Produtos profissionais de alta qualidade para um visual moderno e ousado.',
            'price': 120.00,
            'duration': 120,
            'category': 'treatment',
            'is_combo': False,
            'badge': 'Ousado'
        },
        {
            'name': 'Sobrancelha',
            'description': 'Aparamento e design de sobrancelhas masculinas. Acabamento com pinça e navalha para visual limpo e definido.',
            'price': 20.00,
            'duration': 15,
            'category': 'treatment',
            'is_combo': False,
            'badge': ''
        },
        {
            'name': 'Pacote VIP Executivo',
            'description': 'Experiência premium completa: Corte + Barba + Sobrancelha + Relaxamento facial com toalha quente + Massagem no couro cabeludo + Produtos premium. O tratamento que você merece!',
            'price': 150.00,
            'duration': 120,
            'category': 'combo',
            'is_combo': True,
            'badge': 'VIP',
            'original_price': 200.00,
            'features': ['Corte Premium', 'Barba Completa', 'Sobrancelha', 'Relaxamento Facial', 'Massagem']
        }
    ]
    
    print("=" * 60)
    print("ADICIONANDO SERVIÇOS PROFISSIONAIS")
    print("=" * 60)
    print()
    
    created_count = 0
    updated_count = 0
    
    for service_data in services_data:
        # Verificar se serviço já existe
        existing = Servico.objects.filter(name=service_data['name']).first()
        
        if existing:
            # Atualizar serviço existente
            for key, value in service_data.items():
                setattr(existing, key, value)
            existing.save()
            print(f"[ATUALIZADO] {service_data['name']}")
            print(f"   Preco: R$ {service_data['price']:.2f} | Duracao: {service_data['duration']}min")
            updated_count += 1
        else:
            # Criar novo serviço
            Servico.objects.create(**service_data)
            print(f"[CRIADO] {service_data['name']}")
            print(f"   Preco: R$ {service_data['price']:.2f} | Duracao: {service_data['duration']}min")
            created_count += 1
        
        print()
    
    print("=" * 60)
    print(f"RESUMO:")
    print(f"  Criados: {created_count}")
    print(f"  Atualizados: {updated_count}")
    print(f"  Total: {created_count + updated_count}")
    print("=" * 60)
    print()
    print("[OK] Servicos adicionados com sucesso!")
    print()
    print("PROXIMOS PASSOS:")
    print("   1. Recarregue a pagina de agendamento")
    print("   2. Os servicos devem aparecer agora")
    print("   3. Teste o fluxo de agendamento completo")
    print()


if __name__ == '__main__':
    add_services()

