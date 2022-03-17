from django.contrib import admin
from disc_website.models import Alternativa, Aluno, Resultado, Teste, Turma

from disc_website.models import Pergunta
# Register your models here.

admin.site.register(Turma)
admin.site.register(Aluno)
admin.site.register(Resultado)
admin.site.register(Teste)
admin.site.register(Alternativa)
admin.site.register(Pergunta)