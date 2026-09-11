from django.contrib import admin
from django.urls import include, path
from gimnasio.views import portada

urlpatterns = [
    path("", portada, name="portada"),
    path("gimnasio/", include("gimnasio.urls")),
    path("ejercicios/", include("ejercicios.urls")),
    path("admin/", admin.site.urls),
]