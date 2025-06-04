from django.urls import path
from . import views

app_name = 'turismo'

urlpatterns = [
    path('', views.home, name='home'),
    path('lugar/<int:lugar_id>/', views.detalhe_ponto, name='detalhe_ponto'),
    path('lugar/<int:lugar_id>/avaliar/', views.avaliar, name='avaliar'),
    path('recomendacoes/', views.recomendacoes, name='recomendacoes'),
    
]
