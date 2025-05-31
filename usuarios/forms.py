from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # REMOVEMOS o campo "tipo" exposto, pois sempre será "visitante" neste form público:
    # tipo = forms.ChoiceField(choices=(('visitante', 'Visitante'), ('admin', 'Administrador')))
    localizacao = forms.CharField(required=False)
    data_nascimento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    bio = forms.CharField(widget=forms.Textarea, required=False)
    foto_perfil = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # Note que "tipo" NÃO faz parte de fields.

    def save(self, commit=True):
        # Primeiro, cria o User normalmente (sem commit para ainda não gravar)
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Força que todo perfil criado via este form seja “visitante”:
            PerfilUsuario.objects.create(
                user=user,
                tipo='visitante',
                localizacao=self.cleaned_data.get('localizacao', ''),
                data_nascimento=self.cleaned_data.get('data_nascimento', None),
                bio=self.cleaned_data.get('bio', ''),
                foto_perfil=self.cleaned_data.get('foto_perfil', None)
            )
        return user
