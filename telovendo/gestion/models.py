from django.db import models

class FormaPago(models.Model):
    nombre = models.CharField(max_length=30)
    habilitado = models.BooleanField(default=True)

class Comuna(models.Model):
    nombre = models.CharField(max_length=50)
    region = models.ForeignKey("Region", on_delete=models.PROTECT)

class Region(models.Model):
    nombre = models.CharField(max_length=50)

class Mantenedores(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=200)

    class Meta:
        abstract = True

class MedioPedido(Mantenedores): pass

class EstadoPedido(Mantenedores): pass

class TipoProducto(Mantenedores): pass