from dataclasses import fields
from django import forms
from disc_website.models import Pergunta

class PerguntaForm(forms.ModelForm):
    class Meta:
        fields = ['enunciado']
        model = Pergunta
