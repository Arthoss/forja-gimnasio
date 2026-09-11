from django.db import models


class Clase(models.Model):
    """Una clase que ofrece el gimnasio (ej. Spinning, Yoga, CrossFit)."""
    nombre = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    cupo_maximo = models.IntegerField(default=20)
    fecha_publicacion = models.DateTimeField("fecha de publicación")

    def __str__(self):
        return self.nombre

    def cupos_disponibles(self):
        return self.cupo_maximo - self.inscripcion_set.count()


class Inscripcion(models.Model):
    """Un miembro inscrito a una Clase (relación FK, como Choice -> Question)."""
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    nombre_miembro = models.CharField(max_length=100)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_miembro} en {self.clase.nombre}"