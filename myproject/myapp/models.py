from django.db import models

# Create your models here.
class Proveedor(models.Model):
    empresa = models.CharField(max_length=100)
    tecnologia = models.CharField(max_length=100)
    segmento = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    velocidad = models.CharField(max_length=100)
    conexiones = models.IntegerField()
    router_id = models.ForeignKey('Router', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.empresa} - {self.tecnologia} ({self.segmento}) ({self.departamento}) ({self.velocidad}) ({self.conexiones})"


class Router(models.Model):
    router_id = models.AutoField(primary_key=True)
    departamento = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.router_id} ({self.departamento})"
    