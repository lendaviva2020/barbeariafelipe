"""
Script para popular o banco de dados com dados iniciais
Execute: python populate_db.py
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barbearia.settings")
django.setup()

from barbeiros.models import Barbeiro
from cupons.models import Cupom
from servicos.models import Servico
from users.models import User


def populate():
    print("Populando banco de dados...")

    # 1. Criar usuário admin
    try:
        admin = User.objects.create_superuser(
            email="admin@barbearia.com",
            password="admin123",
            name="Administrador Francisco",
        )
        print("[OK] Admin criado: admin@barbearia.com / admin123")
    except:
        print("[INFO] Admin ja existe")

    # 2. Criar usuário barbeiro
    try:
        barbeiro_user = User.objects.create_user(
            email="joao@barbearia.com",
            password="barber123",
            name="João Silva",
            phone="(45) 99941-7111",
            role="barber",
        )
        print("[OK] Usuario barbeiro criado: joao@barbearia.com / barber123")
    except:
        barbeiro_user = User.objects.get(email="joao@barbearia.com")
        print("[INFO] Barbeiro ja existe")

    # 3. Criar perfil de barbeiro
    try:
        barbeiro = Barbeiro.objects.create(
            user=barbeiro_user,
            name="João Silva",
            specialty="Cortes clássicos e modernos",
            bio="Barbeiro profissional com mais de 10 anos de experiência",
            phone="(45) 99941-7111",
            active=True,
            working_hours={
                "monday": {"active": True, "start": "08:00", "end": "18:00"},
                "tuesday": {"active": True, "start": "08:00", "end": "18:00"},
                "wednesday": {"active": True, "start": "08:00", "end": "18:00"},
                "thursday": {"active": True, "start": "08:00", "end": "18:00"},
                "friday": {"active": True, "start": "08:00", "end": "19:00"},
                "saturday": {"active": True, "start": "08:00", "end": "16:00"},
                "sunday": {"active": False},
            },
            days_off=[],
        )
        print("[OK] Perfil de barbeiro criado")
    except:
        print("[INFO] Perfil de barbeiro ja existe")

    # 4. Criar serviços
    servicos_data = [
        {
            "name": "Corte Social",
            "description": "Corte clássico e moderno, adaptado ao seu estilo",
            "price": 45.00,
            "duration": 30,
            "category": "haircut",
        },
        {
            "name": "Corte Degradê",
            "description": "Corte moderno com degradê lateral",
            "price": 50.00,
            "duration": 40,
            "category": "haircut",
        },
        {
            "name": "Barba Completa",
            "description": "Aparar e modelar a barba com navalha",
            "price": 35.00,
            "duration": 30,
            "category": "beard",
        },
        {
            "name": "Barba + Desenho",
            "description": "Barba completa com desenho e finalização",
            "price": 40.00,
            "duration": 35,
            "category": "beard",
        },
        {
            "name": "Corte + Barba",
            "description": "Pacote completo: corte e barba",
            "price": 70.00,
            "duration": 60,
            "category": "combo",
        },
        {
            "name": "Corte + Barba + Sobrancelha",
            "description": "Pacote premium completo",
            "price": 85.00,
            "duration": 75,
            "category": "combo",
        },
    ]

    for servico_data in servicos_data:
        try:
            Servico.objects.create(**servico_data, active=True)
            print(f"[OK] Servico criado: {servico_data['name']}")
        except:
            print(f"[INFO] Servico ja existe: {servico_data['name']}")

    # 5. Criar cupons de exemplo
    cupons_data = [
        {
            "code": "BEMVINDO20",
            "discount": 20,
            "discount_type": "percentage",
            "description": "Desconto de 20% para primeira visita",
            "max_uses": 100,
        },
        {
            "code": "FIDELIDADE10",
            "discount": 10,
            "discount_type": "percentage",
            "description": "Desconto de 10% para clientes fiéis",
            "max_uses": 0,  # ilimitado
        },
        {
            "code": "DESCONTO15",
            "discount": 15.00,
            "discount_type": "fixed",
            "description": "R$ 15 de desconto em qualquer serviço",
            "max_uses": 50,
        },
    ]

    for cupom_data in cupons_data:
        try:
            Cupom.objects.create(**cupom_data, active=True)
            print(f"[OK] Cupom criado: {cupom_data['code']}")
        except:
            print(f"[INFO] Cupom ja existe: {cupom_data['code']}")

    # 6. Criar usuário de teste
    try:
        User.objects.create_user(
            email="cliente@teste.com",
            password="cliente123",
            name="Cliente Teste",
            phone="(45) 99999-9999",
            role="user",
        )
        print("[OK] Usuario de teste criado: cliente@teste.com / cliente123")
    except:
        print("[INFO] Usuario de teste ja existe")

    print("\n[SUCCESS] Banco de dados populado com sucesso!")
    print("\n[CREDENCIAIS]")
    print("   Admin: admin@barbearia.com / admin123")
    print("   Barbeiro: joao@barbearia.com / barber123")
    print("   Cliente: cliente@teste.com / cliente123")
    print("\n[PROXIMO PASSO] Rode o servidor: python manage.py runserver")


if __name__ == "__main__":
    populate()
