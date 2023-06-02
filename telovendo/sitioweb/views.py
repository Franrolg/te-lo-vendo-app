from django.db import transaction
import random
import string

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password

from .models import Producto, Pedido, DetallePedido
from usuarios.models import Cliente, Usuario, Direccion
from usuarios.forms import FormularioDireccionPedido
from gestion.models import Comuna, MedioPedido, EstadoPedido, FormaPago
from .forms import FormularioProducto, FormularioPedido, FormularioActualizarEstado, FormularioPedidoUsuario

from django.core.mail import send_mail


def generar_contrasena():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))


class ProductosView(ListView):
    model = Producto
    template_name = "productos.html"
    context_object_name = "productos"

    def post(self, request, *args, **kwargs):
        producto = Producto.objects.get(sku=request.POST['sku'])
        producto.stock = request.POST['stock']
        producto.precio = request.POST['precio']
        producto.save()
        return redirect('sitioweb:productos')


class ProductoView(DetailView):
    model = Producto
    slug_field = 'sku'
    slug_url_kwarg = 'sku'
    context_object_name = "producto"
    template_name = "detalle_producto.html"


class ActualizarProductoView(UpdateView):
    model = Producto
    template_name = "actualizar_producto.html"
    form_class = FormularioProducto
    context_object_name = "producto"
    slug_field = 'sku'
    slug_url_kwarg = 'sku'
    success_url = reverse_lazy('sitioweb:productos')


class PedidosView(ListView):
    model = Pedido
    template_name = "pedidos.html"
    context_object_name = "pedidos"

    def post(self, request, *args, **kwargs):
        if request.POST.get('id_cancelar', False):
            pedido = Pedido.objects.get(id=request.POST['id_cancelar'])
            pedido.estado = EstadoPedido.objects.get(id=5)
            detalles_productos = pedido.detallepedido_set.all()
            for detalle in detalles_productos:
                producto = detalle.producto
                producto.stock += detalle.cantidad
                producto.save()

            pedido.save()

        if request.POST.get("id_estado", False):
            pedido = Pedido.objects.get(id=request.POST['id_estado'])
            pedido.estado = EstadoPedido.objects.get(id=pedido.estado_id+1)
            pedido.save()
        
        send_mail(f"Cambio estado pedido #{pedido.id}",
                      f"Estimado {pedido.cliente.nombre}:\n\n\n El estado de su pedido {pedido.id} ha camiado a '{pedido.estado}'.", "telovendopython@gmail.com", [pedido.cliente.usuario.email])

        return redirect('sitioweb:pedidos')


class MisPedidosView(ListView):
    model = Pedido
    template_name = "mis_pedidos.html"
    context_object_name = "pedidos"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            cliente=self.request.user.cliente_set.first())
        return queryset

    def post(self, request, *args, **kwargs):
        pedido = Pedido.objects.get(id=request.POST['id'])
        detalles_productos = pedido.detallepedido_set.all()
        for detalle in detalles_productos:
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()
        pedido.estado = EstadoPedido.objects.get(id=5)
        pedido.save()

        send_mail(f"Cambio estado pedido #{pedido.id}",
                      f"Estimado {pedido.cliente.nombre}:\n\n\n El estado de su pedido {pedido.id} ha camiado a '{pedido.estado}'.", "telovendopython@gmail.com", [pedido.cliente.usuario.email])
        return redirect('sitioweb:mis pedidos')


class ActualizarPedidoView(UpdateView):
    model = Pedido
    template_name = "detalle_pedido.html"
    form_class = FormularioActualizarEstado
    context_object_name = "pedido"
    success_url = reverse_lazy('sitioweb:pedidos')


@transaction.atomic
def registrar_pedido(request):
    if request.method == 'POST':
        form = FormularioPedido(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            email = datos.pop("email")
            contrasena = generar_contrasena()

            usuario = Usuario.objects.create(
                **{"email": email, "password": make_password(contrasena)})

            direccion = Direccion.objects.create(**{"calle": datos.pop("calle"), "numero": datos.pop("numero"), "departamento": datos.pop(
                "departamento", None), "codigo_postal": datos.pop("codigo_postal"), "comuna": Comuna.objects.get(id=datos.pop("comuna").id), "nombre": datos.pop("nombre_direccion"), "descripcion": datos.pop("descripcion")})

            cliente = Cliente.objects.create(**{"usuario": usuario, "rut": datos.pop('rut'), "nombre":  datos.pop('nombre'), "primer_apellido": datos.pop('primer_apellido'),
                                             "segundo_apellido": datos.pop('segundo_apellido'), "telefono": datos.pop('telefono'), "direccion": direccion})

            pedido = Pedido.objects.create(
                **{"cliente": cliente, "medio": MedioPedido.objects.get(id=datos.pop("medio")), "estado": EstadoPedido.objects.get(id=datos.pop("estado")), "forma_pago": FormaPago.objects.get(id=datos.pop("forma_pago")), "direccion": direccion, "creado_por": request.user})

            for key in request.POST:
                if Producto.objects.filter(sku=key).exists() and request.POST[key] and int(request.POST[key]) > 0:
                    producto = Producto.objects.get(sku=key)
                    producto.stock -= int(request.POST[key])
                    producto.save()
                    DetallePedido.objects.create(
                        **{"producto_id": producto.sku, "pedido_id": pedido.id, "cantidad": int(request.POST[key]), "precio": producto.precio})

            send_mail("Registro de pedido en TeLoVendo",
                      f"Estimado {cliente.nombre}:\n\n\n Se ha registrado un pedido exitósamente. \n\n\n Contraseña para verificar e iniciar sesión es: {contrasena}", "telovendopython@gmail.com", [email])
            return redirect('index')
        return render(request, 'registrar_pedido.html', {'form': form, "productos": Producto.objects.all()})
    else:
        form = FormularioPedido()
        return render(request, 'registrar_pedido.html', {'form': form, "productos": Producto.objects.all()})


@transaction.atomic
def registrar_pedido_usuario(request):

    if request.method == 'GET' and len(request.GET) > 1:
        productos = Producto.objects.filter(
            sku__in=[key for key in request.GET if Producto.objects.filter(sku=key)])
        form = FormularioDireccionPedido()
        contexto = []
        for dato in request.GET:
            contexto.append({'id': dato, 'cantidad': request.GET[dato]})
        return render(request, 'registrar_pedido_usuario.html', {'form': form, "productos": productos, "context": contexto})

    if request.method == 'POST':
        form = FormularioDireccionPedido(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            direccion = Direccion.objects.create(**{"calle": datos.pop("calle"), "numero": datos.pop("numero"), "departamento": datos.pop(
                "departamento", None), "codigo_postal": datos.pop("codigo_postal"), "comuna": Comuna.objects.get(id=datos.pop("comuna").id), "nombre": datos.pop("nombre_direccion"), "descripcion": datos.pop("descripcion")})
            pedido = Pedido.objects.create(
                **{"cliente": request.user.cliente_set.first(), "medio": MedioPedido.objects.get(id=1), "estado": EstadoPedido.objects.get(id=1), "forma_pago": FormaPago.objects.get(id=datos.pop("forma_pago")), "direccion": direccion, "creado_por": request.user})

            for key in request.POST:
                if Producto.objects.filter(sku=key).exists() and request.POST[key] and int(request.POST[key]) > 0:
                    producto = Producto.objects.get(sku=key)
                    producto.stock -= int(request.POST[key])
                    producto.save()
                    DetallePedido.objects.create(
                        **{"producto_id": producto.sku, "pedido_id": pedido.id, "cantidad": int(request.POST[key]), "precio": producto.precio})

            send_mail("Registro de pedido en TeLoVendo",
                      f"Estimado {request.user.cliente_set.first().nombre}:\n\n\n Se ha registrado un pedido exitósamente.", "telovendopython@gmail.com", [request.user.email])

            return redirect('index')
        return render(request, 'registrar_pedido_usuario.html', {'form': form, "productos": productos})

    return redirect('index')


@transaction.atomic
def actualizar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, id=pk)

    if request.method == 'POST':
        formulario = FormularioActualizarEstado(request.POST)
        if formulario.is_valid():
            pedido.estado = formulario.cleaned_data['estado']
            pedido.save()

            send_mail(f"Cambio estado pedido #{pedido.id}",
                      f"Estimado {pedido.cliente.nombre}:\n\n\n Su pedido ahora se encuentra {pedido.estado}.", "telovendopython@gmail.com", [pedido.cliente.usuario.email])

            return redirect('sitioweb:pedidos')
    else:
        formulario = FormularioActualizarEstado(instance=pedido)

    return render(request, 'detalle_pedido.html', {'form': formulario})
