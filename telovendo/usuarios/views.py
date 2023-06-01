import random
import string

from django.shortcuts import render
from django.shortcuts import redirect, render

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from .forms import FormularioRegistroCliente, FormularioRegistroTrabajador
from .models import Usuario, Cliente, Trabajador
from sitioweb.models import Producto

from django.core.mail import send_mail


def generar_contrasena():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))


def autenticar_usuario(request, usuario, contrasena):
    usuario = authenticate(request, username=usuario, password=contrasena)
    if usuario:
        login(request, usuario)
    if not usuario.email_verificado:
        usuario.email_verificado = True
        usuario.save()
    return True if usuario is not None else False


def index(request):
    if request.method == 'POST':
        messages.success(request, "¡Has iniciado sesión!") if autenticar_usuario(
            request, request.POST['email'], request.POST['contrasena']) else messages.error(request, "¡Error al iniciar sesión!")
        return redirect('index')

    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        return redirect("sitioweb:pedidos")

    context = {"productos": Producto.objects.all()}
    return render(request, 'index.html', context)


def cerrar_sesion(request):
    logout(request)
    messages.success(request, "¡Has cerrado sesión!")
    return redirect('index')


def registrar_cliente(request):
    if request.method == 'POST':
        form = FormularioRegistroCliente(
            request.POST) if not request.user.is_superuser else FormularioRegistroTrabajador(request.POST)
        if form.is_valid():

            datos = form.cleaned_data
            email = datos.pop("email")
            contrasena = generar_contrasena()
            tipo_trabajador = datos.get("tipo_trabajador", False)
            datos_user = {"email": email,
                          "password": make_password(contrasena)}

            if tipo_trabajador:
                datos_user['is_superuser'] = True if tipo_trabajador == 1 else False
                datos_user['is_staff'] = True if tipo_trabajador == 2 else False

            usuario = Usuario.objects.create(**datos_user)

            Cliente.objects.create(
                **{"usuario": usuario, **datos}) if not tipo_trabajador else Trabajador.objects.create(**{"usuario": usuario, **datos})
            send_mail("Registro en TeLoVendo",
                      f"Estimado {datos['nombre']}:\n\n\n Contraseña para verificar e iniciar sesión es: {contrasena}", "telovendopython@gmail.com", [email])
            return redirect('index')
        return render(request, 'registro_usuario.html', {'form': form})
    else:
        form = FormularioRegistroCliente(
        ) if not request.user.is_superuser else FormularioRegistroTrabajador()
        return render(request, 'registro_usuario.html', {'form': form})
