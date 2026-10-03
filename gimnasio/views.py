import requests
import os
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.shortcuts import redirect
from .forms import ClaseForm
from .models import Clase, Inscripcion
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST


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
    """Muestra el tip recién editado (una sola vez) o uno aleatorio del Flask."""
    tip = request.session.pop("tip_editado", None)
    if tip is not None:
        servicio = "Ruby (Sinatra): actualizó este tip"
    else:
        url_microservicio = "https://forja-microservicio.onrender.com/api/tip"
        tip_por_defecto = {"texto": "Entrena con constancia, los resultados llegan solos.", "categoria": "general"}
        try:
            respuesta = requests.get(url_microservicio, timeout=6)
            respuesta.raise_for_status()
            tip = respuesta.json()
            if tip.get("origen") == "respaldo":
                servicio = "Ruby (Sinatra): respaldo, el Flask no pudo leer la base"
            else:
                servicio = "Flask (Python)"
        except requests.RequestException:
            tip = tip_por_defecto
            servicio = "Ninguno: tip por defecto, el Flask no respondió"
    return render(request, "gimnasio/tip_del_dia.html", {"tip": tip, "servicio": servicio})

def preguntas(request):
    """Vista tipo chat: la IA responde usando el contexto real de la base de datos,
    obtenido consultando nuestro propio endpoint público /api/clases/."""
    respuesta = None
    pregunta = ""

    if request.method == "POST":
        pregunta = request.POST.get("pregunta", "").strip()

        if pregunta:
            # 1) Leemos los datos reales de la base de datos
            lineas = []
            for c in Clase.objects.all():
                lineas.append(
                    f"- {c.nombre} (instructor: {c.instructor}): "
                    f"{c.cupos_disponibles()} de {c.cupo_maximo} cupos disponibles."
                )
            contexto_datos = "\n".join(lineas) if lineas else "Actualmente no hay clases registradas."

            # 2) Armamos la instrucción para Gemini incluyendo esos datos reales como contexto
            api_key = os.environ.get("GEMINI_API_KEY")

            # 2) Armamos la instrucción para Gemini incluyendo esos datos reales como contexto
            api_key = os.environ.get("GEMINI_API_KEY")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"

            instrucciones = (
                "Eres un asistente del gimnasio FORJA. Responde de forma breve y clara "
                "preguntas relacionadas con entrenamiento, rutinas, ejercicios, nutrición "
                "deportiva y motivación. Además, tienes acceso a los datos reales y actuales "
                "de las clases del gimnasio, obtenidos en este momento desde nuestra base de datos:\n\n"
                f"{contexto_datos}\n\n"
                "Usa esta información cuando el usuario pregunte por disponibilidad de cupos, "
                "instructores o clases específicas. Si preguntan algo fuera de estos temas, "
                "responde amablemente que solo puedes ayudar con temas del gimnasio."
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
            except (requests.RequestException, KeyError, IndexError):
                respuesta = "No pude conectarme con el asistente en este momento. Intenta de nuevo más tarde."
        else:
            respuesta = "Escribe una pregunta antes de enviar."

    return render(request, "gimnasio/preguntas.html", {
        "pregunta": pregunta,
        "respuesta": respuesta,
    })

def clase_crear(request):
    if request.method == "POST":
        form = ClaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gimnasio:index")
    else:
        form = ClaseForm()
    return render(request, "gimnasio/clase_form.html", {"form": form, "modo": "Crear"})


def clase_editar(request, clase_id):
    clase = get_object_or_404(Clase, pk=clase_id)
    if request.method == "POST":
        form = ClaseForm(request.POST, instance=clase)
        if form.is_valid():
            form.save()
            return redirect("gimnasio:detail", clase_id=clase.id)
    else:
        form = ClaseForm(instance=clase)
    return render(request, "gimnasio/clase_form.html", {"form": form, "modo": "Editar"})


def clase_eliminar(request, clase_id):
    clase = get_object_or_404(Clase, pk=clase_id)
    if request.method == "POST":
        clase.delete()
        return redirect("gimnasio:index")
    return render(request, "gimnasio/clase_confirmar_eliminar.html", {"clase": clase})

RUBY_URL = os.environ.get("RUBY_URL", "https://forja-ms-actualizar.onrender.com")
NODE_URL = os.environ.get("NODE_URL", "https://forja-ms-eliminar.onrender.com")


@require_POST
def tip_editar(request, tip_id):
    """Llama al microservicio Ruby (PUT /tips/{id}) para actualizar el tip."""
    cuerpo = {}
    texto = request.POST.get("texto", "").strip()
    categoria = request.POST.get("categoria", "").strip()
    if texto:
        cuerpo["texto"] = texto
    if categoria:
        cuerpo["categoria"] = categoria
    if not cuerpo:
        messages.error(request, "Escribe un texto y/o una categoría.")
        return redirect("gimnasio:tip_del_dia")
    try:
        r = requests.put(f"{RUBY_URL}/tips/{tip_id}", json=cuerpo, timeout=25)
        if r.status_code == 404:
            messages.error(request, "Ese tip ya no existe.")
            return redirect("gimnasio:tip_del_dia")
        r.raise_for_status()
        request.session["tip_editado"] = r.json()["tip"]
        messages.success(request, "Tip actualizado correctamente (microservicio Ruby).")
        return redirect("gimnasio:tip_del_dia")
    except (requests.RequestException, KeyError, ValueError):
        messages.error(request, "No se pudo actualizar. Intenta de nuevo en un momento.")
        return redirect("gimnasio:tip_del_dia")


@require_POST
def tip_eliminar(request, tip_id):
    """Llama al microservicio Node (DELETE /tips/{id}) para eliminar el tip."""
    try:
        r = requests.delete(f"{NODE_URL}/tips/{tip_id}", timeout=25)
        if r.status_code == 404:
            messages.error(request, "Ese tip ya no existe.")
        else:
            r.raise_for_status()
            messages.success(request, "Tip eliminado correctamente (microservicio Node.js).")
    except requests.RequestException:
        messages.error(request, "No se pudo eliminar. Intenta de nuevo en un momento.")
    return redirect("gimnasio:tip_del_dia")

def docentes(request):
    """Muestra los docentes involucrados en el proyecto."""
    lista_docentes = [
        {"nombre": "Elfar Didier Morantes Sanchez", "foto": "css/elfar.png"},
        {"nombre": "Omar Andres Bonilla Acosta", "foto": "css/omar.png"},
    ]
    return render(request, "gimnasio/docentes.html", {"docentes": lista_docentes})