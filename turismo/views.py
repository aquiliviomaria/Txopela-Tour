from django.shortcuts import render, get_object_or_404, redirect
from .models import PontoTuristico, Avaliacao, Recomendacao
from usuarios.models import PerfilUsuario
from django.contrib.auth.decorators import login_required
from .forms import PreferenciaForm


def home(request):
    print(">>> View HOME acessada por:", request.user)
    lugares = PontoTuristico.objects.all()
    return render(request, 'turismo/home.html', {'lugares': lugares})

def detalhe_ponto(request, lugar_id):
    lugar = get_object_or_404(PontoTuristico, id=lugar_id)
    avaliacoes = Avaliacao.objects.filter(lugar=lugar)
    return render(request, 'turismo/detalhe_ponto.html', {
        'lugar': lugar,
        'avaliacoes': avaliacoes,
    })

@login_required
def avaliar(request, lugar_id):
    lugar = get_object_or_404(PontoTuristico, id=lugar_id)
    if request.method == 'POST':
        nota = int(request.POST['nota'])
        comentario = request.POST['comentario']
        Avaliacao.objects.create(
            lugar=lugar,
            visitante=request.user.perfilusuario,
            nota=nota,
            comentario=comentario
        )
        return redirect('turismo:detalhe_ponto', lugar_id=lugar.id)
    return render(request, 'turismo/avaliar.html', {'lugar': lugar})

@login_required
def recomendacoes(request):
    locais = PontoTuristico.objects.all()
    form = PreferenciaForm(request.GET or None)

    if form.is_valid():
        localizacao = form.cleaned_data.get('localizacao')
        categoria = form.cleaned_data.get('categoria')

        if localizacao:
            locais = locais.filter(localizacao__icontains=localizacao)
        if categoria:
            locais = locais.filter(categoria__icontains=categoria)

    return render(request, 'turismo/recomendacoes.html', {
        'locais': locais,
        'form': form
    })
