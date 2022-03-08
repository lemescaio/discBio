from django.shortcuts import render
from django.http import HttpResponse

from disc_website.models import Pergunta

# Create your views here.
def home(request):
    return render(request, "disc_website/home.html",
    {"perguntas": Pergunta.objects.all()})
