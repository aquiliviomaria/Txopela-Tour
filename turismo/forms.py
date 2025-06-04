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
