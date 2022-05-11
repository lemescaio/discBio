from django.contrib import admin
from disc_website.models import Alternativa, Aluno, Resultado, Teste, Turma, Pergunta, Link

# Register your models here.

class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'dominancia', 'influencia' ,'cautela', 'estabilidade', 'resultado_final')
    search_fields = ('aluno__ra__icontains',)

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('ra', 'nome', 'email', 'aluno_empregado')
    search_fields = ('ra_icontains', 'nome_icontains')

class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'expire_date', 'link')

admin.site.register(Pergunta)
admin.site.register(Alternativa)
admin.site.register(Teste)
admin.site.register(Resultado, ResultadoAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Turma)
admin.site.register(Link, LinkAdmin)