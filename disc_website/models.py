from django.db import models

# Create your models here.

class Pergunta(models.Model):
    enunciado = models.TextField(max_length=140)