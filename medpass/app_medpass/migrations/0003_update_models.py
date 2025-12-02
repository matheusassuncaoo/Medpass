# Generated manually to update models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_medpass', '0002_senha'),
    ]

    operations = [
        # Remove campos antigos da Senha
        migrations.RemoveField(
            model_name='senha',
            name='atendido_em',
        ),
        migrations.RemoveField(
            model_name='senha',
            name='chamado_em',
        ),
        migrations.RemoveField(
            model_name='senha',
            name='guiche',
        ),
        
        # Adiciona campo sala no Profissional
        migrations.AddField(
            model_name='profissional',
            name='sala',
            field=models.CharField(blank=True, max_length=20, verbose_name='Sala/Consultório'),
        ),
        
        # Adiciona novos campos na Senha
        migrations.AddField(
            model_name='senha',
            name='chamado_guiche_em',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Chamado no Guichê em'),
        ),
        migrations.AddField(
            model_name='senha',
            name='chamado_medico_em',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Chamado pelo Médico em'),
        ),
        migrations.AddField(
            model_name='senha',
            name='consulta_iniciada_em',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Consulta Iniciada em'),
        ),
        migrations.AddField(
            model_name='senha',
            name='nome_paciente',
            field=models.CharField(blank=True, max_length=200, verbose_name='Nome do Paciente'),
        ),
        migrations.AddField(
            model_name='senha',
            name='observacoes_triagem',
            field=models.TextField(blank=True, verbose_name='Observações da Triagem'),
        ),
        migrations.AddField(
            model_name='senha',
            name='triagem_finalizada_em',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Triagem Finalizada em'),
        ),
        migrations.AddField(
            model_name='senha',
            name='triagem_iniciada_em',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Triagem Iniciada em'),
        ),
        
        # Altera o campo status da Senha
        migrations.AlterField(
            model_name='senha',
            name='status',
            field=models.CharField(
                choices=[
                    ('aguardando_guiche', 'Aguardando Guichê'),
                    ('chamando_guiche', 'Chamando no Guichê'),
                    ('em_triagem', 'Em Triagem'),
                    ('aguardando_medico', 'Aguardando Médico'),
                    ('chamando_medico', 'Chamando para Consulta'),
                    ('em_consulta', 'Em Consulta'),
                    ('concluido', 'Concluído'),
                    ('cancelado', 'Cancelado'),
                    ('desistencia', 'Desistência'),
                ],
                default='aguardando_guiche',
                max_length=20,
                verbose_name='Status'
            ),
        ),
        
        # Cria modelo Guiche
        migrations.CreateModel(
            name='Guiche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, unique=True, verbose_name='Número do Guichê')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome do Guichê')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
            ],
            options={
                'verbose_name': 'Guichê',
                'verbose_name_plural': 'Guichês',
                'ordering': ['numero'],
            },
        ),
        
        # Adiciona o campo guiche como ForeignKey
        migrations.AddField(
            model_name='senha',
            name='guiche',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='senhas_atendidas',
                to='app_medpass.guiche',
                verbose_name='Guichê'
            ),
        ),
    ]
