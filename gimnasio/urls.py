from django.urls import path

from . import views

app_name = "gimnasio"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:clase_id>/", views.detail, name="detail"),
    path("<int:clase_id>/inscribirse/", views.inscribirse, name="inscribirse"),
    path("motivacion/", views.motivacion, name="motivacion"),
    path("tip-del-dia/", views.tip_del_dia, name="tip_del_dia"),
    path("preguntas/", views.preguntas, name="preguntas"),
]