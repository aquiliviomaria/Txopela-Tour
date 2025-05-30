from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario
from django.contrib.auth.forms import UserCreationForm

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    tipo = forms.ChoiceField(choices=(('visitante', 'Visitante'), ('admin', 'Administrador')))
    localizacao = forms.CharField(required=False)
    data_nascimento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    bio = forms.CharField(widget=forms.Textarea, required=False)
    foto_perfil = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            perfil = PerfilUsuario.objects.create(
                user=user,
                tipo=self.cleaned_data['tipo'],
                localizacao=self.cleaned_data['localizacao'],
                data_nascimento=self.cleaned_data['data_nascimento'],
                bio=self.cleaned_data['bio'],
                foto_perfil=self.cleaned_data['foto_perfil']
            )
        return user
