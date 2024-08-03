from django.shortcuts import render
from .models import Tamanho, TipoSabor, Acompanhamento
# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')


def cardapio(request):
    tamanho = Tamanho.objects.filter(ativo=True)
    tipo_sabor = TipoSabor.objects.filter(ativo=True)
    acompanhamento = Acompanhamento.objects.filter(ativo=True)
    context = {
        'tamanho': tamanho,
        'tipo_sabor': tipo_sabor,
        'acompanhamento': acompanhamento,
    }
    return render(request, 'cardapio.html', context)