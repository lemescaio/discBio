from django.db import models

# Create your models here.

class Turma(models.Model):
  curso = models.CharField(max_length=50)
  ano = models.IntegerField()
  semestre = models.IntegerField() #TODO: Semestre é um enum


class Aluno(models.Model):
  nome = models.CharField(max_length=30)
  ra = models.IntegerField(unique=True, blank=False)
  email = models.EmailField(max_length=254, blank=False)
  turma = models.ManyToManyField(Turma)

class Resultado(models.Model):
  aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
  data_ini = models.DateTimeField()
  data_fim = models.DateTimeField()
  influencia = models.FloatField()
  dominancia = models.FloatField()
  cautela = models.FloatField()
  estabilidade = models.FloatField()


class Teste(models.Model):
  nome = models.CharField(max_length=30)

  def __str__(self):
    return self.nome

class Pergunta(models.Model):
  teste = models.ForeignKey(Teste, on_delete=models.CASCADE)
  enunciado = models.TextField(max_length=140)
  
  def __str__(self):
    return self.enunciado

CHOICES_ALTERNATIVA = (
  (1,'dominância'),
  (2,'influência'),
  (3,'cautela'),
  (4,'estabilidade'),
)
class Alternativa(models.Model):
  pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
  conteudo = models.CharField(max_length=30, blank=False)
  perfil = models.IntegerField(choices=CHOICES_ALTERNATIVA, blank=False)
  
  def __str__(self):
    return ' - '.join([self.conteudo, 
        self.pergunta.__str__()[:15]+'...',
        self.pergunta.teste.__str__()])

