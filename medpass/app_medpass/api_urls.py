from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import EspecialidadeViewSet, ProfissionalViewSet, SenhaViewSet, GuicheViewSet

router = DefaultRouter()
router.register(r'especialidades', EspecialidadeViewSet, basename='especialidade')
router.register(r'profissionais', ProfissionalViewSet, basename='profissional')
router.register(r'guiches', GuicheViewSet, basename='guiche')
router.register(r'senhas', SenhaViewSet, basename='senha')

urlpatterns = [
    path('', include(router.urls)),
]
