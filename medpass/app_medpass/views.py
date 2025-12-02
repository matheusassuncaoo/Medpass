from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from .models import Especialidade, Profissional, Senha, Guiche


# ============================================
# PÁGINAS PÚBLICAS
# ============================================

def home(request):
    """Página inicial do sistema"""
    return render(request, 'home/home.html')


def painel_senhas(request):
    """Painel público de visualização de senhas"""
    hoje = timezone.now().date()
    
    # Senha atualmente sendo chamada
    senha_chamando_guiche = Senha.objects.filter(
        status='chamando_guiche'
    ).select_related('especialidade', 'guiche').order_by('-chamado_guiche_em').first()
    
    senha_chamando_medico = Senha.objects.filter(
        status='chamando_medico'
    ).select_related('especialidade', 'profissional').order_by('-chamado_medico_em').first()
    
    # Últimas 10 senhas chamadas (guichê ou médico)
    ultimas_chamadas = Senha.objects.filter(
        status__in=['chamando_guiche', 'chamando_medico', 'em_triagem', 'em_consulta', 'concluido']
    ).select_related('especialidade', 'guiche', 'profissional').order_by(
        '-chamado_guiche_em', '-chamado_medico_em', '-concluido_em'
    )[:10]
    
    # Senhas aguardando
    senhas_aguardando_guiche = Senha.objects.filter(
        status='aguardando_guiche'
    ).select_related('especialidade').order_by('criado_em')[:10]
    
    senhas_aguardando_medico = Senha.objects.filter(
        status='aguardando_medico'
    ).select_related('especialidade').order_by('triagem_finalizada_em')[:10]
    
    # Estatísticas
    total_hoje = Senha.objects.filter(criado_em__date=hoje).count()
    total_atendidas = Senha.objects.filter(criado_em__date=hoje, status='concluido').count()
    total_aguardando_guiche = Senha.objects.filter(status='aguardando_guiche').count()
    total_aguardando_medico = Senha.objects.filter(status='aguardando_medico').count()
    
    context = {
        'senha_chamando_guiche': senha_chamando_guiche,
        'senha_chamando_medico': senha_chamando_medico,
        'ultimas_chamadas': ultimas_chamadas,
        'senhas_aguardando_guiche': senhas_aguardando_guiche,
        'senhas_aguardando_medico': senhas_aguardando_medico,
        'total_hoje': total_hoje,
        'total_atendidas': total_atendidas,
        'total_aguardando_guiche': total_aguardando_guiche,
        'total_aguardando_medico': total_aguardando_medico,
    }
    return render(request, 'painel_senhas/painel_senhas.html', context)


# ============================================
# CENTRAL DE SENHAS (Recepção)
# ============================================

def central_senhas(request):
    """View para exibir a central de senhas (recepção)"""
    especialidades = Especialidade.objects.filter(ativa=True).order_by('nome')
    
    hoje = timezone.now().date()
    senhas_hoje = Senha.objects.filter(criado_em__date=hoje).select_related('especialidade').order_by('-criado_em')[:20]
    
    context = {
        'especialidades': especialidades,
        'senhas_hoje': senhas_hoje,
        'total_aguardando_guiche': Senha.objects.filter(status='aguardando_guiche').count(),
        'total_aguardando_medico': Senha.objects.filter(status='aguardando_medico').count(),
    }
    return render(request, 'central_senhas/central_senhas.html', context)


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
            
            # Gera número no formato: TIPO + SIGLA_ESPECIALIDADE + SEQUENCIAL
            # Ex: NC001 (Normal + Cardiologia), PD002 (Preferencial + Dermatologia)
            numero = Senha.gerar_numero(tipo, especialidade)
            
            Senha.objects.create(
                numero=numero,
                tipo=tipo,
                especialidade=especialidade,
                status='aguardando_guiche'
            )
            
            messages.success(request, f'Senha {numero} gerada com sucesso!')
            return redirect('central_senhas')
            
        except Especialidade.DoesNotExist:
            messages.error(request, 'Especialidade não encontrada.')
        except Exception as e:
            messages.error(request, f'Erro ao gerar senha: {str(e)}')
    
    return redirect('central_senhas')


# ============================================
# PAINEL DO GUICHÊ
# ============================================

def selecionar_guiche(request):
    """Página de seleção de guichê"""
    guiches = Guiche.objects.filter(ativo=True).order_by('numero')
    return render(request, 'guiche/selecionar_guiche.html', {'guiches': guiches})


def selecionar_medico(request):
    """Página de seleção de médico"""
    medicos = Profissional.objects.filter(ativo=True).select_related('especialidade').order_by('nome')
    return render(request, 'medico/selecionar_medico.html', {'medicos': medicos})


def painel_guiche(request):
    """Painel do guichê"""
    guiche_id = request.GET.get('guiche')
    
    if not guiche_id:
        return redirect('selecionar_guiche')
    
    guiche = Guiche.objects.filter(id=guiche_id).first()
    
    if not guiche:
        return redirect('selecionar_guiche')
    
    # Lista de guichês disponíveis
    guiches = Guiche.objects.filter(ativo=True).order_by('numero')
    
    # Senhas aguardando (priorizando urgência e preferencial)
    senhas_aguardando = Senha.objects.filter(
        status='aguardando_guiche'
    ).select_related('especialidade').order_by(
        models.Case(
            models.When(tipo='U', then=0),
            models.When(tipo='P', then=1),
            models.When(tipo='N', then=2),
        ),
        'criado_em'
    )
    
    # Senha que este guichê está atendendo
    senha_atual = Senha.objects.filter(
        guiche=guiche,
        status__in=['chamando_guiche', 'em_triagem']
    ).select_related('especialidade').first()
    
    context = {
        'guiche': guiche,
        'guiches': guiches,
        'senhas_aguardando': senhas_aguardando,
        'senha_atual': senha_atual,
        'total_aguardando': senhas_aguardando.count(),
    }
    return render(request, 'guiche/painel_guiche.html', context)


def guiche_chamar_senha(request, senha_id):
    """Guichê chama uma senha"""
    guiche_id = request.POST.get('guiche_id') or request.GET.get('guiche')
    
    if not guiche_id:
        return JsonResponse({'error': 'Guichê não informado'}, status=400)
    
    guiche = Guiche.objects.filter(id=guiche_id).first()
    if not guiche:
        return JsonResponse({'error': 'Guichê não encontrado'}, status=404)
    
    # Verifica se o guichê já está atendendo alguém
    atendendo = Senha.objects.filter(
        guiche=guiche,
        status__in=['chamando_guiche', 'em_triagem']
    ).exists()
    
    if atendendo:
        return JsonResponse({'error': 'Você já está atendendo uma senha.'}, status=400)
    
    try:
        senha = get_object_or_404(Senha, id=senha_id)
        
        if senha.status != 'aguardando_guiche':
            return JsonResponse({'error': 'Esta senha não está disponível.'}, status=400)
        
        senha.status = 'chamando_guiche'
        senha.guiche = guiche
        senha.chamado_guiche_em = timezone.now()
        senha.save()
        
        return JsonResponse({
            'success': True, 
            'numero': senha.numero,
            'message': f'Senha {senha.numero} chamada!'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def guiche_rechamar_senha(request, senha_id):
    """Guichê rechama uma senha (atualiza o timestamp para o painel público falar novamente)"""
    try:
        senha = get_object_or_404(Senha, id=senha_id)
        
        if senha.status != 'chamando_guiche':
            return JsonResponse({'error': 'Esta senha não está sendo chamada.'}, status=400)
        
        # Atualiza o timestamp para o painel público detectar como nova chamada
        senha.chamado_guiche_em = timezone.now()
        senha.save()
        
        return JsonResponse({
            'success': True, 
            'numero': senha.numero,
            'message': f'Senha {senha.numero} rechamada!'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def guiche_iniciar_triagem(request, senha_id):
    """Guichê inicia a triagem"""
    guiche_id = request.POST.get('guiche_id') or request.GET.get('guiche')
    guiche = Guiche.objects.filter(id=guiche_id).first()
    
    try:
        senha = get_object_or_404(Senha, id=senha_id)
        
        if senha.status != 'chamando_guiche':
            return JsonResponse({'error': 'Esta senha não está sendo chamada.'}, status=400)
        
        senha.status = 'em_triagem'
        senha.triagem_iniciada_em = timezone.now()
        senha.save()
        
        return JsonResponse({'success': True, 'message': 'Triagem iniciada!'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def guiche_finalizar_triagem(request, senha_id):
    """Guichê finaliza a triagem"""
    try:
        senha = get_object_or_404(Senha, id=senha_id)
        
        if senha.status != 'em_triagem':
            return JsonResponse({'error': 'Esta senha não está em triagem.'}, status=400)
        
        if request.method == 'POST':
            senha.nome_paciente = request.POST.get('nome_paciente', '')
            senha.observacoes_triagem = request.POST.get('observacoes', '')
        
        senha.status = 'aguardando_medico'
        senha.triagem_finalizada_em = timezone.now()
        senha.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Triagem concluída! Paciente aguardando médico.'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def guiche_cancelar_senha(request, senha_id):
    """Guichê cancela uma senha"""
    try:
        senha = get_object_or_404(Senha, id=senha_id)
        
        if senha.status not in ['aguardando_guiche', 'chamando_guiche', 'em_triagem']:
            return JsonResponse({'error': 'Esta senha não pode ser cancelada.'}, status=400)
        
        motivo = request.POST.get('motivo', 'desistencia')
        senha.status = 'desistencia' if motivo == 'desistencia' else 'cancelado'
        senha.concluido_em = timezone.now()
        senha.save()
        
        return JsonResponse({'success': True, 'message': 'Senha cancelada.'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================
# PAINEL DO MÉDICO
# ============================================

def painel_medico(request):
    """Painel do médico"""
    medico_id = request.GET.get('medico')
    
    if not medico_id:
        return redirect('selecionar_medico')
    
    medico = Profissional.objects.filter(id=medico_id, ativo=True).first()
    
    if not medico:
        return redirect('selecionar_medico')
    
    # Lista de médicos disponíveis
    medicos = Profissional.objects.filter(ativo=True).select_related('especialidade').order_by('nome')
    
    # Senhas aguardando médico da especialidade do médico
    senhas_aguardando = Senha.objects.filter(
        status='aguardando_medico',
        especialidade=medico.especialidade
    ).select_related('especialidade', 'guiche').order_by(
        models.Case(
            models.When(tipo='U', then=0),
            models.When(tipo='P', then=1),
            models.When(tipo='N', then=2),
        ),
        'triagem_finalizada_em'
    )
    
    # Senha que este médico está atendendo
    senha_atual = Senha.objects.filter(
        profissional=medico,
        status__in=['chamando_medico', 'em_consulta']
    ).select_related('especialidade', 'guiche').first()
    
    # Estatísticas
    hoje = timezone.now().date()
    atendidas_hoje = Senha.objects.filter(
        profissional=medico,
        status='concluido',
        concluido_em__date=hoje
    ).count()
    
    context = {
        'medico': medico,
        'medicos': medicos,
        'senhas_aguardando': senhas_aguardando,
        'senha_atual': senha_atual,
        'total_aguardando': senhas_aguardando.count(),
        'atendidas_hoje': atendidas_hoje,
    }
    return render(request, 'medico/painel_medico.html', context)


def medico_chamar_senha(request, senha_id):
    """Médico chama uma senha"""
    medico_id = request.POST.get('medico_id') or request.GET.get('medico')
    
    if not medico_id:
        return JsonResponse({'error': 'Médico não informado'}, status=400)
    
    medico = Profissional.objects.filter(id=medico_id).first()
    if not medico:
        return JsonResponse({'error': 'Médico não encontrado'}, status=404)
    
    # Verifica se o médico já está atendendo alguém
    atendendo = Senha.objects.filter(
        profissional=medico,
        status__in=['chamando_medico', 'em_consulta']
    ).exists()
    
    if atendendo:
        return JsonResponse({'error': 'Você já está atendendo um paciente.'}, status=400)
    
    try:
        senha = get_object_or_404(Senha, id=senha_id)
        
        if senha.status != 'aguardando_medico':
            return JsonResponse({'error': 'Este paciente não está disponível.'}, status=400)
        
        if senha.especialidade != medico.especialidade:
            return JsonResponse({'error': 'Este paciente não é da sua especialidade.'}, status=400)
        
        senha.status = 'chamando_medico'
        senha.profissional = medico
        senha.chamado_medico_em = timezone.now()
        senha.save()
        
        return JsonResponse({
            'success': True, 
            'numero': senha.numero,
            'paciente': senha.nome_paciente or 'Não informado',
            'message': f'Paciente {senha.numero} chamado!'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def medico_iniciar_consulta(request, senha_id):
    """Médico inicia a consulta"""
    try:
        senha = get_object_or_404(Senha, id=senha_id)
        
        if senha.status != 'chamando_medico':
            return JsonResponse({'error': 'Este paciente não está sendo chamado.'}, status=400)
        
        senha.status = 'em_consulta'
        senha.consulta_iniciada_em = timezone.now()
        senha.save()
        
        return JsonResponse({'success': True, 'message': 'Consulta iniciada!'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def medico_finalizar_consulta(request, senha_id):
    """Médico finaliza a consulta"""
    try:
        senha = get_object_or_404(Senha, id=senha_id)
        
        if senha.status != 'em_consulta':
            return JsonResponse({'error': 'Este paciente não está em consulta.'}, status=400)
        
        senha.status = 'concluido'
        senha.concluido_em = timezone.now()
        senha.save()
        
        return JsonResponse({'success': True, 'message': 'Consulta finalizada!'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def medico_rechamar_senha(request, senha_id):
    """Médico rechama o paciente"""
    try:
        senha = get_object_or_404(Senha, id=senha_id)
        
        if senha.status != 'chamando_medico':
            return JsonResponse({'error': 'Só é possível rechamar senhas sendo chamadas.'}, status=400)
        
        senha.chamado_medico_em = timezone.now()
        senha.save()
        
        return JsonResponse({
            'success': True, 
            'numero': senha.numero,
            'message': f'Paciente {senha.numero} rechamado!'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def medico_desistencia_senha(request, senha_id):
    """Médico marca desistência"""
    try:
        senha = get_object_or_404(Senha, id=senha_id)
        
        if senha.status not in ['chamando_medico', 'em_consulta']:
            return JsonResponse({'error': 'Esta senha não pode ser marcada como desistência.'}, status=400)
        
        senha.status = 'desistencia'
        senha.concluido_em = timezone.now()
        senha.save()
        
        return JsonResponse({'success': True, 'message': 'Paciente marcado como desistência.'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================
# CADASTROS
# ============================================

def cadastrar_medicos(request):
    """Cadastro de médicos"""
    if request.method == 'POST':
        nome = request.POST.get('nome')
        crm = request.POST.get('crm')
        uf_crm = request.POST.get('uf_crm', 'MT')
        especialidade_id = request.POST.get('especialidade')
        sala = request.POST.get('sala', '')
        telefone = request.POST.get('telefone', '')
        email = request.POST.get('email', '')
        
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
                    sala=sala,
                    telefone=telefone,
                    email=email
                )
                messages.success(request, f'Dr(a). {nome} cadastrado(a) com sucesso!')
                return redirect('cadastrar_medicos')
            except Especialidade.DoesNotExist:
                messages.error(request, 'Especialidade não encontrada.')
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    especialidades = Especialidade.objects.filter(ativa=True).order_by('nome')
    profissionais = Profissional.objects.filter(ativo=True).select_related('especialidade').order_by('-criado_em')
    
    return render(request, 'cadastrarmedicos/cadastrar_medicos.html', {
        'especialidades': especialidades,
        'profissionais': profissionais
    })


def cadastrar_guiche(request):
    """Cadastro de guichês"""
    if request.method == 'POST':
        numero = request.POST.get('numero')
        nome = request.POST.get('nome')
        
        if not numero or not nome:
            messages.error(request, 'Por favor, preencha todos os campos.')
        else:
            try:
                if Guiche.objects.filter(numero=numero).exists():
                    messages.error(request, 'Este número de guichê já existe.')
                else:
                    Guiche.objects.create(numero=numero, nome=nome)
                    messages.success(request, f'Guichê {numero} cadastrado com sucesso!')
                    return redirect('cadastrar_guiche')
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    guiches = Guiche.objects.filter(ativo=True).order_by('numero')
    
    return render(request, 'cadastrarguiche/cadastrar_guiche.html', {'guiches': guiches})


def cadastrar_especialidade(request):
    """Cadastro de especialidades"""
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sigla = request.POST.get('sigla', '').upper()
        descricao = request.POST.get('descricao', '')
        
        if not nome or not sigla:
            messages.error(request, 'Por favor, informe o nome e a sigla da especialidade.')
        else:
            try:
                Especialidade.objects.create(nome=nome, sigla=sigla, descricao=descricao)
                messages.success(request, f'Especialidade {nome} (sigla: {sigla}) cadastrada!')
                return redirect('cadastrar_especialidade')
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    especialidades = Especialidade.objects.filter(ativa=True).order_by('-criado_em')
    
    return render(request, 'cadastrarespecialidade/cadastrar_especialidade.html', {
        'especialidades': especialidades
    })


def deletar_especialidade(request, id):
    """Deleta uma especialidade"""
    try:
        esp = get_object_or_404(Especialidade, id=id)
        nome = esp.nome
        esp.delete()
        messages.success(request, f'Especialidade {nome} removida!')
    except Exception as e:
        messages.error(request, f'Erro ao remover: {str(e)}')
    return redirect('cadastrar_especialidade')


def deletar_medico(request, id):
    """Deleta um médico"""
    try:
        prof = get_object_or_404(Profissional, id=id)
        nome = prof.nome
        prof.delete()
        messages.success(request, f'Dr(a). {nome} removido(a)!')
    except Exception as e:
        messages.error(request, f'Erro ao remover: {str(e)}')
    return redirect('cadastrar_medicos')


def deletar_guiche(request, id):
    """Deleta um guichê"""
    try:
        g = get_object_or_404(Guiche, id=id)
        numero = g.numero
        g.delete()
        messages.success(request, f'Guichê {numero} removido!')
    except Exception as e:
        messages.error(request, f'Erro ao remover: {str(e)}')
    return redirect('cadastrar_guiche')


# ============================================
# APIs
# ============================================

def api_senhas_aguardando(request):
    """API para obter senhas aguardando"""
    tipo = request.GET.get('tipo', 'guiche')
    especialidade_id = request.GET.get('especialidade')
    
    if tipo == 'guiche':
        senhas = Senha.objects.filter(status='aguardando_guiche')
    else:
        senhas = Senha.objects.filter(status='aguardando_medico')
        if especialidade_id:
            senhas = senhas.filter(especialidade_id=especialidade_id)
    
    senhas = senhas.select_related('especialidade').order_by('criado_em')[:20]
    
    data = [{
        'id': s.id,
        'numero': s.numero,
        'tipo': s.get_tipo_display(),
        'especialidade': s.especialidade.nome,
        'criado_em': s.criado_em.strftime('%H:%M'),
        'nome_paciente': s.nome_paciente or '',
    } for s in senhas]
    
    return JsonResponse({'senhas': data})


def api_senha_chamando(request):
    """API para obter a senha sendo chamada"""
    senha_guiche = Senha.objects.filter(
        status='chamando_guiche'
    ).select_related('guiche').order_by('-chamado_guiche_em').first()
    
    senha_medico = Senha.objects.filter(
        status='chamando_medico'
    ).select_related('profissional').order_by('-chamado_medico_em').first()
    
    data = {'guiche': None, 'medico': None}
    
    if senha_guiche:
        data['guiche'] = {
            'numero': senha_guiche.numero,
            'guiche': senha_guiche.guiche.numero if senha_guiche.guiche else '',
            'chamado_em': senha_guiche.chamado_guiche_em.strftime('%H:%M:%S') if senha_guiche.chamado_guiche_em else ''
        }
    
    if senha_medico:
        data['medico'] = {
            'numero': senha_medico.numero,
            'sala': senha_medico.profissional.sala if senha_medico.profissional else '',
            'medico': senha_medico.profissional.nome if senha_medico.profissional else '',
            'chamado_em': senha_medico.chamado_medico_em.strftime('%H:%M:%S') if senha_medico.chamado_medico_em else ''
        }
    
    return JsonResponse(data)
