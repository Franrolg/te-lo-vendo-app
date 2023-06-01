from django.contrib import admin
from . import models


@admin.register(models.FormaPago)
class FormaPagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']


@admin.register(models.Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'region']


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']


@admin.register(models.MedioPedido)
class MedioPedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']


@admin.register(models.EstadoPedido)
class EstadoPedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']


@admin.register(models.TipoProducto)
class TipoProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
