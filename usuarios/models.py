from django.db import models
from django.contrib.auth.models import User

TIPO_USUARIO = (
    ('admin', 'Administrador'),
    ('visitante', 'Visitante'),
)

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO, default='visitante')
    localizacao = models.CharField(max_length=100, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"
