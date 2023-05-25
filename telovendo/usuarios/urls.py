from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registrar_cliente, name='registro'),
    path('logout', views.cerrar_sesion, name='cerrar sesion')
]