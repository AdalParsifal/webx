from django.db import models

class Plan(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.PositiveIntegerField()
    precio_anual = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre
 
class CodigoDescuento(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)  # Relaciona el código de descuento con un plan específico

    def __str__(self):
        return f"{self.codigo} - {self.plan.nombre}"    


class Estado(models.Model):
    ESTADOS_CHOICES = [
        ('No Captado', 'No Captado'),
        ('Suscrito', 'Suscrito'),
        ('Suscrito-Activo', 'Suscrito-Activo'),
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Captado Rechazado', 'Captado Rechazado'),
    ]
    
    nombre = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='No Captado')

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    empresa_pagina = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(max_length=255)
    numero_contacto = models.CharField(max_length=20)
    proyecto = models.TextField()
    estado = models.ForeignKey(Estado, on_delete=models.SET_DEFAULT, default=1)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.empresa_pagina})"


class Pago(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago #{self.id} - Cliente: {self.cliente.nombre}"
