from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import date, timedelta
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Especialidade, Profissional, Senha
from .serializers import (
    EspecialidadeSerializer, 
    ProfissionalSerializer, 
    SenhaSerializer,
    SenhaCreateSerializer,
    SenhaChamarSerializer,
    SenhaStatusSerializer
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
        description="Gera uma nova senha para atendimento. O número da senha é gerado automaticamente no formato: SIGLA-TIPO-NÚMERO (ex: CAR-N-001).",
        tags=['Senhas'],
        examples=[
            OpenApiExample(
                'Senha Normal',
                value={
                    'especialidade': 1,
                    'tipo': 'normal'
                },
                request_only=True,
            ),
            OpenApiExample(
                'Senha Prioritária',
                value={
                    'especialidade': 1,
                    'tipo': 'prioritario'
                },
                request_only=True,
            ),
        ]
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
    
    Permite operações completas de gerenciamento de senhas, incluindo
    geração, chamada, atendimento e finalização.
    """
    queryset = Senha.objects.all().select_related('especialidade')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SenhaCreateSerializer
        return SenhaSerializer
    
    @extend_schema(
        summary="Senhas Aguardando",
        description="Retorna todas as senhas que estão aguardando serem chamadas, ordenadas por ordem de chegada.",
        tags=['Senhas']
    )
    @action(detail=False, methods=['get'])
    def aguardando(self, request):
        """Retorna senhas aguardando atendimento"""
        senhas = self.queryset.filter(status='aguardando').order_by('criado_em')
        serializer = self.get_serializer(senhas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def chamando(self, request):
        """Retorna senhas sendo chamadas"""
        senhas = self.queryset.filter(status='chamando').order_by('-chamado_em')
        serializer = self.get_serializer(senhas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def em_atendimento(self, request):
        """Retorna senhas em atendimento"""
        senhas = self.queryset.filter(status='atendendo').order_by('-atendido_em')
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
        
        total_hoje = self.queryset.filter(criado_em__date=hoje).count()
        aguardando = self.queryset.filter(status='aguardando').count()
        chamando = self.queryset.filter(status='chamando').count()
        em_atendimento = self.queryset.filter(status='atendendo').count()
        finalizadas_hoje = self.queryset.filter(
            status='concluido',
            concluido_em__date=hoje
        ).count()
        
        return Response({
            'total_hoje': total_hoje,
            'aguardando': aguardando,
            'chamando': chamando,
            'em_atendimento': em_atendimento,
            'finalizadas_hoje': finalizadas_hoje,
            'data': hoje.isoformat()
        })
    
    @action(detail=True, methods=['post'])
    def chamar(self, request, pk=None):
        """Chama uma senha para atendimento"""
        senha = self.get_object()
        serializer = SenhaChamarSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if senha.status != 'aguardando':
            return Response(
                {'error': 'Senha não está aguardando'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        senha.status = 'chamando'
        senha.guiche = serializer.validated_data['guiche']
        senha.chamado_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    @action(detail=True, methods=['post'])
    def iniciar_atendimento(self, request, pk=None):
        """Inicia o atendimento de uma senha"""
        senha = self.get_object()
        
        if senha.status != 'chamando':
            return Response(
                {'error': 'Senha não está sendo chamada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        senha.status = 'atendendo'
        senha.atendido_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        """Finaliza o atendimento de uma senha"""
        senha = self.get_object()
        
        if senha.status not in ['chamando', 'atendendo']:
            return Response(
                {'error': 'Senha não está em atendimento'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        senha.status = 'concluido'
        senha.concluido_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
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
    
    @action(detail=False, methods=['get'])
    def proxima(self, request):
        """Retorna a próxima senha a ser chamada (prioritárias primeiro)"""
        # Primeiro verifica se há prioritárias/urgências aguardando
        senha_prioritaria = self.queryset.filter(
            status='aguardando',
            tipo__in=['P', 'U']
        ).order_by('criado_em').first()
        
        if senha_prioritaria:
            serializer = self.get_serializer(senha_prioritaria)
            return Response(serializer.data)
        
        # Se não há prioritária, pega a próxima normal
        senha_normal = self.queryset.filter(
            status='aguardando',
            tipo='N'
        ).order_by('criado_em').first()
        
        if senha_normal:
            serializer = self.get_serializer(senha_normal)
            return Response(serializer.data)
        
        return Response(
            {'message': 'Nenhuma senha aguardando'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(detail=False, methods=['get'])
    def painel(self, request):
        """Retorna dados para o painel de senhas"""
        hoje = date.today()
        
        # Senha sendo chamada
        senha_chamando = self.queryset.filter(status='chamando').order_by('-chamado_em').first()
        
        # Últimas 5 senhas chamadas
        ultimas_chamadas = self.queryset.filter(
            status__in=['atendendo', 'concluido'],
            chamado_em__isnull=False
        ).order_by('-chamado_em')[:5]
        
        # Senhas aguardando
        senhas_aguardando = self.queryset.filter(status='aguardando').order_by('criado_em')[:10]
        
        # Estatísticas
        total_hoje = self.queryset.filter(criado_em__date=hoje).count()
        total_atendidas = self.queryset.filter(status='concluido', concluido_em__date=hoje).count()
        total_aguardando = self.queryset.filter(status='aguardando').count()
        total_em_atendimento = self.queryset.filter(status='atendendo').count()
        
        return Response({
            'senha_chamando': SenhaSerializer(senha_chamando).data if senha_chamando else None,
            'ultimas_chamadas': SenhaSerializer(ultimas_chamadas, many=True).data,
            'senhas_aguardando': SenhaSerializer(senhas_aguardando, many=True).data,
            'estatisticas': {
                'total_hoje': total_hoje,
                'total_atendidas': total_atendidas,
                'total_aguardando': total_aguardando,
                'total_em_atendimento': total_em_atendimento,
            }
        })
