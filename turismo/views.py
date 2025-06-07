from django.shortcuts import render, get_object_or_404, redirect
from .models import PontoTuristico, Avaliacao, Recomendacao
from usuarios.models import PerfilUsuario
from django.contrib.auth.decorators import login_required
from .forms import PreferenciaForm
from django.db.models import Count
from django.contrib import messages
from .forms import AvaliacaoForm


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
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            Avaliacao.objects.create(
                lugar=lugar,
                visitante=request.user,
                nota=form.cleaned_data['nota'],
                comentario=form.cleaned_data['comentario']
            )
            messages.success(request, 'Avaliação enviada com sucesso!')
            return redirect('turismo:detalhe_ponto', lugar_id=lugar.id)
        else:
            messages.error(request, 'Erro ao enviar a avaliação. Verifique os dados.')
    else:
        form = AvaliacaoForm()
    return render(request, 'turismo/avaliar.html', {'lugar': lugar, 'form': form})


@login_required
def recomendacoes(request):
    locais = PontoTuristico.objects.all()
    form = PreferenciaForm(request.GET or None)

    filtros_ativos = False  # flag para sabermos se o usuário filtrou manualmente

    if request.GET and form.is_valid():
        localizacao = form.cleaned_data.get('localizacao')
        categoria = form.cleaned_data.get('categoria')

        if localizacao:
            locais = locais.filter(localizacao__icontains=localizacao)
            filtros_ativos = True
        if categoria:
            locais = locais.filter(categoria__icontains=categoria)
            filtros_ativos = True

    usuario = request.user  # User (não perfil)

    # Geração de recomendações com base nas avaliações anteriores
    boas_avaliacoes = Avaliacao.objects.filter(visitante=usuario, nota__gte=4)
    categorias_favoritas = boas_avaliacoes.values_list('lugar__categoria', flat=True)
    localizacoes_favoritas = boas_avaliacoes.values_list('lugar__localizacao', flat=True)
    locais_avaliados_ids = boas_avaliacoes.values_list('lugar_id', flat=True)

    recomendados = PontoTuristico.objects.filter(
        categoria__in=categorias_favoritas
    ).exclude(id__in=locais_avaliados_ids)

    recomendados |= PontoTuristico.objects.filter(
        localizacao__in=localizacoes_favoritas
    ).exclude(id__in=locais_avaliados_ids)

    recomendados = recomendados.distinct()

    # Se não houver filtros, mostrar recomendações
    if not filtros_ativos:
        locais = recomendados

    return render(request, 'turismo/recomendacoes.html', {
        'locais': locais,
        'form': form,
    })
