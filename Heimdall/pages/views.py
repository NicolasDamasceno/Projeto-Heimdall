from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from .models import Aluno, Entrada, Usuario
from .forms import EntradaForm
from polymorphic.query import PolymorphicQuerySet

# Create your views here.

class PaginaInicial(TemplateView):
    template_name = 'design/index.html'

def registrar_entrada(request):
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            cpf_ou_matricula = form.cleaned_data['cpf_ou_matricula']

            usuario = None
            # Primeiro tenta buscar pelo CPF
            usuario = Usuario.objects.filter(cpf=cpf_ou_matricula).first()

            # Se não encontrar pelo CPF, tenta buscar pela matrícula (apenas em Aluno)
            if not usuario:
                usuario = Usuario.objects.instance_of(Aluno).filter(aluno__matricula=cpf_ou_matricula).first()

            if usuario:
                # Registra a entrada
                entrada = Entrada.objects.create(id_usuario=usuario)
                return HttpResponse(f"Entrada registrada com sucesso: {usuario.nome} às {entrada.data_entrada}")
            else:
                return HttpResponse("Usuário não encontrado.")
        else:
            return render(request, 'pages/registro_usuario.html', {'form': form, 'errors': form.errors})

    else:
        form = EntradaForm()

    return render(request, 'pages/registro_usuario.html', {'form': form})