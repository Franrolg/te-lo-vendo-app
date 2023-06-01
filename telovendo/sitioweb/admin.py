from django.contrib import admin
from . import models


@admin.register(models.Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'tipo']


@admin.register(models.Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'estado', 'medio', 'forma_pago']
