from django.contrib import admin
from .models import Cliente, Plan, Estado, Pago, CodigoDescuento

# Registramos los modelos en el sitio de administración
admin.site.register(Cliente)
admin.site.register(Plan)
admin.site.register(Estado)
admin.site.register(Pago)
admin.site.register(CodigoDescuento)