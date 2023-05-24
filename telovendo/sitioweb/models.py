from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    stock = models.IntegerField()
    precio = models.IntegerField()
    url_imagen = models.CharField()
    tipo = models.ForeignKey("gestion.TipoProducto", on_delete=models.PROTECT)
    creado_por = models.ForeignKey("usuarios.Usuario", on_delete=models.PROTECT, related_name="productos_creados")
    actualizado_por = models.ForeignKey("usuarios.Usuario", on_delete=models.PROTECT, null=True, related_name="productos_actualizados")

class Pedido(models.Model):
    cliente = models.ForeignKey("usuarios.Cliente", on_delete=models.PROTECT, related_name="pedidos")
    medio = models.ForeignKey("gestion.MedioPedido", on_delete=models.PROTECT)
    estado = models.ForeignKey("gestion.EstadoPedido", on_delete=models.PROTECT)
    forma_pago = models.ForeignKey("gestion.FormaPago", on_delete=models.PROTECT)
    direccion = models.ForeignKey("usuarios.Direccion", on_delete=models.PROTECT)
    creado_por = models.ForeignKey("usuarios.Usuario", on_delete=models.PROTECT, related_name="pedidos_creados")
    actualizado_por = models.ForeignKey("usuarios.Usuario", on_delete=models.PROTECT, null=True, related_name="pedidos_actualizados")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)


class DetallePedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio = models.IntegerField()