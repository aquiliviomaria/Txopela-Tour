from django.contrib import admin
from .models import PontoTuristico, Avaliacao, Recomendacao

@admin.register(PontoTuristico)
class PontoTuristicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'localizacao', 'data_cadastro']
    search_fields = ['nome', 'localizacao']

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['visitante', 'lugar', 'nota', 'data_avaliacao']
    search_fields = ['visitante__username', 'lugar__nome']

@admin.register(Recomendacao)
class RecomendacaoAdmin(admin.ModelAdmin):
    list_display = ['lugar', 'data_recomendacao']
