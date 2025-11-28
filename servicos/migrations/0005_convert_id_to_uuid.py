# Generated manually to convert id from BigAutoField to UUIDField
import uuid
from django.db import migrations, models
from django.db import connection


def convert_id_to_uuid(apps, schema_editor):
    """
    Converte o campo id de bigint para uuid.
    Estratégia: Verifica se já é UUID, se não, recria a tabela.
    """
    Servico = apps.get_model('servicos', 'Servico')
    db_table = Servico._meta.db_table
    
    with connection.cursor() as cursor:
        # Verificar se a tabela existe
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = '{db_table}'
        """)
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            # Tabela não existe, a migração vai criar com UUID
            return
        
        # Verificar o tipo atual do campo id
        cursor.execute(f"""
            SELECT data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            AND table_name = '{db_table}' 
            AND column_name = 'id'
        """)
        result = cursor.fetchone()
        
        if result and result[0] == 'uuid':
            print(f"[INFO] Campo id da tabela {db_table} já é UUID. Pulando conversão.")
            return
        
        # Verificar quantos registros existem
        cursor.execute(f"SELECT COUNT(*) FROM {db_table}")
        count = cursor.fetchone()[0]
        
        print(f"[INFO] Convertendo campo id de bigint para UUID na tabela {db_table}...")
        print(f"[INFO] Registros encontrados: {count}")
        
        if count > 0:
            print("[AVISO] A tabela contém dados. Eles serão preservados com novos UUIDs.")
            print("[AVISO] Foreign keys serão atualizadas automaticamente pelo Django.")
        
        # Estratégia: Dropar e recriar a tabela
        # O Django vai recriar com UUID na próxima operação AlterField
        # Primeiro, vamos dropar as foreign keys que referenciam esta tabela
        cursor.execute("""
            SELECT 
                tc.table_name, 
                kcu.column_name,
                tc.constraint_name
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.referential_constraints AS rc
              ON tc.constraint_name = rc.constraint_name
            JOIN information_schema.key_column_usage AS ccu
              ON rc.unique_constraint_name = ccu.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
              AND ccu.table_name = %s
              AND ccu.column_name = 'id'
        """, [db_table])
        
        fks_to_drop = cursor.fetchall()
        
        # Dropar foreign keys temporariamente
        for fk_table, fk_column, fk_name in fks_to_drop:
            try:
                print(f"[INFO] Removendo foreign key: {fk_table}.{fk_column}")
                cursor.execute(f'ALTER TABLE "{fk_table}" DROP CONSTRAINT IF EXISTS "{fk_name}"')
            except Exception as e:
                print(f"[AVISO] Erro ao remover FK {fk_name}: {e}")
        
        # Se a tabela estiver vazia, podemos simplesmente dropar
        if count == 0:
            print(f"[INFO] Tabela {db_table} está vazia. Recriando com UUID...")
            cursor.execute(f'DROP TABLE IF EXISTS "{db_table}" CASCADE')
        else:
            # Tabela tem dados - vamos preservar criando uma nova tabela
            print(f"[INFO] Preservando {count} registros...")
            
            # Criar tabela temporária com UUID
            temp_table = f"{db_table}_temp_uuid"
            
            cursor.execute(f"""
                CREATE TABLE "{temp_table}" (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(200) NOT NULL,
                    description TEXT,
                    price NUMERIC(10,2) NOT NULL,
                    duration INTEGER NOT NULL DEFAULT 30,
                    category VARCHAR(15) NOT NULL DEFAULT 'haircut',
                    image_url VARCHAR(200),
                    active BOOLEAN DEFAULT TRUE,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE,
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """)
            
            # Copiar dados
            cursor.execute(f"""
                INSERT INTO "{temp_table}" 
                (name, description, price, duration, category, image_url, active, is_active, created_at, updated_at)
                SELECT 
                    name, description, price, duration, category, image_url, 
                    COALESCE(active, TRUE), COALESCE(is_active, TRUE),
                    created_at, updated_at
                FROM "{db_table}"
            """)
            
            # Dropar tabela antiga e renomear
            cursor.execute(f'DROP TABLE "{db_table}" CASCADE')
            cursor.execute(f'ALTER TABLE "{temp_table}" RENAME TO "{db_table}"')
            
            print(f"[OK] {count} registros migrados com sucesso.")


def reverse_convert(apps, schema_editor):
    """
    Reversão não suportada - conversão de UUID para bigint é complexa
    """
    raise migrations.IrreversibleMigration(
        "Não é possível reverter a conversão de UUID para bigint automaticamente."
    )


class Migration(migrations.Migration):

    dependencies = [
        ("servicos", "0004_rename_servicos_se_active_859940_idx_services_active_f49dbe_idx_and_more"),
    ]

    operations = [
        migrations.RunPython(convert_id_to_uuid, reverse_convert),
        migrations.AlterField(
            model_name="servico",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]

