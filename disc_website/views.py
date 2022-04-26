from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from disc_website.forms import PerguntaForm
from disc_website.models import CHOICES_ALTERNATIVA, Alternativa, Aluno, Pergunta, Resultado, Link
import pytz

utc=pytz.UTC

# Create your views here.


def home(request):
    return render(request, "disc_website/home.html", 
                  {"perguntas": Pergunta.objects.all()})

def pergunta_form(request):
    if request.method == 'POST':
        form = PerguntaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = PerguntaForm()
    return render(request, 'disc_website/pergunta_form.html', {'form': form})

def resultados(request):
    if request.method == 'POST':
        busca = request.POST['buscaAluno']
        if not busca:
            alunos = Aluno.objects.all()
            return render(request, "disc_website/resultados.html",
                          {"resultados": Resultado.objects.filter(aluno__in=alunos),
                           "navbar_resultados": "active"})
        else:
            alunos = Aluno.objects.filter(nome__icontains=busca)
            return render(request, "disc_website/resultados.html",
                          {"resultados": Resultado.objects.filter(aluno__in=alunos),
                           "navbar_resultados": "active"})
    else:
        alunos = Aluno.objects.all()

    return render(request, "disc_website/resultados.html",
                  {"resultados": Resultado.objects.filter(aluno__in=alunos),
                   "navbar_resultados" : "active"})


def teste(request, id):
    #TODO: Criar um dicionario de perguntas/alternativas
    perguntas_dict = {}
    if request.method == "GET":
        link = Link.objects.get(id=id)
        if link.expire_date < datetime.now().replace(tzinfo=utc):
            return HttpResponseRedirect('/admin')

        for pergunta in Pergunta.objects.filter():
            perguntas_dict[pergunta.enunciado] = Alternativa.objects.filter(pergunta=pergunta)
        return render(request, "disc_website/teste.html",
                      {"perguntas": perguntas_dict, "navbar_teste" : "active"})
    elif request.method == "POST":
        print(request.POST)
        totalRespostas = 0
        respostas_dict = {
            "1" : 0,
            "2" : 0,
            "3" : 0,
            "4" : 0,
        }
        ra = request.POST["ra"]
        email = request.POST["email"]
        nome = request.POST["nome"]
        print (request.POST)
        for chave, conteudo in request.POST.items():
            if chave not in ["csrfmiddlewaretoken", 'ra', 'email', 'nome']:
                respostas_dict[conteudo[0]] += 1
                totalRespostas += 1
        
        for chave, conteudo in respostas_dict.items():
            respostas_dict[chave] = respostas_dict[chave] / totalRespostas
            
        try:
            aluno = Aluno.objects.get(ra=ra)
            
        except Aluno.DoesNotExist:
            aluno = Aluno()
            aluno.ra = ra
            aluno.nome = nome
            aluno.email = email
            aluno.save()
            
        resultado = Resultado()
        for choice, nome in CHOICES_ALTERNATIVA:
            setattr(resultado, nome, respostas_dict[str(choice)])
        
        resultado.data_fim = resultado.data_ini = datetime.now()
        resultado.aluno = aluno
        resultado.save()
        
        print(respostas_dict)
        return HttpResponseRedirect("/obrigado/{}".format(aluno.nome))

def obrigado(request, nome):
    return render(request, "disc_website/obrigado.html",
                  {"nome": nome.split()[0]})
