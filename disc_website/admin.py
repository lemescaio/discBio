from django.contrib import admin
from disc_website.models import Alternativa, Aluno, Resultado, Teste, Turma, Pergunta, Link

# Register your models here.

class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'dominancia', 'influencia' ,'cautela', 'estabilidade')
    search_fielda = ('aluno__ra__icontains',)

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('ra', 'nome', 'email')
    search_fields = ('ra_icontains', 'nome_icontains')

admin.site.register(Pergunta)
admin.site.register(Alternativa)
admin.site.register(Teste)
admin.site.register(Resultado, ResultadoAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Turma)
admin.site.register(Link)