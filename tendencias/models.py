from django.db import models

# Create your models here.

class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to="imgPelicula")
    fecha_lanzamiento = models.DateField(null=True, blank=True, verbose_name="Fecha de lanzamiento")
    director = models.TextField()
    genero = models.TextField()   
    duracion = models.TextField()

    def __str__(self) :
        return self.titulo

    class Meta:
        verbose_name = "Pelicula"
        verbose_name_plural = "Peliculas"
