from django import forms
from .models import Producto, Pedido
from usuarios.forms import FormularioRegistroCliente, FormularioDireccion
from gestion.models import MedioPedido, EstadoPedido, FormaPago


class FormularioProducto(forms.ModelForm):
    sku = forms.CharField(label="SKU", disabled=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    nombre = forms.CharField(label="Nombre", disabled=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    descripcion = forms.CharField(label="Descipción", max_length=500, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Descripción'}))
    stock = forms.IntegerField(label="Stock disponible", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Stock disponible'}))
    precio = forms.IntegerField(label="Precio", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Precio'}))

    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'descripcion', 'stock', 'precio']


class FormularioPedido(FormularioRegistroCliente, FormularioDireccion):
    medio = forms.ChoiceField(label="Pedido realizado en", choices=[
                              (x.id, x.nombre) for x in MedioPedido.objects.all()])
    estado = forms.ChoiceField(label="Estado del Pedido", choices=[
                              (x.id, x.nombre) for x in EstadoPedido.objects.all()])
    forma_pago = forms.ChoiceField(label="Forma de pago", choices=[
        (x.id, x.nombre) for x in FormaPago.objects.filter(habilitado=True)])

    class Meta(FormularioRegistroCliente.Meta, FormularioDireccion.Meta):
        model = Pedido


class FormularioPedidoUsuario(FormularioPedido):
    class Meta:
        model = Pedido
        exclude = ['medio', 'estado']


class FormularioActualizarEstado(forms.ModelForm):
    estado = forms.ChoiceField(label="Estado del Pedido", choices=[
                               (x.id, x.nombre) for x in EstadoPedido.objects.all()])

    class Meta:
        model = Pedido
        fields = ['estado']

    def clean_estado(self):
        return EstadoPedido.objects.get(id=self.cleaned_data['estado'])
