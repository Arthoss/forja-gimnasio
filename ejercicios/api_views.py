from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Ejercicio, Categoria
from .serializers import EjercicioSerializer, CategoriaSerializer


@swagger_auto_schema(method="get", operation_description="Lista todas las categorías de ejercicios")
@api_view(["GET"])
def api_lista_categorias(request):
    categorias = Categoria.objects.all()
    return Response(CategoriaSerializer(categorias, many=True).data)


@swagger_auto_schema(method="get", operation_description="Lista ejercicios de una categoría, opcionalmente filtrados por nivel (?nivel=avanzado)")
@api_view(["GET"])
def api_ejercicios_por_categoria(request, categoria_id):
    ejercicios = Ejercicio.objects.filter(categoria_id=categoria_id)
    nivel = request.GET.get("nivel")
    if nivel:
        ejercicios = ejercicios.filter(nivel=nivel)
    return Response(EjercicioSerializer(ejercicios, many=True).data)