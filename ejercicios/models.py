from django.db import models


class Categoria(models.Model):
    """Grupo muscular o tipo de ejercicio (ej. Piernas, Espalda, Cardio)."""
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre


class Ejercicio(models.Model):
    class Nivel(models.TextChoices):
        PRINCIPIANTE = "principiante", "Principiante"
        INTERMEDIO = "intermedio", "Intermedio"
        AVANZADO = "avanzado", "Avanzado"

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="ejercicios")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    series = models.PositiveIntegerField(default=3)
    repeticiones = models.PositiveIntegerField(default=12)
    nivel = models.CharField(max_length=20, choices=Nivel.choices, default=Nivel.PRINCIPIANTE)

    def __str__(self):
        return self.nombre