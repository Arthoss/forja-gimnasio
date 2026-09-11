from django.contrib import admin
from .models import Categoria, Ejercicio


class EjercicioInline(admin.TabularInline):
    model = Ejercicio
    extra = 1


class CategoriaAdmin(admin.ModelAdmin):
    inlines = [EjercicioInline]
    list_display = ["nombre"]
    search_fields = ["nombre"]


class EjercicioAdmin(admin.ModelAdmin):
    list_display = ["nombre", "categoria", "nivel", "series", "repeticiones"]
    list_filter = ["categoria", "nivel"]
    search_fields = ["nombre"]


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Ejercicio, EjercicioAdmin)