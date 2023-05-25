from django import forms
from .models import Usuario, Cliente, Direccion

class FormularioUsuario(forms.ModelForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Correo Electrónico'}))
    
    class Meta:
        model = Usuario
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con ese email")
        return email

class FormularioDireccion(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = [] 

class FormularioRegistroCliente(FormularioUsuario):
    nombre = forms.CharField(label="",max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre'}))
    primer_apellido = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Primer Apellido'}))
    segundo_apellido = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Segundo Apellido'}))
    rut = forms.CharField(label="",max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'RUT'}))
    telefono = forms.CharField(label="",max_length=12, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Teléfono'}))

    class Meta:
        model = Cliente
        fields = ['email', 'nombre', 'primer_apellido', 'segundo_apellido', 'rut', 'telefono']
