from django.contrib import admin
from .models import Clase, Inscripcion


class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 1


class ClaseAdmin(admin.ModelAdmin):
    fields = ["nombre", "instructor", "descripcion", "cupo_maximo", "fecha_publicacion"]
    inlines = [InscripcionInline]
    list_display = ["nombre", "instructor", "fecha_publicacion"]
    search_fields = ["nombre", "instructor"]


admin.site.register(Clase, ClaseAdmin)