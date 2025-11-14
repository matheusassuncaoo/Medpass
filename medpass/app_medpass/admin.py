from django.contrib import admin
from .models import Especialidade, Profissional, Senha

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


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'crm', 'uf_crm', 'especialidade', 'ativo', 'criado_em']
    list_filter = ['ativo', 'especialidade', 'uf_crm', 'criado_em']
    search_fields = ['nome', 'crm', 'email']
    readonly_fields = ['criado_em', 'atualizado_em']
    autocomplete_fields = []
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'crm', 'uf_crm')
        }),
        ('Informações Profissionais', {
            'fields': ('especialidade', 'ativo')
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
    list_display = ['numero', 'tipo', 'especialidade', 'status', 'guiche', 'profissional', 'criado_em']
    list_filter = ['status', 'tipo', 'especialidade', 'criado_em']
    search_fields = ['numero', 'guiche']
    readonly_fields = ['criado_em', 'chamado_em', 'atendido_em', 'concluido_em']
    autocomplete_fields = []
    date_hierarchy = 'criado_em'
    fieldsets = (
        ('Informações da Senha', {
            'fields': ('numero', 'tipo', 'especialidade', 'status')
        }),
        ('Atendimento', {
            'fields': ('profissional', 'guiche')
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'chamado_em', 'atendido_em', 'concluido_em'),
            'classes': ('collapse',)
        }),
    )
