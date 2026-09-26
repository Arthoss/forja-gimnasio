from rest_framework import serializers
from .models import Clase


class ClaseSerializer(serializers.ModelSerializer):
    cupos_disponibles = serializers.SerializerMethodField()

    class Meta:
        model = Clase
        fields = ["id", "nombre", "instructor", "descripcion", "cupo_maximo", "cupos_disponibles", "fecha_publicacion"]

    def get_cupos_disponibles(self, obj):
        return obj.cupos_disponibles()