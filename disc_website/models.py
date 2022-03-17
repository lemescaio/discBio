from django.db import models

# Create your models here.

class Turma(models.Model):
    curso = models.IntegerField(max_length=50)
    ano = models.IntegerField()
    semestre = models.IntegerField() #TODO: Semestre é um enum

class Aluno(models.Model):
    nome = models.CharField(max_length=30)
    ra = models.IntegerField(unique=True, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    turma = models.ManyToManyField(Turma)

class Resultado(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_ini = models.DateField()
    data_fim = models.DateField()
    dominancia = models.FloatField()
    influencia = models.FloatField()
    cautela = models.FloatField()
    estabilidade = models.FloatField()

class Teste(models.Model):
    nome = models.CharField(max_length=30, blank=False)

class Pergunta(models.Model):
    teste = models.ForeignKey(Teste, on_delete=models.CASCADE)
    enunciado = models.TextField(max_length=140)
    
    def __str__(self) -> str:
        return super().__str__()
    
CHOICES_ALTERNATIVAS= (
    (1,'dominancia'),
    (2,'influencia'),
    (3,'cautela'),
    (4,'estabilidade'),
)

class Alternativa(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    conteudo = models.CharField(max_length=30)
    peso = models.FloatField()

def __str__(self):
    return ' _ '.join([self.conteudo, self.pergunta])
