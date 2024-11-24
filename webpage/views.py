from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import mercadopago
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

PUBLIC_KEY = 'TEST-055ecb2c-e0ed-49c3-adf0-f714bc173c3d'
ACCESS_TOKEN = 'TEST-1846613135498560-112319-d1471b37c56b35a15b8f9e0027f8be0d-245524862'

def home(request):
    return render(request, 'home.html')

def contratación(request):
    return render(request, 'contratación.html')
def pago(request):
    return render(request, 'pago.html')
@csrf_exempt
def formulario_pago(request):
    if request.method == 'POST':
        # Obtener datos del formulario enviado
        nombre = request.POST.get('nombre')
        empresa = request.POST.get('empresa')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        comentario = request.POST.get('comentario')

        # Configurar el SDK de Mercado Pago con el Access Token
        sdk = mercadopago.SDK(ACCESS_TOKEN)

        # Crear la preferencia de pago
        preference_data = {
            "items": [
                {
                    "title": "Asesoría Web",
                    "quantity": 1,
                    "unit_price": 100.00  # Precio del servicio
                }
            ],
            "payer": {
                "name": nombre,
                "email": correo,
                "phone": {
                    "number": telefono
                }
            },
            "back_urls": {
                "success": "http://localhost:8000/pago_exitoso/",
                "failure": "http://localhost:8000/pago_fallido/",
                "pending": "http://localhost:8000/pago_pendiente/"
            },
            "auto_return": "approved"
        }

        # Llamar al API de Mercado Pago para crear la preferencia
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        # Renderizar la página de pago con la Public Key y Preference ID
        return render(request, 'pago.html', {
            'public_key': PUBLIC_KEY,
            'preference_id': preference['245524862']
        })

    # Renderizar el formulario inicial si el método es GET
    return render(request, 'formulario.html')


@csrf_exempt
def payment_notification(request):
    if request.method == 'POST':
        try:
            # Procesar la información enviada por Mercado Pago
            notification_data = json.loads(request.body)
            print("Notificación recibida:", notification_data)

            # Responder que la notificación fue recibida correctamente
            return JsonResponse({'status': 'received'})
        except json.JSONDecodeError:
            # Manejar errores en caso de datos mal formateados
            return JsonResponse({'error': 'Datos mal formateados'}, status=400)

    # Responder con error si el método no es POST
    return JsonResponse({'error': 'Método no permitido'}, status=405)