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
    sigla = models.CharField(
        max_length=3,
        unique=True,
        verbose_name="Sigla",
        help_text="Sigla para gerar a senha (ex: C para Cardiologia, P para Pediatria)"
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


class Guiche(models.Model):
    """
    Modelo para armazenar os guichês de atendimento (triagem/recepção).
    """
    numero = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Número do Guichê",
        help_text="Identificação do guichê (ex: G01, G02)"
    )
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Guichê",
        help_text="Nome descritivo do guichê (ex: Guichê de Triagem 1)"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Indica se o guichê está ativo"
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
        verbose_name = "Guichê"
        verbose_name_plural = "Guichês"
        ordering = ['numero']

    def __str__(self):
        return f"{self.numero} - {self.nome}"


class Profissional(models.Model):
    """
    Modelo para armazenar os profissionais de saúde (médicos) cadastrados no sistema.
    Cada médico tem um usuário para login.
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
    sala = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Sala/Consultório",
        help_text="Número da sala ou consultório do médico"
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
        return f"Dr(a). {self.nome} - CRM {self.crm}/{self.uf_crm}"


class Senha(models.Model):
    """
    Modelo para gerenciar as senhas geradas na central de senhas.
    
    Fluxo:
    1. Paciente pega senha → status 'aguardando_guiche'
    2. Guichê chama → status 'chamando_guiche'
    3. Guichê atende (triagem) → status 'em_triagem'
    4. Guichê finaliza triagem → status 'aguardando_medico'
    5. Médico chama → status 'chamando_medico'
    6. Médico atende → status 'em_consulta'
    7. Médico finaliza → status 'concluido'
    """
    TIPO_CHOICES = [
        ('N', 'Normal'),
        ('P', 'Preferencial'),
        ('U', 'Urgência'),
    ]
    
    STATUS_CHOICES = [
        # Etapa 1: Aguardando Guichê
        ('aguardando_guiche', 'Aguardando Guichê'),
        ('chamando_guiche', 'Chamando no Guichê'),
        ('em_triagem', 'Em Triagem'),
        # Etapa 2: Aguardando Médico
        ('aguardando_medico', 'Aguardando Médico'),
        ('chamando_medico', 'Chamando para Consulta'),
        ('em_consulta', 'Em Consulta'),
        # Finalizados
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        ('desistencia', 'Desistência'),
    ]
    
    numero = models.CharField(
        max_length=10,
        verbose_name="Número da Senha",
        help_text="Número da senha gerada (ex: N001, P002, U003)"
    )
    tipo = models.CharField(
        max_length=1,
        choices=TIPO_CHOICES,
        default='N',
        verbose_name="Tipo de Senha",
        help_text="Tipo da senha (Normal, Preferencial, Urgência)"
    )
    especialidade = models.ForeignKey(
        Especialidade,
        on_delete=models.PROTECT,
        related_name='senhas',
        verbose_name="Especialidade",
        help_text="Especialidade para qual a senha foi gerada"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aguardando_guiche',
        verbose_name="Status",
        help_text="Status atual da senha"
    )
    
    # Relacionamentos
    guiche = models.ForeignKey(
        Guiche,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='senhas_atendidas',
        verbose_name="Guichê",
        help_text="Guichê que atendeu/está atendendo"
    )
    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='senhas_atendidas',
        verbose_name="Médico",
        help_text="Médico que está atendendo/atendeu"
    )
    
    # Dados da triagem (preenchido pelo guichê)
    nome_paciente = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Nome do Paciente",
        help_text="Nome do paciente (preenchido na triagem)"
    )
    observacoes_triagem = models.TextField(
        blank=True,
        verbose_name="Observações da Triagem",
        help_text="Observações registradas durante a triagem"
    )
    
    # Timestamps
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    chamado_guiche_em = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Chamado no Guichê em"
    )
    triagem_iniciada_em = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Triagem Iniciada em"
    )
    triagem_finalizada_em = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Triagem Finalizada em"
    )
    chamado_medico_em = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Chamado pelo Médico em"
    )
    consulta_iniciada_em = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Consulta Iniciada em"
    )
    concluido_em = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Conclusão"
    )
    
    class Meta:
        verbose_name = "Senha"
        verbose_name_plural = "Senhas"
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.numero} - {self.get_tipo_display()} - {self.especialidade.nome}"
    
    @classmethod
    def gerar_numero(cls, tipo, especialidade):
        """
        Gera o número da senha no formato: TIPO + SIGLA_ESPECIALIDADE + SEQUENCIAL
        Ex: NC001 (Normal + Cardiologia + 001)
            PD002 (Preferencial + Dermatologia + 002)
            UG003 (Urgência + Clínica Geral + 003)
        """
        from django.utils import timezone
        from django.db.models import Max
        
        hoje = timezone.now().date()
        prefixo = f"{tipo}{especialidade.sigla}"
        
        # Busca o último número do dia para esta combinação
        ultima_senha = cls.objects.filter(
            numero__startswith=prefixo,
            criado_em__date=hoje
        ).aggregate(Max('numero'))['numero__max']
        
        if ultima_senha:
            # Extrai o número sequencial
            try:
                ultimo_seq = int(ultima_senha[len(prefixo):])
                novo_seq = ultimo_seq + 1
            except ValueError:
                novo_seq = 1
        else:
            novo_seq = 1
        
        return f"{prefixo}{novo_seq:03d}"
    
    @property
    def etapa_atual(self):
        """Retorna a etapa atual do atendimento"""
        if self.status in ['aguardando_guiche', 'chamando_guiche', 'em_triagem']:
            return 'guiche'
        elif self.status in ['aguardando_medico', 'chamando_medico', 'em_consulta']:
            return 'medico'
        else:
            return 'finalizado'
