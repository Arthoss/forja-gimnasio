from django.contrib import admin
from django.urls import include, path
from gimnasio.views import portada
from gimnasio import api_views as gimnasio_api
from ejercicios import api_views as ejercicios_api
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="FORJA API",
        default_version="v1",
        description="Documentación de la API de FORJA (clases, ejercicios, tips y asistente IA)",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", portada, name="portada"),
    path("gimnasio/", include("gimnasio.urls")),
    path("ejercicios/", include("ejercicios.urls")),

    # Endpoints de API (JSON)
    path("api/clases/", gimnasio_api.api_lista_clases, name="api_lista_clases"),
    path("api/clases/<int:clase_id>/", gimnasio_api.api_detalle_clase, name="api_detalle_clase"),
    path("api/tip/", gimnasio_api.api_tip, name="api_tip"),
    path("api/preguntas/", gimnasio_api.api_preguntas, name="api_preguntas"),
    path("api/ejercicios/categoria/<int:categoria_id>/", ejercicios_api.api_ejercicios_por_categoria, name="api_ejercicios_por_categoria"),
    path("api/ejercicios/categorias/", ejercicios_api.api_lista_categorias, name="api_lista_categorias"),

    # Documentación Swagger
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-docs"),
]