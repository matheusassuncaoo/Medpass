from django.contrib import admin
from django.urls import path, include
from app_medpass import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include('app_medpass.api_urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Páginas
    path('', views.home, name='home'),
    path('painel/', views.painel_senhas, name='painel_senhas'),
    
    # Central de Senhas
    path('central-senhas/', views.central_senhas, name='central_senhas'),
    path('gerar-senha/', views.gerar_senha, name='gerar_senha'),
    
    # Guichê
    path('guiche/', views.painel_guiche, name='painel_guiche'),
    path('selecionar-guiche/', views.selecionar_guiche, name='selecionar_guiche'),
    path('guiche/chamar/<int:senha_id>/', views.guiche_chamar_senha, name='guiche_chamar_senha'),
    path('guiche/rechamar/<int:senha_id>/', views.guiche_rechamar_senha, name='guiche_rechamar_senha'),
    path('guiche/iniciar-triagem/<int:senha_id>/', views.guiche_iniciar_triagem, name='guiche_iniciar_triagem'),
    path('guiche/finalizar-triagem/<int:senha_id>/', views.guiche_finalizar_triagem, name='guiche_finalizar_triagem'),
    path('guiche/cancelar/<int:senha_id>/', views.guiche_cancelar_senha, name='guiche_cancelar_senha'),
    
    # Médico
    path('medico/', views.painel_medico, name='painel_medico'),
    path('selecionar-medico/', views.selecionar_medico, name='selecionar_medico'),
    path('medico/chamar/<int:senha_id>/', views.medico_chamar_senha, name='medico_chamar_senha'),
    path('medico/iniciar-consulta/<int:senha_id>/', views.medico_iniciar_consulta, name='medico_iniciar_consulta'),
    path('medico/finalizar-consulta/<int:senha_id>/', views.medico_finalizar_consulta, name='medico_finalizar_consulta'),
    path('medico/rechamar/<int:senha_id>/', views.medico_rechamar_senha, name='medico_rechamar_senha'),
    path('medico/desistencia/<int:senha_id>/', views.medico_desistencia_senha, name='medico_desistencia_senha'),
    
    # Cadastros
    path('cadastrar-medicos/', views.cadastrar_medicos, name='cadastrar_medicos'),
    path('cadastrar-guiche/', views.cadastrar_guiche, name='cadastrar_guiche'),
    path('cadastrar-especialidade/', views.cadastrar_especialidade, name='cadastrar_especialidade'),
    
    # Deletar
    path('deletar-especialidade/<int:id>/', views.deletar_especialidade, name='deletar_especialidade'),
    path('deletar-medico/<int:id>/', views.deletar_medico, name='deletar_medico'),
    path('deletar-guiche/<int:id>/', views.deletar_guiche, name='deletar_guiche'),
    
    # APIs internas
    path('api/senhas-aguardando/', views.api_senhas_aguardando, name='api_senhas_aguardando'),
    path('api/senha-chamando/', views.api_senha_chamando, name='api_senha_chamando'),
]
