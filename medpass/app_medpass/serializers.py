from rest_framework import serializers
from .models import Especialidade, Profissional, Senha


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = ['id', 'nome', 'descricao', 'ativo', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']


class ProfissionalSerializer(serializers.ModelSerializer):
    especialidade_nome = serializers.CharField(source='especialidade.nome', read_only=True)
    
    class Meta:
        model = Profissional
        fields = ['id', 'nome', 'crm', 'especialidade', 'especialidade_nome', 
                  'telefone', 'email', 'ativo', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']


class SenhaSerializer(serializers.ModelSerializer):
    especialidade_nome = serializers.CharField(source='especialidade.nome', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Senha
        fields = ['id', 'numero', 'especialidade', 'especialidade_nome', 
                  'tipo', 'tipo_display', 'status', 'status_display',
                  'guiche', 'criado_em', 'chamado_em', 'atendido_em', 
                  'finalizado_em', 'atualizado_em']
        read_only_fields = ['numero', 'criado_em', 'chamado_em', 'atendido_em', 
                           'finalizado_em', 'atualizado_em']


class SenhaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Senha
        fields = ['especialidade', 'tipo']
        
    def create(self, validated_data):
        # Gera o número da senha automaticamente
        from datetime import date
        especialidade = validated_data['especialidade']
        tipo = validated_data.get('tipo', 'normal')
        
        # Contar senhas da especialidade no dia
        hoje = date.today()
        count = Senha.objects.filter(
            especialidade=especialidade,
            criado_em__date=hoje
        ).count() + 1
        
        # Formato: SIGLA + TIPO + NUMERO (ex: CAR-N-001)
        sigla = especialidade.nome[:3].upper()
        tipo_letra = 'P' if tipo == 'prioritario' else 'N'
        numero = f"{sigla}-{tipo_letra}-{count:03d}"
        
        senha = Senha.objects.create(
            numero=numero,
            **validated_data
        )
        return senha


class SenhaChamarSerializer(serializers.Serializer):
    guiche = serializers.IntegerField(min_value=1, max_value=99)


class SenhaStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['aguardando', 'chamando', 'atendimento', 'finalizado'])
