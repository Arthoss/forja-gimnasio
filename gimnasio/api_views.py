import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Clase
from .serializers import ClaseSerializer


@swagger_auto_schema(method="get", operation_description="Lista todas las clases del gimnasio")
@api_view(["GET"])
def api_lista_clases(request):
    clases = Clase.objects.order_by("-fecha_publicacion")
    data = ClaseSerializer(clases, many=True).data
    return Response(data)


@swagger_auto_schema(method="get", operation_description="Obtiene el detalle de una clase por su ID")
@api_view(["GET"])
def api_detalle_clase(request, clase_id):
    try:
        clase = Clase.objects.get(pk=clase_id)
    except Clase.DoesNotExist:
        return Response({"error": "Clase no encontrada"}, status=404)
    return Response(ClaseSerializer(clase).data)


@swagger_auto_schema(
    method="get",
    operation_description="Obtiene un tip de entrenamiento aleatorio (consulta el microservicio propio en Supabase)",
)
@api_view(["GET"])
def api_tip(request):
    url = "https://forja-microservicio.onrender.com/api/tip"
    try:
        resp = requests.get(url, timeout=8)
        resp.raise_for_status()
        return Response(resp.json())
    except requests.RequestException:
        return Response({"error": "Microservicio no disponible"}, status=503)


pregunta_param = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={"pregunta": openapi.Schema(type=openapi.TYPE_STRING, description="Pregunta sobre entrenamiento")},
    required=["pregunta"],
)


@swagger_auto_schema(
    method="post",
    operation_description="Envía una pregunta sobre entrenamiento/rutinas a la IA (Gemini) y devuelve la respuesta",
    request_body=pregunta_param,
)
@api_view(["POST"])
def api_preguntas(request):
    pregunta = request.data.get("pregunta", "").strip()
    if not pregunta:
        return Response({"error": "Debes enviar una pregunta"}, status=400)

    api_key = os.environ.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    instrucciones = (
        "Eres un asistente del gimnasio FORJA. Responde de forma breve y clara "
        "solo preguntas relacionadas con entrenamiento, rutinas, ejercicios, "
        "nutrición deportiva y motivación para hacer ejercicio."
    )
    cuerpo = {
        "contents": [{"parts": [{"text": pregunta}]}],
        "systemInstruction": {"parts": [{"text": instrucciones}]},
    }
    try:
        resp = requests.post(url, json=cuerpo, timeout=15)
        resp.raise_for_status()
        datos = resp.json()
        respuesta = datos["candidates"][0]["content"]["parts"][0]["text"]
        return Response({"pregunta": pregunta, "respuesta": respuesta})
    except (requests.RequestException, KeyError, IndexError):
        return Response({"error": "No se pudo consultar el asistente"}, status=503)