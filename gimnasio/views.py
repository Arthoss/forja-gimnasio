import requests
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Clase, Inscripcion


def index(request):
    """Lista todas las clases del gimnasio, ordenadas por fecha de publicación."""
    lista_clases = Clase.objects.order_by("-fecha_publicacion")
    contexto = {"lista_clases": lista_clases}
    return render(request, "gimnasio/index.html", contexto)


def detail(request, clase_id):
    """Consulta el detalle de una clase específica y sus inscritos."""
    clase = get_object_or_404(Clase, pk=clase_id)
    return render(request, "gimnasio/detail.html", {"clase": clase})


def inscribirse(request, clase_id):
    """Modifica la base de datos: crea una nueva inscripción para la clase."""
    clase = get_object_or_404(Clase, pk=clase_id)
    nombre = request.POST.get("nombre_miembro", "").strip()

    if not nombre:
        return render(request, "gimnasio/detail.html", {
            "clase": clase,
            "error_message": "Debes escribir tu nombre para inscribirte.",
        })

    if clase.cupos_disponibles() <= 0:
        return render(request, "gimnasio/detail.html", {
            "clase": clase,
            "error_message": "Esta clase ya no tiene cupos disponibles.",
        })

    Inscripcion.objects.create(clase=clase, nombre_miembro=nombre)
    # Patrón Post/Redirect/Get, igual al de la vista 'vote' del tutorial oficial.
    return HttpResponseRedirect(reverse("gimnasio:detail", args=(clase.id,)))


def motivacion(request):
    """Consulta un microservicio externo (API pública) y muestra una frase motivacional."""
    frase_por_defecto = {
        "content": "El único mal entrenamiento es el que no hiciste.",
        "author": "Gimnasio",
    }
    try:
        respuesta = requests.get("https://api.quotable.io/random", timeout=4)
        respuesta.raise_for_status()
        datos = respuesta.json()
        frase = {"content": datos.get("content"), "author": datos.get("author")}
    except requests.RequestException:
        frase = frase_por_defecto

    return render(request, "gimnasio/motivacion.html", {"frase": frase})


def portada(request):
    """Página de inicio del sitio: enlaza a las clases y al catálogo de ejercicios."""
    total_clases = Clase.objects.count()
    total_inscripciones = Inscripcion.objects.count()
    return render(request, "gimnasio/portada.html", {
        "total_clases": total_clases,
        "total_inscripciones": total_inscripciones,
    })

def tip_del_dia(request):
    """Consume el microservicio propio (Flask + Supabase) para mostrar un tip aleatorio."""
    url_microservicio = "https://forja-microservicio.onrender.com/api/tip"
    tip_por_defecto = {"texto": "Entrena con constancia, los resultados llegan solos.", "categoria": "general"}
    try:
        respuesta = requests.get(url_microservicio, timeout=6)
        respuesta.raise_for_status()
        tip = respuesta.json()
    except requests.RequestException:
        tip = tip_por_defecto
    return render(request, "gimnasio/tip_del_dia.html", {"tip": tip})
