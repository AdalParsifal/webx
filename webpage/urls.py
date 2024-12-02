from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path ('contratación/', views.contratación, name='contratación' ),
    path('pago/', views.pago, name='pago'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),

    # Opcionales: Rutas para el flujo de resultados del pago
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago_fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago_pendiente/', views.pago_pendiente, name='pago_pendiente'),
]