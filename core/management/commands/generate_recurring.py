"""
Comando Django para gerar agendamentos recorrentes
Uso: python manage.py generate_recurring [--days=7]
"""
from django.core.management.base import BaseCommand
from core.recurring_scheduler import generate_recurring_appointments, get_recurring_stats


class Command(BaseCommand):
    help = 'Gera agendamentos a partir de recorrências ativas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Número de dias à frente para gerar agendamentos (padrão: 7)'
        )
        
        parser.add_argument(
            '--stats-only',
            action='store_true',
            help='Apenas mostrar estatísticas sem gerar agendamentos'
        )

    def handle(self, *args, **options):
        days_ahead = options['days']
        stats_only = options['stats_only']
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Sistema de Agendamentos Recorrentes'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        if stats_only:
            # Apenas mostrar estatísticas
            stats = get_recurring_stats()
            self.stdout.write('\n📊 Estatísticas:')
            self.stdout.write(f"  Total de recorrências: {stats['total_recurring']}")
            self.stdout.write(f"  Recorrências ativas: {stats['active_recurring']}")
            self.stdout.write(f"  Recorrências inativas: {stats['inactive_recurring']}")
            self.stdout.write(f"  Agendamentos futuros: {stats['future_appointments']}")
            return
        
        self.stdout.write(f'\n🔄 Gerando agendamentos para os próximos {days_ahead} dias...\n')
        
        try:
            result = generate_recurring_appointments(days_ahead=days_ahead)
            
            self.stdout.write('\n✅ Geração concluída!\n')
            self.stdout.write(f"📋 Recorrências processadas: {result['processed']}")
            self.stdout.write(f"✅ Agendamentos criados: {result['created']}")
            self.stdout.write(f"⏭️  Agendamentos ignorados (já existentes): {result['skipped']}")
            self.stdout.write(f"🔒 Recorrências desativadas (expiradas): {result['deactivated']}")
            
            if result['errors'] > 0:
                self.stdout.write(self.style.ERROR(f"❌ Erros: {result['errors']}"))
            
            self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Erro ao gerar agendamentos: {str(e)}'))
            raise

