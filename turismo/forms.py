from django import forms

CATEGORIAS_CHOICES = [
    ('Histórico', 'Histórico'),
    ('Natural', 'Natural'),
    ('Urbano', 'Urbano'),
    ('Religioso', 'Religioso'),
    ('Aventura', 'Aventura'),
]

class PreferenciaForm(forms.Form):
    localizacao = forms.CharField(label="Sua localização", required=False)
    categoria = forms.ChoiceField(label="Categoria preferida", choices=CATEGORIAS_CHOICES, required=False)


class AvaliacaoForm(forms.Form):
    nota = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.Select(choices=[('', 'Escolha uma nota')] + [(i, i) for i in range(1, 6)]),
        required=True,
    )
    comentario = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escreva sua opinião...'}),
        required=False,
    )