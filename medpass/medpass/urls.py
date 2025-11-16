
from django.contrib import admin
from django.urls import path, include
from app_medpass import views

urlpatterns = [
    # Admin do Django
    path('admin/', admin.site.urls),
    
    # API RESTful
    path('api/', include('app_medpass.api_urls')),
    path('api-auth/', include('rest_framework.urls')),
    
    # Rotas que serão usadas no projeto
    # Rotas, view selecionada, nome referencia
    
    # Página inicial - medpass.com
    path('', views.home, name='home'),
    
    # Central de Senhas (Gerenciamento)
    path('central-senhas/', views.central_senhas, name='central_senhas'),
    path('gerar-senha/', views.gerar_senha, name='gerar_senha'),
    path('chamar-senha/<int:senha_id>/', views.chamar_senha, name='chamar_senha'),
    path('atualizar-status-senha/<int:senha_id>/', views.atualizar_status_senha, name='atualizar_status_senha'),
    
    # Painel Público de Senhas (Visualização com Áudio)
    path('painel/', views.painel_senhas, name='painel_senhas'),
    
    # Cadastro de Médicos
    path('cadastrar-medicos/', views.cadastrar_medicos, name='cadastrar_medicos'),
    
    # Cadastro de Especialidades  
    path('cadastrar-especialidade/', views.cadastrar_especialidade, name='cadastrar_especialidade'),
]
