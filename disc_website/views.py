from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from pyexpat.errors import messages

from disc_website.forms import PerguntaForm
from disc_website.models import CHOICES_ALTERNATIVA, Alternativa, Aluno, Pergunta, Resultado, Link
import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from functools import reduce
from django.db.models import Q
import operator
import csv

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

@login_required(login_url='/login')
def resultados_csv(request):
    resultados = Resultado.objects.all()
    
    headers = ['Aluno', 'Data', 'Dominancia', 'Influência', 'Cautela', 'Estabilidade', 'Resultado final', 'Empregado?']
    data    = []

    for resultado in resultados:
        data.append(tuple([resultado.aluno.nome, 
                            resultado.data_fim.strftime("%m/%d/%Y %H:%M:%S"), 
                            str(resultado.dominancia*100)+'%',
                            str(resultado.influencia*100)+'%',
                            str(resultado.cautela*100)+'%',
                            str(resultado.estabilidade*100)+'%',
                            resultado.resultado_final,
                            'Sim' if resultado.aluno.aluno_empregado else 'Não']
                        ))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=resultados.csv; enconding=UTF-8;'

    writer = csv.writer(response, dialect='excel', delimiter=';')
    writer.writerow(headers)
    for d in data:
        writer.writerow(d)

    return response

@login_required(login_url='/login')
def resultados(request):
    if request.method == 'POST':
        busca = request.POST['buscaAluno']
        empregado = request.POST['empregado']
        desempregado = request.POST['desempregado']
        domin = request.POST['dominante']
        caute = request.POST['cauteloso']
        influ = request.POST['influente']
        estav = request.POST['estavel']
        
        listaPerfis = []
        if domin == 'on':
            listaPerfis.append("Dominante")
        if caute == 'on':
            listaPerfis.append("Cauteloso")
        if influ == 'on':
            listaPerfis.append("Influente")
        if estav == 'on':
            listaPerfis.append("Estável")
         
        if not busca:
            if empregado == 'on' and desempregado == '':
                alunos = Aluno.objects.filter(aluno_empregado='True')
            elif empregado == '' and desempregado == 'on':
                alunos = Aluno.objects.filter(aluno_empregado='False')
            elif empregado == 'on' and desempregado == 'on' or empregado == '' and desempregado == '':
                alunos = Aluno.objects.all()

        else:
            if empregado == 'on' and desempregado == '':
                alunos = Aluno.objects.filter(nome__icontains=busca, aluno_empregado='True')
            elif empregado == '' and desempregado == 'on':
                alunos = Aluno.objects.filter(nome__icontains=busca, aluno_empregado='False')
            elif empregado == 'on' and desempregado == 'on' or empregado == '' and desempregado == '':
                alunos = Aluno.objects.filter(nome__icontains=busca)

    else:
        alunos = Aluno.objects.all()
        listaPerfis = ["Dominante", "Cauteloso", "Influente", "Estável"]

    return render(request, "disc_website/resultados.html",
                  {"resultados": Resultado.objects.filter(reduce(operator.or_, (Q(aluno__in=alunos, resultado_final__contains=x) for x in listaPerfis))),
                   "navbar_resultados" : "active"})


def teste(request, id):
    #TODO: Criar um dicionario de perguntas/alternativas
    perguntas_dict = {}

    link = Link.objects.get(id=id)
    if link.expire_date < datetime.now().   replace(tzinfo=utc):
        return render(request, 'disc_website/404.html')

    if request.method == "GET":
        for pergunta in Pergunta.objects.filter(teste_id=link.teste.id):
            perguntas_dict[pergunta.enunciado] = Alternativa.objects.filter(pergunta=pergunta)
        return render(request, "disc_website/teste.html",
                      {"perguntas": perguntas_dict, "navbar_teste" : "active"})

    elif request.method == "POST":

        ra = request.POST["ra"]
        cpf = request.POST["cpf"]
        email = request.POST["email"]
        nome = request.POST["nome"]
        aluno_empregado = False
        if request.POST["aluno_empregado"] == '1':
            aluno_empregado = True

        listaPerguntasResp = []
        for chave, conteudo in request.POST.items():
            if chave not in ["csrfmiddlewaretoken", 'ra', 'email', 'nome','aluno_empregado', "cpf"]:
                listaPerguntasResp.append(chave)
        l = [x.split('__')[0] for x in listaPerguntasResp]

        perguntasTest = Pergunta.objects.filter(teste_id=link.teste.id).exclude(id__in = l)

        if not perguntasTest and ra != "" and nome != "" and email != "" and aluno_empregado != "":

            if len(request.POST) > 0:
                totalRespostas = 0
                respostas_dict = {
                    "1" : 0,
                    "2" : 0,
                    "3" : 0,
                    "4" : 0,
                }

                for chave, conteudo in request.POST.items():

                    if chave not in ["csrfmiddlewaretoken", 'ra', 'email', 'nome', 'aluno_empregado', "cpf"]:
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
                    aluno.cpf = cpf
                    aluno.email = email
                aluno.aluno_empregado = aluno_empregado
                aluno.save()

                resultado = Resultado()
                for choice, nome in CHOICES_ALTERNATIVA:
                    setattr(resultado, nome, respostas_dict[str(choice)])

                resultado.data_fim = resultado.data_ini = datetime.now()
                resultado.aluno = aluno
                resultado.save()

                return HttpResponseRedirect("/obrigado/{}".format(aluno.nome))
        else:
            aluno = Aluno()
            aluno.ra = ra
            aluno.nome = nome
            aluno.email = email
            aluno.cpf = cpf
            aluno.aluno_empregado = aluno_empregado

            respostasChave = []
            for pergunta in Pergunta.objects.filter(teste_id=link.teste.id):
                perguntas_dict[pergunta.enunciado] = Alternativa.objects.filter(pergunta=pergunta)

            for chave, conteudo in request.POST.items():
                if chave not in ["csrfmiddlewaretoken", 'ra', 'email', 'nome', 'aluno_empregado',"cpf"]:
                    respostasChave.append(chave)
            respostas = [int(x.split('__')[1]) for x in respostasChave]

            retorno = "****Responder todas as perguntas****"

            if ra == "":
                retorno = "Campo RA não informado."

            if email == "":
                retorno = "Campo email não informado."

            if nome == "":
                retorno = "Campo nome não informado."
            if cpf == "":
                retorno = "Campo nome não informado."

            return render(request, "disc_website/teste.html",
                          {"retorno": retorno, "perguntas": perguntas_dict, "aluno": aluno, "respostas": respostas,"navbar_teste": "active"})

def obrigado(request, nome):
    return render(request, "disc_website/obrigado.html",
                  {"nome": nome.split()[0]})
def logout_user(request):
    logout(request)
    return render(request, 'disc_website/logout.html')

def handler404(request, exception):
    return render(request, 'disc_website/404.html')

def login_user(request):
    logout(request)
    username = password = ''
    next = request.GET.get('next','/')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
    return render(request, 'disc_website/login.html', {'next' : next})