
from django.urls import path
from app_medpass import views

urlpatterns = [
    # Rotas que serão usadas no projeto
    # Rotas, view selecionada, nome referencia
    
    # Página inicial - medpass.com
    path('', views.home, name='home'),
    
    # Central de Senhas
    path('central-senhas/', views.central_senhas, name='central_senhas'),
    
    # Cadastro de Médicos
    path('cadastrar-medicos/', views.cadastrar_medicos, name='cadastrar_medicos'),
    
    # Cadastro de Especialidades  
    path('cadastrar-especialidade/', views.cadastrar_especialidade, name='cadastrar_especialidade'),
]
