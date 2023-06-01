from django.db import models
import locale


class Producto(models.Model):
    sku = models.CharField(
        max_length=50, primary_key=True, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    stock = models.IntegerField()
    precio = models.IntegerField()
    url_imagen = models.CharField()
    tipo = models.ForeignKey("gestion.TipoProducto", on_delete=models.PROTECT)
    creado_por = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.PROTECT, related_name="productos_creados")
    actualizado_por = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.PROTECT, null=True, related_name="productos_actualizados")

    def mostrar_precio(self):
        return f'${self.precio}'


class Pedido(models.Model):
    cliente = models.ForeignKey(
        "usuarios.Cliente", on_delete=models.PROTECT, related_name="pedidos")
    medio = models.ForeignKey("gestion.MedioPedido", on_delete=models.PROTECT)
    estado = models.ForeignKey(
        "gestion.EstadoPedido", on_delete=models.PROTECT)
    forma_pago = models.ForeignKey(
        "gestion.FormaPago", on_delete=models.PROTECT)
    direccion = models.ForeignKey(
        "usuarios.Direccion", on_delete=models.PROTECT)
    creado_por = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.PROTECT, related_name="pedidos_creados")
    actualizado_por = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.PROTECT, null=True, related_name="pedidos_actualizados")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)

    def precio_total(self):
        # Configuración del locale para Chile
        locale.setlocale(locale.LC_ALL, 'es_CL.utf8')
        precio_total = sum(
            [detalle.precio for detalle in self.detallepedido_set.all()])
        return locale.currency(precio_total, symbol=True, grouping=True)


class DetallePedido(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, to_field='sku')
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio = models.PositiveBigIntegerField()

    def mostrar_precio(self):
        locale.setlocale(locale.LC_ALL, 'es_CL.utf8')
        return locale.currency(self.precio, symbol=True, grouping=True)
