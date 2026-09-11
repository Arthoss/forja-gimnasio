from django.urls import path
from . import views

app_name = "ejercicios"
urlpatterns = [
    path("", views.index, name="index"),
    path("categoria/<int:categoria_id>/", views.por_categoria, name="por_categoria"),
    path("<int:ejercicio_id>/", views.detail, name="detail"),
]