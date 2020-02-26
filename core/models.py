from django.db import models

# Create your models here.

class Atualizacao(models.Model):
    data = models.DateTimeField()
    tipo = models.TextField(max_length=30)