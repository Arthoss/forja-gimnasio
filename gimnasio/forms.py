from django import forms
from .models import Clase


class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ["nombre", "instructor","sede","descripcion", "cupo_maximo", "fecha_publicacion"]
        widgets = {
            "fecha_publicacion": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }