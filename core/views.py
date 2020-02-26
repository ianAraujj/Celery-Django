from django.shortcuts import render, HttpResponse
from core.models import Atualizacao

# Create your views here.

def mainHome(request):
    at = []
    for i in Atualizacao.objects.all():
        at.append((i.data, i.tipo))

    context = {
        "atualizacoes": at
    }
    return render(request, 'home.html', context)