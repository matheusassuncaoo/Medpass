from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Especialidade(models.Model):
    """
    Modelo para armazenar as especialidades médicas disponíveis no sistema.
    """
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome da Especialidade",
        help_text="Nome da especialidade médica (ex: Cardiologia, Pediatria)"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição detalhada da especialidade"
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name="Ativa",
        help_text="Indica se a especialidade está ativa no sistema"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )

    class Meta:
        verbose_name = "Especialidade"
        verbose_name_plural = "Especialidades"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Profissional(models.Model):
    """
    Modelo para armazenar os profissionais de saúde cadastrados no sistema.
    """
    # Validador para CRM (somente números, de 4 a 8 dígitos)
    crm_validator = RegexValidator(
        regex=r'^\d{4,8}$',
        message='CRM deve conter entre 4 e 8 dígitos numéricos'
    )

    nome = models.CharField(
        max_length=200,
        verbose_name="Nome Completo",
        help_text="Nome completo do profissional de saúde"
    )
    crm = models.CharField(
        max_length=8,
        validators=[crm_validator],
        verbose_name="CRM",
        help_text="Número do CRM (Conselho Regional de Medicina)"
    )
    uf_crm = models.CharField(
        max_length=2,
        verbose_name="UF do CRM",
        help_text="Estado do CRM (ex: MT, SP, RJ)",
        default="MT"
    )
    especialidade = models.ForeignKey(
        Especialidade,
        on_delete=models.PROTECT,
        related_name='profissionais',
        verbose_name="Especialidade",
        help_text="Especialidade médica do profissional"
    )
    telefone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="Telefone",
        help_text="Telefone de contato"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail",
        help_text="E-mail de contato"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Indica se o profissional está ativo no sistema"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )

    class Meta:
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"
        ordering = ['nome']
        unique_together = [['crm', 'uf_crm']]

    def __str__(self):
        return f"{self.nome} - CRM {self.crm}/{self.uf_crm}"
