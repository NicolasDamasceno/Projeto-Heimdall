from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from .models import Aluno, Entrada, Usuario
from .forms import EntradaForm

import logging

# Create your views here.

logger = logging.getLogger(__name__)


class PaginaInicial(TemplateView):
    template_name = 'pages/index.html'

def validar_entrada(request):
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            cpf_ou_matricula = form.cleaned_data['cpf_ou_matricula']
            dispositivo = form.cleaned_data['dispositivo']

            # Primeiro tenta buscar pelo CPF
            usuario = Usuario.objects.filter(cpf=cpf_ou_matricula).first()

            # Se não encontrar pelo CPF, tenta buscar pela matrícula (apenas em Aluno)
            if not usuario:
                usuario = Usuario.objects.filter(aluno__matricula=cpf_ou_matricula).first()

            if usuario:
                # Registra a entrada
                entrada = Entrada.objects.create(id_usuario=usuario, dispositivo=dispositivo)
                logger.info(f"Entrada registrada com sucesso: {usuario.nome} às {entrada.data_entrada} pelo {dispositivo}")
                return HttpResponse(f"Entrada registrada com sucesso: {usuario.nome} às {entrada.data_entrada} pelo {dispositivo}")
            else:
                logger.error("Usuário não encontrado.")
                return HttpResponse("Usuário não encontrado.")
        else:
            logger.error("Erro ao validar formulário.")
            return render(request, 'pages/validar_entrada.html', {'form': form, 'errors': form.errors})

    else:
        form = EntradaForm()

    return render(request, 'pages/validar_entrada.html', {'form': form})


def listar_entradas(request):
    entradas = Entrada.objects.select_related('id_usuario', 'dispositivo').all()
    return render(request, 'pages/listar_entradas.html', {'entradas': entradas})
