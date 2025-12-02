from rest_framework import serializers
from .models import Especialidade, Profissional, Senha, Guiche


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = ['id', 'nome', 'descricao', 'ativa', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']


class GuicheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guiche
        fields = ['id', 'numero', 'nome', 'ativo', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']


class ProfissionalSerializer(serializers.ModelSerializer):
    especialidade_nome = serializers.CharField(source='especialidade.nome', read_only=True)
    
    class Meta:
        model = Profissional
        fields = ['id', 'nome', 'crm', 'uf_crm', 'especialidade', 'especialidade_nome', 
                  'sala', 'telefone', 'email', 'ativo', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']


class SenhaSerializer(serializers.ModelSerializer):
    especialidade_nome = serializers.CharField(source='especialidade.nome', read_only=True)
    guiche_numero = serializers.CharField(source='guiche.numero', read_only=True, allow_null=True)
    profissional_nome = serializers.CharField(source='profissional.nome', read_only=True, allow_null=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    etapa_atual = serializers.CharField(read_only=True)
    
    class Meta:
        model = Senha
        fields = [
            'id', 'numero', 'especialidade', 'especialidade_nome', 
            'tipo', 'tipo_display', 'status', 'status_display', 'etapa_atual',
            'guiche', 'guiche_numero', 'profissional', 'profissional_nome',
            'nome_paciente', 'observacoes_triagem',
            'criado_em', 'chamado_guiche_em', 'triagem_iniciada_em', 'triagem_finalizada_em',
            'chamado_medico_em', 'consulta_iniciada_em', 'concluido_em'
        ]
        read_only_fields = [
            'numero', 'criado_em', 'chamado_guiche_em', 'triagem_iniciada_em', 
            'triagem_finalizada_em', 'chamado_medico_em', 'consulta_iniciada_em', 'concluido_em'
        ]


class SenhaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Senha
        fields = ['especialidade', 'tipo']
        
    def create(self, validated_data):
        # Gera o número da senha automaticamente
        from datetime import date
        especialidade = validated_data['especialidade']
        tipo = validated_data.get('tipo', 'N')
        
        # Contar senhas do tipo no dia
        hoje = date.today()
        count = Senha.objects.filter(
            tipo=tipo,
            criado_em__date=hoje
        ).count() + 1
        
        # Formato: TIPO + NUMERO (ex: N001, P002, U003)
        numero = f"{tipo}{count:03d}"
        
        senha = Senha.objects.create(
            numero=numero,
            status='aguardando_guiche',
            **validated_data
        )
        return senha


class SenhaChamarSerializer(serializers.Serializer):
    guiche = serializers.CharField(max_length=10)


class SenhaStatusSerializer(serializers.Serializer):
    STATUS_CHOICES = [
        'aguardando_guiche', 'chamando_guiche', 'em_triagem',
        'aguardando_medico', 'chamando_medico', 'em_consulta',
        'concluido', 'cancelado', 'desistencia'
    ]
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
