from django.shortcuts import render
from django.shortcuts import redirect, render

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import FormularioRegistroCliente
from .models import Usuario


def autenticar_usuario(request, usuario, contrasena):
    user = authenticate(request, username=usuario, password=contrasena)
    if user: login(request, user)
    return True if user is not None else False

def index(request):
    if request.method == 'POST':
        messages.success(request, "¡Has iniciado sesión!") if autenticar_usuario(request, request.POST['usuario'], request.POST['contrasena']) else messages.error(request, "¡Error al iniciar sesión!")
        return redirect('index')
    return render(request, 'index.html')

def cerrar_sesion(request):
    logout(request)
    messages.success(request, "¡Has cerrado sesión!")
    return redirect('index')

def registrar_cliente(request):
    if request.method == 'POST':
        form = FormularioRegistroCliente(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('index')
        
    form = FormularioRegistroCliente()
    return render(request, 'registro_usuario.html', {'form':form})
