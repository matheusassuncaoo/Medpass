from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import date
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Especialidade, Profissional, Senha, Guiche
from .serializers import (
    EspecialidadeSerializer, 
    ProfissionalSerializer, 
    SenhaSerializer,
    SenhaCreateSerializer,
    SenhaChamarSerializer,
    SenhaStatusSerializer,
    GuicheSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="Listar Especialidades",
        description="Retorna a lista de todas as especialidades médicas cadastradas no sistema.",
        tags=['Especialidades']
    ),
    create=extend_schema(
        summary="Criar Especialidade",
        description="Cadastra uma nova especialidade médica no sistema.",
        tags=['Especialidades']
    ),
    retrieve=extend_schema(
        summary="Obter Especialidade",
        description="Retorna os detalhes de uma especialidade específica.",
        tags=['Especialidades']
    ),
    update=extend_schema(
        summary="Atualizar Especialidade",
        description="Atualiza completamente uma especialidade existente.",
        tags=['Especialidades']
    ),
    partial_update=extend_schema(
        summary="Atualizar Parcialmente Especialidade",
        description="Atualiza parcialmente uma especialidade existente.",
        tags=['Especialidades']
    ),
    destroy=extend_schema(
        summary="Deletar Especialidade",
        description="Remove uma especialidade do sistema.",
        tags=['Especialidades']
    ),
)
class EspecialidadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Especialidades Médicas.
    
    Permite operações CRUD completas para especialidades médicas.
    """
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    
    @extend_schema(
        summary="Listar Especialidades Ativas",
        description="Retorna apenas as especialidades que estão ativas no sistema.",
        tags=['Especialidades']
    )
    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """Retorna apenas especialidades ativas"""
        especialidades = self.queryset.filter(ativa=True)
        serializer = self.get_serializer(especialidades, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Listar Guichês",
        description="Retorna a lista de todos os guichês cadastrados.",
        tags=['Guichês']
    ),
    create=extend_schema(
        summary="Criar Guichê",
        description="Cadastra um novo guichê no sistema.",
        tags=['Guichês']
    ),
    retrieve=extend_schema(
        summary="Obter Guichê",
        description="Retorna os detalhes de um guichê específico.",
        tags=['Guichês']
    ),
)
class GuicheViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Guichês.
    """
    queryset = Guiche.objects.all()
    serializer_class = GuicheSerializer
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Retorna apenas guichês ativos"""
        guiches = self.queryset.filter(ativo=True)
        serializer = self.get_serializer(guiches, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Listar Profissionais",
        description="Retorna a lista de todos os profissionais de saúde cadastrados.",
        tags=['Profissionais']
    ),
    create=extend_schema(
        summary="Criar Profissional",
        description="Cadastra um novo profissional de saúde no sistema.",
        tags=['Profissionais']
    ),
    retrieve=extend_schema(
        summary="Obter Profissional",
        description="Retorna os detalhes de um profissional específico.",
        tags=['Profissionais']
    ),
    update=extend_schema(
        summary="Atualizar Profissional",
        description="Atualiza completamente um profissional existente.",
        tags=['Profissionais']
    ),
    partial_update=extend_schema(
        summary="Atualizar Parcialmente Profissional",
        description="Atualiza parcialmente um profissional existente.",
        tags=['Profissionais']
    ),
    destroy=extend_schema(
        summary="Deletar Profissional",
        description="Remove um profissional do sistema.",
        tags=['Profissionais']
    ),
)
class ProfissionalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Profissionais de Saúde.
    
    Permite operações CRUD completas para profissionais médicos.
    """
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    
    @extend_schema(
        summary="Listar Profissionais Ativos",
        description="Retorna apenas os profissionais que estão ativos no sistema.",
        tags=['Profissionais']
    )
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Retorna apenas profissionais ativos"""
        profissionais = self.queryset.filter(ativo=True)
        serializer = self.get_serializer(profissionais, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Listar Profissionais por Especialidade",
        description="Retorna profissionais filtrados por especialidade específica.",
        parameters=[
            OpenApiParameter(
                name='especialidade_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='ID da especialidade para filtrar',
                required=True
            ),
        ],
        tags=['Profissionais']
    )
    @action(detail=False, methods=['get'])
    def por_especialidade(self, request):
        """Retorna profissionais filtrados por especialidade"""
        especialidade_id = request.query_params.get('especialidade_id')
        if not especialidade_id:
            return Response(
                {'error': 'especialidade_id é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profissionais = self.queryset.filter(
            especialidade_id=especialidade_id,
            ativo=True
        )
        serializer = self.get_serializer(profissionais, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Listar Senhas",
        description="Retorna a lista de todas as senhas do sistema.",
        tags=['Senhas']
    ),
    create=extend_schema(
        summary="Gerar Nova Senha",
        description="Gera uma nova senha para atendimento. O número da senha é gerado automaticamente.",
        tags=['Senhas'],
    ),
    retrieve=extend_schema(
        summary="Obter Senha",
        description="Retorna os detalhes de uma senha específica.",
        tags=['Senhas']
    ),
    update=extend_schema(
        summary="Atualizar Senha",
        description="Atualiza completamente uma senha existente.",
        tags=['Senhas']
    ),
    partial_update=extend_schema(
        summary="Atualizar Parcialmente Senha",
        description="Atualiza parcialmente uma senha existente.",
        tags=['Senhas']
    ),
    destroy=extend_schema(
        summary="Deletar Senha",
        description="Remove uma senha do sistema.",
        tags=['Senhas']
    ),
)
class SenhaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento do Sistema de Senhas.
    
    Fluxo de atendimento:
    1. Paciente pega senha (aguardando_guiche)
    2. Guichê chama (chamando_guiche)
    3. Guichê faz triagem (em_triagem)
    4. Paciente aguarda médico (aguardando_medico)
    5. Médico chama (chamando_medico)
    6. Médico atende (em_consulta)
    7. Consulta finalizada (concluido)
    """
    queryset = Senha.objects.all().select_related('especialidade', 'guiche', 'profissional')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SenhaCreateSerializer
        return SenhaSerializer
    
    # =====================
    # Consultas de Status
    # =====================
    
    @extend_schema(summary="Senhas Aguardando Guichê", tags=['Senhas'])
    @action(detail=False, methods=['get'])
    def aguardando_guiche(self, request):
        """Retorna senhas aguardando triagem no guichê"""
        senhas = self.queryset.filter(status='aguardando_guiche').order_by('criado_em')
        serializer = self.get_serializer(senhas, many=True)
        return Response(serializer.data)
    
    @extend_schema(summary="Senhas Aguardando Médico", tags=['Senhas'])
    @action(detail=False, methods=['get'])
    def aguardando_medico(self, request):
        """Retorna senhas aguardando consulta médica"""
        especialidade_id = request.query_params.get('especialidade_id')
        senhas = self.queryset.filter(status='aguardando_medico')
        if especialidade_id:
            senhas = senhas.filter(especialidade_id=especialidade_id)
        senhas = senhas.order_by('triagem_finalizada_em')
        serializer = self.get_serializer(senhas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def em_atendimento(self, request):
        """Retorna senhas em atendimento (triagem ou consulta)"""
        senhas = self.queryset.filter(
            status__in=['chamando_guiche', 'em_triagem', 'chamando_medico', 'em_consulta']
        ).order_by('-chamado_guiche_em', '-chamado_medico_em')
        serializer = self.get_serializer(senhas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def finalizadas(self, request):
        """Retorna senhas finalizadas"""
        senhas = self.queryset.filter(status='concluido').order_by('-concluido_em')
        serializer = self.get_serializer(senhas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def hoje(self, request):
        """Retorna senhas geradas hoje"""
        hoje = date.today()
        senhas = self.queryset.filter(criado_em__date=hoje).order_by('-criado_em')
        serializer = self.get_serializer(senhas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas das senhas"""
        hoje = date.today()
        
        return Response({
            'total_hoje': self.queryset.filter(criado_em__date=hoje).count(),
            'aguardando_guiche': self.queryset.filter(status='aguardando_guiche').count(),
            'em_triagem': self.queryset.filter(status__in=['chamando_guiche', 'em_triagem']).count(),
            'aguardando_medico': self.queryset.filter(status='aguardando_medico').count(),
            'em_consulta': self.queryset.filter(status__in=['chamando_medico', 'em_consulta']).count(),
            'finalizadas_hoje': self.queryset.filter(status='concluido', concluido_em__date=hoje).count(),
            'data': hoje.isoformat()
        })
    
    # =====================
    # Ações do Guichê
    # =====================
    
    @action(detail=True, methods=['post'])
    def chamar_guiche(self, request, pk=None):
        """Guichê chama uma senha para triagem"""
        senha = self.get_object()
        
        if senha.status != 'aguardando_guiche':
            return Response(
                {'error': 'Senha não está aguardando guichê'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        guiche_id = request.data.get('guiche_id')
        if guiche_id:
            try:
                guiche = Guiche.objects.get(id=guiche_id)
                senha.guiche = guiche
            except Guiche.DoesNotExist:
                pass
        
        senha.status = 'chamando_guiche'
        senha.chamado_guiche_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    @action(detail=True, methods=['post'])
    def iniciar_triagem(self, request, pk=None):
        """Inicia a triagem no guichê"""
        senha = self.get_object()
        
        if senha.status != 'chamando_guiche':
            return Response(
                {'error': 'Senha não está sendo chamada no guichê'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        senha.status = 'em_triagem'
        senha.triagem_iniciada_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    @action(detail=True, methods=['post'])
    def finalizar_triagem(self, request, pk=None):
        """Finaliza a triagem e envia para o médico"""
        senha = self.get_object()
        
        if senha.status != 'em_triagem':
            return Response(
                {'error': 'Senha não está em triagem'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualiza dados do paciente se fornecidos
        senha.nome_paciente = request.data.get('nome_paciente', senha.nome_paciente)
        senha.observacoes_triagem = request.data.get('observacoes', senha.observacoes_triagem)
        senha.status = 'aguardando_medico'
        senha.triagem_finalizada_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    # =====================
    # Ações do Médico
    # =====================
    
    @action(detail=True, methods=['post'])
    def chamar_medico(self, request, pk=None):
        """Médico chama o paciente para consulta"""
        senha = self.get_object()
        
        if senha.status != 'aguardando_medico':
            return Response(
                {'error': 'Paciente não está aguardando médico'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profissional_id = request.data.get('profissional_id')
        if profissional_id:
            try:
                profissional = Profissional.objects.get(id=profissional_id)
                senha.profissional = profissional
            except Profissional.DoesNotExist:
                pass
        
        senha.status = 'chamando_medico'
        senha.chamado_medico_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    @action(detail=True, methods=['post'])
    def iniciar_consulta(self, request, pk=None):
        """Inicia a consulta médica"""
        senha = self.get_object()
        
        if senha.status != 'chamando_medico':
            return Response(
                {'error': 'Paciente não está sendo chamado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        senha.status = 'em_consulta'
        senha.consulta_iniciada_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    @action(detail=True, methods=['post'])
    def finalizar_consulta(self, request, pk=None):
        """Finaliza a consulta médica"""
        senha = self.get_object()
        
        if senha.status != 'em_consulta':
            return Response(
                {'error': 'Paciente não está em consulta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        senha.status = 'concluido'
        senha.concluido_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    # =====================
    # Ações Gerais
    # =====================
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancela uma senha"""
        senha = self.get_object()
        
        if senha.status == 'concluido':
            return Response(
                {'error': 'Senha já foi finalizada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        senha.status = 'cancelado'
        senha.concluido_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    @action(detail=True, methods=['post'])
    def desistencia(self, request, pk=None):
        """Marca a senha como desistência"""
        senha = self.get_object()
        
        if senha.status == 'concluido':
            return Response(
                {'error': 'Senha já foi finalizada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        senha.status = 'desistencia'
        senha.concluido_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    @action(detail=False, methods=['get'])
    def painel(self, request):
        """Retorna dados para o painel de senhas"""
        hoje = date.today()
        
        # Senhas sendo chamadas
        senha_chamando_guiche = self.queryset.filter(
            status='chamando_guiche'
        ).order_by('-chamado_guiche_em').first()
        
        senha_chamando_medico = self.queryset.filter(
            status='chamando_medico'
        ).order_by('-chamado_medico_em').first()
        
        # Últimas senhas chamadas
        ultimas_chamadas = self.queryset.filter(
            status__in=['em_triagem', 'em_consulta', 'concluido'],
        ).order_by('-chamado_guiche_em', '-chamado_medico_em')[:5]
        
        # Senhas aguardando
        senhas_aguardando_guiche = self.queryset.filter(
            status='aguardando_guiche'
        ).order_by('criado_em')[:10]
        
        senhas_aguardando_medico = self.queryset.filter(
            status='aguardando_medico'
        ).order_by('triagem_finalizada_em')[:10]
        
        # Estatísticas
        total_hoje = self.queryset.filter(criado_em__date=hoje).count()
        total_atendidas = self.queryset.filter(status='concluido', concluido_em__date=hoje).count()
        
        return Response({
            'senha_chamando_guiche': SenhaSerializer(senha_chamando_guiche).data if senha_chamando_guiche else None,
            'senha_chamando_medico': SenhaSerializer(senha_chamando_medico).data if senha_chamando_medico else None,
            'ultimas_chamadas': SenhaSerializer(ultimas_chamadas, many=True).data,
            'senhas_aguardando_guiche': SenhaSerializer(senhas_aguardando_guiche, many=True).data,
            'senhas_aguardando_medico': SenhaSerializer(senhas_aguardando_medico, many=True).data,
            'estatisticas': {
                'total_hoje': total_hoje,
                'total_atendidas': total_atendidas,
                'aguardando_guiche': self.queryset.filter(status='aguardando_guiche').count(),
                'aguardando_medico': self.queryset.filter(status='aguardando_medico').count(),
            }
        })
