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
    path("clases/nueva/", views.clase_crear, name="clase_crear"),
    path("<int:clase_id>/editar/", views.clase_editar, name="clase_editar"),
    path("<int:clase_id>/eliminar/", views.clase_eliminar, name="clase_eliminar"),
        path("tip-del-dia/<int:tip_id>/editar/", views.tip_editar, name="tip_editar"),
    path("tip-del-dia/<int:tip_id>/eliminar/", views.tip_eliminar, name="tip_eliminar"),
]