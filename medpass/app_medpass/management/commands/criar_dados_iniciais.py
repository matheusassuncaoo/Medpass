from django.core.management.base import BaseCommand
from app_medpass.models import Especialidade, Profissional, Guiche


class Command(BaseCommand):
    help = 'Cria dados iniciais: 5 especialidades, 5 médicos e 5 guichês'

    def handle(self, *args, **options):
        # Criar Especialidades com siglas
        especialidades_data = [
            {'nome': 'Cardiologia', 'sigla': 'C', 'descricao': 'Especialidade médica que trata do coração e sistema circulatório'},
            {'nome': 'Pediatria', 'sigla': 'P', 'descricao': 'Especialidade médica dedicada ao cuidado de crianças e adolescentes'},
            {'nome': 'Clínica Geral', 'sigla': 'G', 'descricao': 'Atendimento médico geral para adultos'},
            {'nome': 'Ortopedia', 'sigla': 'O', 'descricao': 'Especialidade médica que trata do sistema musculoesquelético'},
            {'nome': 'Dermatologia', 'sigla': 'D', 'descricao': 'Especialidade médica que trata da pele, cabelos e unhas'},
        ]
        
        especialidades_criadas = []
        for esp_data in especialidades_data:
            esp, created = Especialidade.objects.get_or_create(
                nome=esp_data['nome'],
                defaults=esp_data
            )
            especialidades_criadas.append(esp)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Especialidade "{esp.nome}" (sigla: {esp.sigla}) criada'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Especialidade "{esp.nome}" já existe'))
        
        # Criar Médicos
        medicos_data = [
            {'nome': 'Dr. João Silva', 'crm': '12345', 'uf_crm': 'MT', 'especialidade': especialidades_criadas[0], 'sala': '101'},
            {'nome': 'Dra. Maria Santos', 'crm': '23456', 'uf_crm': 'MT', 'especialidade': especialidades_criadas[1], 'sala': '102'},
            {'nome': 'Dr. Pedro Oliveira', 'crm': '34567', 'uf_crm': 'MT', 'especialidade': especialidades_criadas[2], 'sala': '103'},
            {'nome': 'Dra. Ana Costa', 'crm': '45678', 'uf_crm': 'MT', 'especialidade': especialidades_criadas[3], 'sala': '104'},
            {'nome': 'Dr. Carlos Pereira', 'crm': '56789', 'uf_crm': 'MT', 'especialidade': especialidades_criadas[4], 'sala': '105'},
        ]
        
        for med_data in medicos_data:
            med, created = Profissional.objects.get_or_create(
                crm=med_data['crm'],
                uf_crm=med_data['uf_crm'],
                defaults=med_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Médico "{med.nome}" criado'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Médico "{med.nome}" já existe'))
        
        # Criar Guichês
        guiches_data = [
            {'numero': '01', 'nome': 'Triagem 1'},
            {'numero': '02', 'nome': 'Triagem 2'},
            {'numero': '03', 'nome': 'Triagem 3'},
            {'numero': '04', 'nome': 'Triagem 4'},
            {'numero': '05', 'nome': 'Triagem 5'},
        ]
        
        for guiche_data in guiches_data:
            g, created = Guiche.objects.get_or_create(
                numero=guiche_data['numero'],
                defaults=guiche_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Guichê "{g.numero}" criado'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Guichê "{g.numero}" já existe'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Dados iniciais criados com sucesso!'))
        self.stdout.write(self.style.SUCCESS('\n📝 Formato das senhas:'))
        self.stdout.write('   NC001 = Normal + Cardiologia')
        self.stdout.write('   PC001 = Preferencial + Cardiologia')
        self.stdout.write('   UC001 = Urgência + Cardiologia')
        self.stdout.write('   ND001 = Normal + Dermatologia')
        self.stdout.write('   PD001 = Preferencial + Dermatologia')
        self.stdout.write('   etc...')
