from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Especialidade, Profissional

# Views do sistema MedPass
def home(request):
    return render(request, 'home/home.html')

def central_senhas(request):
    return render(request, 'central_senhas/central_senhas.html')

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
