from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm
from django.contrib import messages

User = get_user_model()

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro concluído com sucesso. Faça login.')
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirecionar com base no tipo de perfil
            perfil = getattr(user, 'perfilusuario', None)
            if perfil:
                if perfil.tipo == 'admin':
                    return redirect('painel_admin')  # admin → painel de gestão
                else:
                    return redirect('turismo:recomendacoes')  # visitante → recomendações
            else:
                return redirect('turismo:home')  # fallback

    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso.')
            return redirect('usuarios:perfil')
    else:
        form = RegistroUsuarioForm(instance=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})


@login_required
def apagar_perfil(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Conta apagada com sucesso.')
        return redirect('usuarios:registro')
    return render(request, 'usuarios/confirmar_apagar.html')


def logout_usuario(request):
    logout(request)
    return redirect('usuarios:login')


@login_required
def perfil_usuario(request):
    return render(request, 'usuarios/perfil.html')
