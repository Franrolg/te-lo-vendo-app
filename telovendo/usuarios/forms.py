from django import forms
from .models import Usuario, Cliente, Direccion, Trabajador
from rut_chile import rut_chile as rutcl
import phonenumbers
from gestion.models import Comuna, FormaPago


class FormularioUsuario(forms.ModelForm):
    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}))

    class Meta:
        model = Usuario
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con ese email")
        return email


class FormularioDireccion(forms.ModelForm):
    calle = forms.CharField(label="", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'DIRECCION: Calle'}))
    numero = forms.CharField(label="", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'DIRECCION: Numero'}))
    departamento = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'DIRECCION: Departamento'}))
    codigo_postal = forms.CharField(label="", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'DIRECCION: Código Postal'}))
    comuna = forms.ChoiceField(
        choices=[(x.id, x.nombre) for x in Comuna.objects.all().order_by('nombre')])
    nombre_direccion = forms.CharField(label="", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre Dirección: Ej: Casa'}))
    descripcion = forms.CharField(label="", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Descripción Dirección: Ej: Condomio 123, Sector 456'}))

    class Meta:
        model = Direccion
        fields = ['calle', 'numero', 'departamento',
                  'codigo_postal', 'comuna', 'nombre_direccion', 'descripcion']

    def clean_comuna(self):
        return Comuna.objects.get(id=self.cleaned_data['comuna'])


class FormularioDireccionPedido(FormularioDireccion):
    forma_pago = forms.ChoiceField(label="Forma de pago", choices=[
        (x.id, x.nombre) for x in FormaPago.objects.filter(habilitado=True)])

    class Meta(FormularioDireccion.Meta):
        model = Direccion


class FormularioRegistroCliente(FormularioUsuario):
    nombre = forms.CharField(label="", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    primer_apellido = forms.CharField(label="", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Primer Apellido'}))
    segundo_apellido = forms.CharField(label="", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Segundo Apellido'}))
    rut = forms.CharField(label="", max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'RUT'}))
    telefono = forms.CharField(label="", max_length=12, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Teléfono'}))

    class Meta:
        model = Cliente
        fields = ['email', 'nombre', 'primer_apellido',
                  'segundo_apellido', 'rut', 'telefono']

    def clean_rut(self):
        rut = self.cleaned_data['rut'].lower()
        try:
            if not rutcl.is_valid_rut(rut):
                raise forms.ValidationError("El RUT ingresado no es válido")
        except:
            raise forms.ValidationError(
                "Formato de RUT debe ser el siguiente: 12345678-9 (Sin puntos)")

        if Cliente.objects.filter(rut=rut).exists():
            raise forms.ValidationError(
                "Ya existe un usuario con el RUT ingresado")

        return rut

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        try:
            if not phonenumbers.is_possible_number(phonenumbers.parse(telefono)):
                raise forms.ValidationError(
                    "El formato del teléfono debe ser: +56912345678")
        except:
            raise forms.ValidationError(
                "El formato del teléfono debe ser: +56912345678")
        return telefono


class FormularioRegistroTrabajador(FormularioRegistroCliente):
    tipo_trabajador = forms.ChoiceField(label="Tipo Trabajador",
                                        choices=Trabajador.TRABAJADOR_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Trabajador
        fields = ['email', 'nombre', 'primer_apellido', 'segundo_apellido',
                  'rut', 'telefono', 'tipo_trabajador']
