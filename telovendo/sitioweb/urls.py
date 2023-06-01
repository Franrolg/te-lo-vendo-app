from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'sitioweb'
urlpatterns = [
    path('productos', views.ProductosView.as_view(), name='productos'),
    path('pedidos', views.PedidosView.as_view(), name='pedidos'),
    path('mis_pedidos', views.MisPedidosView.as_view(), name='mis pedidos'),
    path('producto/<str:sku>/',
         views.ProductoView.as_view(), name='producto'),
    path('pedido/<int:pk>/',
         views.actualizar_pedido, name='pedido'),
    path('editar_producto/<str:sku>/',
         views.ActualizarProductoView.as_view(), name='editar_producto'),
    path('registrar_pedido/', views.registrar_pedido, name='registrar pedido'),
    path('registrar_pedido_usuario/', views.registrar_pedido_usuario,
         name='registrar pedido usuario'),
]
