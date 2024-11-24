from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path ('contratación/', views.contratación, name='contratación' ),
    path('pago/', views.pago, name='pago'),
    path('formulario_pago/', views.formulario_pago, name='formulario_pago'),
    path('payment_notification/', views.payment_notification, name='payment_notification'),
]