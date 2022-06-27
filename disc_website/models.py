from django.db import models
import uuid
import hashlib

# Create your models here.

class Turma(models.Model):
  curso = models.CharField(max_length=50)
  ano = models.IntegerField()
  semestre = models.IntegerField() #TODO: Semestre é um enum


class Aluno(models.Model):
  nome = models.CharField(max_length=30)
  ra = models.IntegerField(unique=True, blank=False)
  email = models.EmailField(max_length=254, blank=False)
  aluno_empregado = models.BooleanField(default=False)
  cpf = models.CharField(max_length=11, default='11111111111')
  #turma = models.ManyToManyField(Turma)

  def save(self, *args, **kwargs):
        self.cpf = hashlib.md5(self.cpf)
        super(Aluno, self).save(*args, **kwargs)

  def __str__(self):
    return str(self.ra)

class Resultado(models.Model):
  aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
  data_ini = models.DateTimeField()
  data_fim = models.DateTimeField()
  influencia = models.FloatField()
  dominancia = models.FloatField()
  cautela = models.FloatField()
  estabilidade = models.FloatField()
  resultado_final = models.CharField(max_length=255, default="")

  # verifica o resultado final e retorna como string
  def get_resultado_final(self):
    res_perfis = [("Dominante", self.dominancia), 
                  ("Influente",self.influencia), 
                  ("Cauteloso",self.cautela), 
                  ("Estável",self.estabilidade)]
    res_perfis.sort(reverse=True, key=lambda t: t[1])
    res = ""
    for perfil in res_perfis:  
      if perfil[1] == res_perfis[0][1]:
        res += perfil[0] + ' '
    return res

  # chama get_resultado_final() e armazena o valor na propriedade resultado_final
  def save(self, *args, **kwargs): 
    self.resultado_final = self.get_resultado_final()
    super(Resultado, self).save(*args, **kwargs)
  
  def __str__(self):
      return ' - '.join([str(self.aluno.ra), self.data_fim.isoformat()])

CHOICES_TIPO = (
  (1,'check-box'),
  (2,'radio-button'),
)

class Teste(models.Model):
  nome = models.CharField(max_length=30)
  tipo = models.IntegerField(choices=CHOICES_TIPO, blank=False)

  def __str__(self):
    return self.nome

class Pergunta(models.Model):
  teste = models.ForeignKey(Teste, on_delete=models.CASCADE)
  enunciado = models.TextField(max_length=140)
  
  def __str__(self):
    return self.enunciado

CHOICES_ALTERNATIVA = (
  (1,'dominancia'),
  (2,'influencia'),
  (3,'cautela'),
  (4,'estabilidade'),
)

class Alternativa(models.Model):
  pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
  conteudo = models.CharField(max_length=140, blank=False)
  perfil = models.IntegerField(choices=CHOICES_ALTERNATIVA, blank=False)
  
  def __str__(self):
    return ' - '.join([self.conteudo, 
        self.pergunta.__str__()[:15]+'...',
        self.pergunta.teste.__str__()])

class Universidade(models.Model):
  nome = models.CharField(max_length=500, blank=False)

  def __str__(self):
    return self.nome

class Link(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  expire_date = models.DateTimeField()
  apelido = models.CharField(max_length=150, blank=False)
  teste = models.ForeignKey(Teste, on_delete=models.CASCADE)
  universidade = models.ForeignKey(Universidade, on_delete=models.CASCADE)

  @property
  def link(self):
    return '<a href="/teste/{}" target=_blank>Link</a>'.format(str(self.id))


