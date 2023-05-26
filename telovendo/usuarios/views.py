import random, string

from django.shortcuts import render
from django.shortcuts import redirect, render

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from .forms import FormularioRegistroCliente
from .models import Usuario, Cliente

from django.core.mail import send_mail

def generar_contrasena():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))

def autenticar_usuario(request, usuario, contrasena):
    usuario = authenticate(request, username=usuario, password=contrasena)
    if usuario: login(request, usuario)
    if not usuario.email_verificado: 
        usuario.email_verificado = True
        usuario.save()
    return True if usuario is not None else False

def index(request):
    if request.method == 'POST':
        messages.success(request, "¡Has iniciado sesión!") if autenticar_usuario(request, request.POST['email'], request.POST['contrasena']) else messages.error(request, "¡Error al iniciar sesión!")
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
            datos = form.cleaned_data
            email = datos.pop("email")
            contrasena = generar_contrasena()
            usuario = Usuario.objects.create(email=email, password=make_password(contrasena))
            Cliente.objects.create(**{"usuario": usuario, **datos})
            send_mail("Registro en TeLoVendo", f"Estimado {datos['nombre']}:\n\n\n Contraseña para verificar e iniciar sesión es: {contrasena}", "telovendopython@gmail.com", [email])  
            return redirect('index')
        return render(request, 'registro_usuario.html', {'form': form})
    else:
        form = FormularioRegistroCliente()
        return render(request, 'registro_usuario.html', {'form':form})
