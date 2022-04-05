from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from disc_website.forms import PerguntaForm
from disc_website.models import Pergunta

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
    
def respostas(request):
    return render(request, "disc_website/respostas.html")
    