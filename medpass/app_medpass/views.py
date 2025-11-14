from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Especialidade, Profissional, Senha

# Views do sistema MedPass
def home(request):
    return render(request, 'home/home.html')

def central_senhas(request):
    """View para exibir a central de senhas"""
    especialidades = Especialidade.objects.filter(ativa=True).order_by('nome')
    senhas_aguardando = Senha.objects.filter(status='aguardando').select_related('especialidade').order_by('criado_em')
    senhas_chamando = Senha.objects.filter(status='chamando').select_related('especialidade', 'profissional').order_by('-chamado_em')
    senhas_atendendo = Senha.objects.filter(status='atendendo').select_related('especialidade', 'profissional').order_by('-atendido_em')
    
    context = {
        'especialidades': especialidades,
        'senhas_aguardando': senhas_aguardando,
        'senhas_chamando': senhas_chamando,
        'senhas_atendendo': senhas_atendendo,
    }
    return render(request, 'central_senhas/central_senhas.html', context)

def painel_senhas(request):
    """View para painel público de visualização de senhas com áudio"""
    hoje = timezone.now().date()
    
    # Senha atualmente sendo chamada (mais recente com status chamando)
    senha_chamando = Senha.objects.filter(status='chamando').select_related('especialidade', 'profissional').order_by('-chamado_em').first()
    
    # Últimas 5 senhas chamadas (chamando ou atendendo)
    ultimas_chamadas = Senha.objects.filter(
        status__in=['chamando', 'atendendo']
    ).select_related('especialidade', 'profissional').order_by('-chamado_em')[:5]
    
    # Senhas aguardando
    senhas_aguardando = Senha.objects.filter(
        status='aguardando'
    ).select_related('especialidade').order_by('criado_em')[:10]
    
    # Estatísticas do dia
    total_hoje = Senha.objects.filter(criado_em__date=hoje).count()
    total_atendidas = Senha.objects.filter(criado_em__date=hoje, status='concluido').count()
    total_aguardando = Senha.objects.filter(status='aguardando').count()
    total_em_atendimento = Senha.objects.filter(status__in=['chamando', 'atendendo']).count()
    
    context = {
        'senha_chamando': senha_chamando,
        'ultimas_chamadas': ultimas_chamadas,
        'senhas_aguardando': senhas_aguardando,
        'total_hoje': total_hoje,
        'total_atendidas': total_atendidas,
        'total_aguardando': total_aguardando,
        'total_em_atendimento': total_em_atendimento,
    }
    return render(request, 'painel_senhas/painel_senhas.html', context)

def gerar_senha(request):
    """View para gerar uma nova senha"""
    if request.method == 'POST':
        especialidade_id = request.POST.get('especialidade')
        tipo = request.POST.get('tipo', 'N')
        
        if not especialidade_id:
            messages.error(request, 'Por favor, selecione uma especialidade.')
            return redirect('central_senhas')
        
        try:
            especialidade = Especialidade.objects.get(id=especialidade_id)
            
            # Gerar número da senha
            hoje = timezone.now().date()
            senhas_hoje = Senha.objects.filter(
                tipo=tipo,
                criado_em__date=hoje
            ).count() + 1
            
            numero = f"{tipo}{senhas_hoje:03d}"
            
            # Criar a senha
            senha = Senha.objects.create(
                numero=numero,
                tipo=tipo,
                especialidade=especialidade,
                status='aguardando'
            )
            
            messages.success(request, f'Senha {numero} gerada com sucesso!')
            return redirect('central_senhas')
            
        except Especialidade.DoesNotExist:
            messages.error(request, 'Especialidade não encontrada.')
        except Exception as e:
            messages.error(request, f'Erro ao gerar senha: {str(e)}')
    
    return redirect('central_senhas')

def chamar_senha(request, senha_id):
    """View para chamar uma senha"""
    if request.method == 'POST':
        try:
            senha = get_object_or_404(Senha, id=senha_id)
            profissional_id = request.POST.get('profissional')
            guiche = request.POST.get('guiche', '')
            
            if senha.status != 'aguardando':
                return JsonResponse({'error': 'Esta senha não está disponível para chamada.'}, status=400)
            
            senha.status = 'chamando'
            senha.chamado_em = timezone.now()
            senha.guiche = guiche
            
            if profissional_id:
                profissional = get_object_or_404(Profissional, id=profissional_id)
                senha.profissional = profissional
            
            senha.save()
            
            messages.success(request, f'Senha {senha.numero} chamada com sucesso!')
            return JsonResponse({'success': True, 'numero': senha.numero})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def atualizar_status_senha(request, senha_id):
    """View para atualizar o status de uma senha"""
    if request.method == 'POST':
        try:
            senha = get_object_or_404(Senha, id=senha_id)
            novo_status = request.POST.get('status')
            
            if novo_status not in ['aguardando', 'chamando', 'atendendo', 'concluido', 'cancelado']:
                return JsonResponse({'error': 'Status inválido.'}, status=400)
            
            senha.status = novo_status
            
            if novo_status == 'atendendo' and not senha.atendido_em:
                senha.atendido_em = timezone.now()
            elif novo_status == 'concluido' and not senha.concluido_em:
                senha.concluido_em = timezone.now()
            
            senha.save()
            
            messages.success(request, f'Status da senha {senha.numero} atualizado para {senha.get_status_display()}!')
            return JsonResponse({'success': True, 'status': novo_status})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def cadastrar_medicos(request):
    if request.method == 'POST':
        # Processar o formulário de cadastro de médicos
        nome = request.POST.get('nome')
        crm = request.POST.get('crm')
        uf_crm = request.POST.get('uf_crm', 'MT')
        especialidade_id = request.POST.get('especialidade')
        telefone = request.POST.get('telefone', '')
        email = request.POST.get('email', '')
        
        # Validações básicas
        if not nome or not crm or not especialidade_id:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
        else:
            try:
                especialidade = Especialidade.objects.get(id=especialidade_id)
                Profissional.objects.create(
                    nome=nome,
                    crm=crm,
                    uf_crm=uf_crm,
                    especialidade=especialidade,
                    telefone=telefone,
                    email=email
                )
                messages.success(request, f'Profissional {nome} cadastrado com sucesso!')
                return redirect('cadastrar_medicos')
            except Especialidade.DoesNotExist:
                messages.error(request, 'Especialidade selecionada não existe.')
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar profissional: {str(e)}')
    
    # Buscar todas as especialidades ativas e profissionais para exibir
    especialidades = Especialidade.objects.filter(ativa=True).order_by('nome')
    profissionais = Profissional.objects.filter(ativo=True).select_related('especialidade').order_by('-criado_em')
    
    context = {
        'especialidades': especialidades,
        'profissionais': profissionais
    }
    return render(request, 'cadastrarmedicos/cadastrar_medicos.html', context)

def cadastrar_especialidade(request):
    if request.method == 'POST':
        # Processar o formulário de cadastro de especialidades
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        
        # Validações básicas
        if not nome:
            messages.error(request, 'Por favor, informe o nome da especialidade.')
        else:
            try:
                Especialidade.objects.create(
                    nome=nome,
                    descricao=descricao
                )
                messages.success(request, f'Especialidade {nome} cadastrada com sucesso!')
                return redirect('cadastrar_especialidade')
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar especialidade: {str(e)}')
    
    # Buscar todas as especialidades para exibir
    especialidades = Especialidade.objects.filter(ativa=True).order_by('-criado_em')
    
    context = {
        'especialidades': especialidades
    }
    return render(request, 'cadastrarespecialidade/cadastrar_especialidade.html', context)
