#!/usr/bin/env python
"""
Script para popular o banco de dados com serviços e combos da Barbearia Francisco
Execute: python populate_services.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbearia.settings')
django.setup()

from servicos.models import Servico

def populate_services():
    """Popular banco com 6 serviços individuais e 3 combos"""
    
    print("Criando/atualizando servicos...")
    
    # Serviço 1: Corte Tradicional
    corte_tradicional = Servico.objects.create(
        name="Corte de Cabelo Tradicional",
        description="Corte clássico com técnicas tradicionais de barbearia, perfeito para quem busca elegância e sofisticação.",
        price=35.00,
        duration=30,
        category="haircut",
        image_url="https://images.unsplash.com/photo-1599351431202-1e0f0137899a?w=800",
        badge="Mais Procurado",
        features=[
            "Corte preciso com tesoura e máquina",
            "Acabamento com produtos premium",
            "Consultoria de estilo personalizada"
        ],
        active=True
    )
    print(f"  OK - {corte_tradicional.name}")
    
    # Serviço 2: Barba Completa
    barba_completa = Servico.objects.create(
        name="Barba Completa",
        description="Modelagem, aparagem e acabamento da barba com produtos específicos para hidratar e dar forma.",
        price=25.00,
        duration=25,
        category="beard",
        image_url="https://images.unsplash.com/photo-1516472042447-702bf6f6d322?w=800",
        badge="",
        features=[
            "Aparar e modelar com precisão",
            "Hidratação com óleo para barba",
            "Toalha quente para abrir os poros"
        ],
        active=True
    )
    print(f"  OK - {barba_completa.name}")
    
    # Serviço 3: Tratamento Capilar
    tratamento = Servico.objects.create(
        name="Tratamento Capilar",
        description="Hidratação profunda e reconstrução dos fios com produtos profissionais para cabelos saudáveis.",
        price=40.00,
        duration=40,
        category="treatment",
        image_url="https://images.unsplash.com/photo-1596704014031-3337aed51016?w=800",
        badge="",
        features=[
            "Limpeza profunda do couro cabeludo",
            "Hidratação com queratina",
            "Selamento dos fios"
        ],
        active=True
    )
    print(f"  OK - {tratamento.name}")
    
    # Serviço 4: Corte Degradê
    corte_degrade = Servico.objects.create(
        name="Corte Degradê",
        description="Corte moderno com transição suave entre os comprimentos, criando um visual contemporâneo e estiloso.",
        price=40.00,
        duration=35,
        category="haircut",
        image_url="https://images.unsplash.com/photo-1503951914875-452c1f0b0c8a?w=800",
        badge="Novidade",
        features=[
            "Técnica de degradê com máquina",
            "Design personalizado",
            "Acabamento com pomada modeladora"
        ],
        active=True
    )
    print(f"  OK - {corte_degrade.name}")
    
    # Serviço 5: Spa da Barba
    spa_barba = Servico.objects.create(
        name="Spa da Barba",
        description="Experiência relaxante com tratamento completo para a barba, incluindo limpeza, hidratação e modelagem.",
        price=50.00,
        duration=45,
        category="beard",
        image_url="https://images.unsplash.com/photo-1540337706094-da0b4a5b0c6f?w=800",
        badge="",
        features=[
            "Esfoliação facial",
            "Máscara hidratante",
            "Massagem facial relaxante"
        ],
        active=True
    )
    print(f"  OK - {spa_barba.name}")
    
    # Serviço 6: Limpeza de Pele
    limpeza_pele = Servico.objects.create(
        name="Limpeza de Pele",
        description="Limpeza facial profunda para remover impurezas, cravos e células mortas, revitalizando a pele.",
        price=45.00,
        duration=40,
        category="treatment",
        image_url="https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=800",
        badge="",
        features=[
            "Limpeza profunda com vapor",
            "Extração de cravos e impurezas",
            "Máscara facial de tratamento"
        ],
        active=True
    )
    print(f"  OK - {limpeza_pele.name}")
    
    print("\nCriando combos especiais...")
    
    # Combo 1: Clássico
    combo_classico = Servico.objects.create(
        name="Combo Clássico",
        description="O pacote perfeito para quem busca um visual tradicional e bem cuidado.",
        price=50.00,
        original_price=60.00,
        duration=55,
        category="combo",
        image_url="https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=800",
        badge="Economize R$ 10",
        features=[
            "Corte de Cabelo Tradicional",
            "Barba Completa",
            "Acabamento com produtos premium"
        ],
        is_combo=True,
        active=True
    )
    combo_classico.combo_services.add(corte_tradicional, barba_completa)
    print(f"  OK - {combo_classico.name} (economia: R$ {combo_classico.savings})")
    
    # Combo 2: Premium
    combo_premium = Servico.objects.create(
        name="Combo Premium",
        description="Experiência completa de cuidados masculinos para quem busca o máximo em bem-estar.",
        price=110.00,
        original_price=135.00,
        duration=120,
        category="combo",
        image_url="https://images.unsplash.com/photo-1595877244574-e90ce41ce089?w=800",
        badge="Mais Popular",
        features=[
            "Corte de Cabelo Degradê",
            "Spa da Barba",
            "Limpeza de Pele",
            "Massagem relaxante"
        ],
        is_combo=True,
        active=True
    )
    combo_premium.combo_services.add(corte_degrade, spa_barba, limpeza_pele)
    print(f"  OK - {combo_premium.name} (economia: R$ {combo_premium.savings})")
    
    # Combo 3: Manutenção
    combo_manutencao = Servico.objects.create(
        name="Combo Manutenção",
        description="Ideal para quem busca manter o visual sempre impecável entre cortes mais elaborados.",
        price=35.00,
        original_price=45.00,
        duration=30,
        category="combo",
        image_url="https://images.unsplash.com/photo-1595273670150-bd0c3c392e46?w=800",
        badge="Para Assinantes",
        features=[
            "Ajuste de laterais e nuca",
            "Acerto da barba",
            "Hidratação rápida",
            "Design de sobrancelhas"
        ],
        is_combo=True,
        active=True
    )
    print(f"  OK - {combo_manutencao.name} (economia: R$ {combo_manutencao.savings})")
    
    print(f"\nCONCLUIDO! {Servico.objects.count()} servicos criados:")
    print(f"   {Servico.objects.filter(is_combo=False).count()} servicos individuais")
    print(f"   {Servico.objects.filter(is_combo=True).count()} combos especiais")
    print("\nExecute: python manage.py runserver")
    print("Acesse: http://127.0.0.1:8000/servicos/\n")


if __name__ == '__main__':
    print("=" * 60)
    print("  BARBEARIA FRANCISCO - Popular Serviços")
    print("=" * 60)
    print()
    
    populate_services()

