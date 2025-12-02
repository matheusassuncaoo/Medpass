# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_medpass', '0003_update_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='especialidade',
            name='sigla',
            field=models.CharField(
                default='X',
                help_text='Sigla para gerar a senha (ex: C para Cardiologia, P para Pediatria)',
                max_length=3,
                unique=True,
                verbose_name='Sigla'
            ),
            preserve_default=False,
        ),
    ]

