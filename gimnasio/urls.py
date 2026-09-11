from django.urls import path

from . import views

app_name = "gimnasio"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:clase_id>/", views.detail, name="detail"),
    path("<int:clase_id>/inscribirse/", views.inscribirse, name="inscribirse"),
    path("motivacion/", views.motivacion, name="motivacion"),
]