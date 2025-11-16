from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import date, timedelta
from .models import Especialidade, Profissional, Senha
from .serializers import (
    EspecialidadeSerializer, 
    ProfissionalSerializer, 
    SenhaSerializer,
    SenhaCreateSerializer,
    SenhaChamarSerializer,
    SenhaStatusSerializer
)


class EspecialidadeViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Especialidades.
    
    list: Lista todas as especialidades
    create: Cria uma nova especialidade
    retrieve: Retorna uma especialidade específica
    update: Atualiza uma especialidade
    partial_update: Atualiza parcialmente uma especialidade
    destroy: Remove uma especialidade
    """
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    
    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """Retorna apenas especialidades ativas"""
        especialidades = self.queryset.filter(ativo=True)
        serializer = self.get_serializer(especialidades, many=True)
        return Response(serializer.data)


class ProfissionalViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Profissionais.
    
    list: Lista todos os profissionais
    create: Cria um novo profissional
    retrieve: Retorna um profissional específico
    update: Atualiza um profissional
    partial_update: Atualiza parcialmente um profissional
    destroy: Remove um profissional
    """
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Retorna apenas profissionais ativos"""
        profissionais = self.queryset.filter(ativo=True)
        serializer = self.get_serializer(profissionais, many=True)
        return Response(serializer.data)
    
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


class SenhaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Senhas.
    
    list: Lista todas as senhas
    create: Gera uma nova senha
    retrieve: Retorna uma senha específica
    update: Atualiza uma senha
    partial_update: Atualiza parcialmente uma senha
    destroy: Remove uma senha
    """
    queryset = Senha.objects.all().select_related('especialidade')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SenhaCreateSerializer
        return SenhaSerializer
    
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
        senhas = self.queryset.filter(status='atendimento').order_by('-atendido_em')
        serializer = self.get_serializer(senhas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def finalizadas(self, request):
        """Retorna senhas finalizadas"""
        senhas = self.queryset.filter(status='finalizado').order_by('-finalizado_em')
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
        em_atendimento = self.queryset.filter(status='atendimento').count()
        finalizadas_hoje = self.queryset.filter(
            status='finalizado',
            finalizado_em__date=hoje
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
        
        senha.status = 'atendimento'
        senha.atendido_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        """Finaliza o atendimento de uma senha"""
        senha = self.get_object()
        
        if senha.status not in ['chamando', 'atendimento']:
            return Response(
                {'error': 'Senha não está em atendimento'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        senha.status = 'finalizado'
        senha.finalizado_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancela uma senha"""
        senha = self.get_object()
        
        if senha.status == 'finalizado':
            return Response(
                {'error': 'Senha já foi finalizada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        senha.status = 'finalizado'
        senha.finalizado_em = timezone.now()
        senha.save()
        
        return Response(SenhaSerializer(senha).data)
    
    @action(detail=False, methods=['get'])
    def proxima(self, request):
        """Retorna a próxima senha a ser chamada (prioritárias primeiro)"""
        # Primeiro verifica se há prioritárias aguardando
        senha_prioritaria = self.queryset.filter(
            status='aguardando',
            tipo='prioritario'
        ).order_by('criado_em').first()
        
        if senha_prioritaria:
            serializer = self.get_serializer(senha_prioritaria)
            return Response(serializer.data)
        
        # Se não há prioritária, pega a próxima normal
        senha_normal = self.queryset.filter(
            status='aguardando',
            tipo='normal'
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
            status__in=['atendimento', 'finalizado'],
            chamado_em__isnull=False
        ).order_by('-chamado_em')[:5]
        
        # Senhas aguardando
        senhas_aguardando = self.queryset.filter(status='aguardando').order_by('criado_em')[:10]
        
        # Estatísticas
        total_hoje = self.queryset.filter(criado_em__date=hoje).count()
        total_atendidas = self.queryset.filter(status='finalizado', finalizado_em__date=hoje).count()
        total_aguardando = self.queryset.filter(status='aguardando').count()
        total_em_atendimento = self.queryset.filter(status='atendimento').count()
        
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
