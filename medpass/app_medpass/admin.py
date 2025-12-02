from django.contrib import admin
from .models import Especialidade, Profissional, Senha, Guiche

# Register your models here.

@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativa', 'criado_em', 'atualizado_em']
    list_filter = ['ativa', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'ativa')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Guiche)
class GuicheAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nome', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['numero', 'nome']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = (
        ('Informações do Guichê', {
            'fields': ('numero', 'nome', 'ativo')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'crm', 'uf_crm', 'especialidade', 'sala', 'ativo', 'criado_em']
    list_filter = ['ativo', 'especialidade', 'uf_crm', 'criado_em']
    search_fields = ['nome', 'crm', 'email']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'crm', 'uf_crm')
        }),
        ('Informações Profissionais', {
            'fields': ('especialidade', 'sala', 'ativo')
        }),
        ('Contato', {
            'fields': ('telefone', 'email'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Senha)
class SenhaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'tipo', 'especialidade', 'status', 'nome_paciente', 'guiche', 'profissional', 'criado_em']
    list_filter = ['status', 'tipo', 'especialidade', 'criado_em']
    search_fields = ['numero', 'nome_paciente']
    readonly_fields = [
        'criado_em', 
        'chamado_guiche_em', 
        'triagem_iniciada_em', 
        'triagem_finalizada_em',
        'chamado_medico_em', 
        'consulta_iniciada_em', 
        'concluido_em'
    ]
    date_hierarchy = 'criado_em'
    fieldsets = (
        ('Informações da Senha', {
            'fields': ('numero', 'tipo', 'especialidade', 'status')
        }),
        ('Paciente', {
            'fields': ('nome_paciente', 'observacoes_triagem')
        }),
        ('Atendimento', {
            'fields': ('guiche', 'profissional')
        }),
        ('Timestamps - Guichê', {
            'fields': ('criado_em', 'chamado_guiche_em', 'triagem_iniciada_em', 'triagem_finalizada_em'),
            'classes': ('collapse',)
        }),
        ('Timestamps - Médico', {
            'fields': ('chamado_medico_em', 'consulta_iniciada_em', 'concluido_em'),
            'classes': ('collapse',)
        }),
    )
