from django.shortcuts import render

# Views do sistema MedPass
def home(request):
    return render(request, 'home/home.html')

def central_senhas(request):
    return render(request, 'central_senhas/central_senhas.html')

def cadastrar_medicos(request):
    return render(request, 'cadastrarmedicos/cadastrar_medicos.html')

def cadastrar_especialidade(request):
    return render(request, 'cadastrarespecialidade/cadastrar_especialidade.html')
