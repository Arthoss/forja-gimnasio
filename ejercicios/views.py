from django.shortcuts import get_object_or_404, render
from .models import Categoria, Ejercicio


def index(request):
    """Lista todas las categorías de ejercicios."""
    lista_categorias = Categoria.objects.all()
    return render(request, "ejercicios/index.html", {"lista_categorias": lista_categorias})


def por_categoria(request, categoria_id):
    """Ruta dinámica: usa categoria_id para consultar solo los ejercicios
    de esa categoría. Si llega ?nivel=... en la URL, filtra además por nivel."""
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    ejercicios = categoria.ejercicios.all()

    nivel = request.GET.get("nivel")
    if nivel in dict(Ejercicio.Nivel.choices):
        ejercicios = ejercicios.filter(nivel=nivel)

    return render(request, "ejercicios/por_categoria.html", {
        "categoria": categoria, "ejercicios": ejercicios,
        "nivel_actual": nivel, "niveles": Ejercicio.Nivel.choices,
    })


def detail(request, ejercicio_id):
    """Ruta dinámica: consulta un ejercicio puntual y sugiere otros de su misma categoría."""
    ejercicio = get_object_or_404(Ejercicio, pk=ejercicio_id)
    relacionados = ejercicio.categoria.ejercicios.exclude(pk=ejercicio.id)[:4]
    return render(request, "ejercicios/detail.html", {
        "ejercicio": ejercicio, "relacionados": relacionados,
    })