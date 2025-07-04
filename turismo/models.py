from django.db import models
from django.db.models import Avg
from django.conf import settings

class PontoTuristico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    localizacao = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='pontos/', null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome

    @property
    def media_avaliacoes(self):
        avg = self.avaliacoes.aggregate(Avg('nota'))['nota__avg']
        return round(avg, 1) if avg is not None else "Ainda sem avaliações"

class Avaliacao(models.Model):
    visitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'perfilusuario__tipo': 'visitante'}
    )
    lugar = models.ForeignKey(PontoTuristico, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField(blank=True, null=True)  # Made optional
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.visitante.username} em {self.lugar.nome}"

class Recomendacao(models.Model):
    lugar = models.ForeignKey(PontoTuristico, on_delete=models.CASCADE)
    motivo = models.TextField()
    data_recomendacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recomendação de {self.lugar.nome}"