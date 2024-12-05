from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import mercadopago
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from .models import Cliente, Estado, Plan, CodigoDescuento

PUBLIC_KEY = 'TEST-055ecb2c-e0ed-49c3-adf0-f714bc173c3d'
ACCESS_TOKEN = 'TEST-1846613135498560-112319-d1471b37c56b35a15b8f9e0027f8be0d-245524862'
logger = logging.getLogger(__name__)
def home(request):
    # Obtener todos los planes de la base de datos
    planes = Plan.objects.all()
    return render(request, 'home.html', {'planes': planes})

def validar_codigo_descuento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codigo = data.get('codigo')
        try:
            descuento = CodigoDescuento.objects.get(codigo=codigo)
            return JsonResponse({
                'success': True,
                'plan_nombre': descuento.plan.nombre,
                'plan_id': descuento.plan.id
            })
        except CodigoDescuento.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Código no válido'})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def select_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    request.session['selected_plan_id'] = plan.id
    request.session['selected_plan_name'] = plan.nombre
    request.session['selected_plan_price'] = plan.precio
    return redirect('contratación')
def contratación(request):
    selected_plan = {
        'id': request.session.get('selected_plan_id'),
        'name': request.session.get('selected_plan_name'),
        'price': request.session.get('selected_plan_price'),
    }
    return render(request, 'contratación.html', {'selected_plan': selected_plan})
def guardar_cliente(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        estado_default = Estado.objects.get(pk=1)
        plan = Plan.objects.get(pk=data['plan'])
        
        cliente = Cliente.objects.create(
            nombre=data['nombre'],
            empresa_pagina=data.get('empresa'),
            correo=data['correo'],
            numero_contacto=data['telefono'],
            proyecto=data['comentario'],
            estado=estado_default,
            plan=plan,
        )
        
        return JsonResponse({'message': 'Cliente guardado exitosamente'}, status=200)
    return JsonResponse({'error': 'Método no permitido'}, status=405)



def pago(request):
    return render(request, 'pago.html')
@csrf_exempt
def procesar_pago(request):
    if request.method == "POST":
        # Inicializar el SDK de Mercado Pago
        sdk = mercadopago.SDK(ACCESS_TOKEN)

        try:
            logger.info("Inicio del procesamiento de pago")

            # Leer y decodificar el cuerpo JSON
            body_unicode = request.body.decode('utf-8')
            logger.debug("Cuerpo bruto recibido: %s", body_unicode)

            try:
                body_data = json.loads(body_unicode)
                logger.debug("JSON recibido: %s", body_data)
            except json.JSONDecodeError as e:
                logger.error("Error al decodificar JSON: %s", str(e))
                return JsonResponse({"error": "Cuerpo de la solicitud no es un JSON válido."}, status=400)

            # Validar el campo transaction_amount
            transaction_amount = body_data.get("transaction_amount")
            logger.debug("transaction_amount recibido: %s", transaction_amount)

            if transaction_amount is None:
                logger.error("El monto de la transacción no está presente en el JSON.")
                return JsonResponse({"error": "El monto de la transacción es obligatorio."}, status=400)

            try:
                transaction_amount = float(transaction_amount)  # Convertir a float
                logger.debug("Monto de la transacción convertido a float: %s", transaction_amount)
            except ValueError:
                logger.error("El monto de la transacción no es un número válido: %s", transaction_amount)
                return JsonResponse({"error": "El monto de la transacción debe ser un número válido."}, status=400)

            # Validar el método de pago
            payment_method = body_data.get("payment_method")
            logger.debug("payment_method recibido: %s", payment_method)
            if not payment_method:
                logger.error("El método de pago no está presente en el JSON.")
                return JsonResponse({"error": "El método de pago es obligatorio."}, status=400)

            # Preparar los datos para Mercado Pago
            payment_data = {
                "transaction_amount": transaction_amount,
                
                "description": body_data.get("description", "Compra de producto/servicio"),
            }
            logger.debug("Datos de pago preparados: %s", payment_data)


            payment_data["auto_return"] = "approved"

            # Crear el pago con Mercado Pago
            payment_response = sdk.payment().create(payment_data)
            payment = payment_response["response"]
            print(payment)
            logger.info("Respuesta de Mercado Pago: %s", payment)
            print("=== Respuesta de Mercado Pago ===")
            print(json.dumps(payment, indent=4))  
            print("=== Fin de la respuesta ===")

            return JsonResponse(payment)

        except Exception as e:
            logger.error("Error procesando el pago: %s", str(e), exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)

    logger.warning("Método no permitido para esta URL: %s", request.method)
    return JsonResponse({"error": "Método no permitido."}, status=405)

@csrf_exempt
def process_payment(request):
    if request.method == "POST":
        sdk = mercadopago.SDK("TEST-ACCESS-TOKEN")
        data = json.loads(request.body)

        payment_data = {
            "transaction_amount": data.get("transaction_amount"),
            "token": data.get("token"),
            "description": "Compra en mi tienda",
            "installments": data.get("installments"),
            "payment_method_id": data.get("payment_method_id"),
            "payer": {
                "email": data.get("payer").get("email"),
                "identification": data.get("payer").get("identification"),
            }
        }

        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]

        return JsonResponse(payment)

    return JsonResponse({"error": "Método no permitido"}, status=405)

def pago_exitoso(request):
    return render(request, 'pago_exitoso.html')

def pago_fallido(request):
    return render(request, 'pago_fallido.html')

def pago_pendiente(request):
    return render(request, 'pago_pendiente.html')