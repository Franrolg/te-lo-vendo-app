from django.db import models


class FormaPago(models.Model):
    nombre = models.CharField(max_length=30)
    habilitado = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.nombre


class Comuna(models.Model):
    nombre = models.CharField(max_length=50)
    region = models.ForeignKey("Region", on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.nombre}, {self.region.nombre}'


class Region(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nombre


class Mantenedores(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.nombre


class MedioPedido(Mantenedores):
    pass


class EstadoPedido(Mantenedores):
    pass


class TipoProducto(Mantenedores):
    pass
