from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import localtime, now
from django.views.generic import TemplateView
from .models import Aluno, Docente, Visitante, Entrada, Usuario, Dispositivo
from .forms import EntradaForm, LoginForm, RegisterAdminForm, VisitanteForm, CursoForm, DocenteForm, AlunoForm, DispositivoForm

import csv
import logging
import pytz

# Create your views here.

logger = logging.getLogger(__name__)

def obter_hora_local():
    fuso_horario = pytz.timezone('America/Fortaleza')
    return datetime.now(fuso_horario)


class PaginaInicial(TemplateView):
    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            hoje = now().date()
            total_alunos = Aluno.objects.count()
            total_docentes = Docente.objects.count()
            total_visitantes = Visitante.objects.count()
            entradas_hoje = Entrada.objects.filter(data_entrada__date=hoje).count()

            forms = {
                'adminForm': RegisterAdminForm(),
                'alunoForm': AlunoForm(),
                'cursoForm': CursoForm(),
                'docenteForm': DocenteForm(),
                'dispositivoForm': DispositivoForm(),
            }
            
            context = {
                'total_alunos': total_alunos,
                'total_docentes': total_docentes,
                'total_visitantes': total_visitantes,
                'entradas_hoje': entradas_hoje,
                'forms': forms,
            }
            return render(request, self.template_name, context)
        if not User.objects.filter(is_staff=True).exists():
            return redirect('register_admin')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        forms = {
            'adminForm': RegisterAdminForm(),
            'alunoForm': AlunoForm(),
            'cursoForm': CursoForm(),
            'docenteForm': DocenteForm(),
            'dispositivoForm': DispositivoForm(),
        }

        form_name = request.POST.get('form_name')
        form_class = {
            'adminForm': RegisterAdminForm,
            'alunoForm': AlunoForm,
            'cursoForm': CursoForm,
            'docenteForm': DocenteForm,
            'dispositivoForm': DispositivoForm,
        }.get(form_name)

        if form_class:
            form = form_class(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '✅ Cadastro realizado com sucesso!')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'⛔ {field}: {error}')
            return redirect('index')

        hoje = now().date()
        total_alunos = Aluno.objects.count()
        total_docentes = Docente.objects.count()
        total_visitantes = Visitante.objects.count()
        entradas_hoje = Entrada.objects.filter(data_entrada__date=hoje).count()

        context = {
            'total_alunos': total_alunos,
            'total_docentes': total_docentes,
            'total_visitantes': total_visitantes,
            'entradas_hoje': entradas_hoje,
            'forms': forms,
        }
        return render(request, self.template_name, context)


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
                if hasattr(usuario, 'aluno') and usuario.aluno.situacao_matricula != 'Deferida':
                    return JsonResponse({'status': 'error', 'message': 'Matrícula não está ativa.'})
                
                # Registra a entrada
                entrada = Entrada.objects.create(id_usuario=usuario, dispositivo=dispositivo)
                entrada_data_local = obter_hora_local()
                logger.info(f"Entrada registrada com sucesso: {usuario.nome} às {entrada_data_local.strftime('%H:%M - %d/%m/%Y')} pelo {dispositivo}")
                return JsonResponse({'status': 'success', 'message': f"Entrada registrada com sucesso: {usuario.nome} às {entrada_data_local.strftime('%H:%M - %d/%m/%Y')} pelo {dispositivo}"})
            else:
                logger.error("Usuário não encontrado.")
                return JsonResponse({'status': 'error', 'message': 'Usuário não encontrado.'})
        else:
            logger.error("Erro ao validar formulário.")
            return JsonResponse({'status': 'error', 'message': 'Erro ao validar formulário.'})
    else:
        form = EntradaForm()

    return render(request, 'pages/validar_entrada.html', {'form': form})


def listar_entradas(request):
    hoje = timezone.now().date()
    entradas = Entrada.objects.select_related('id_usuario', 'dispositivo').all().order_by('-data_entrada')

    # Filtro por período
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    if data_inicial or data_final:
        data_inicio = datetime.strptime(data_inicial, "%Y-%m-%d") if data_inicial else hoje
        data_fim = datetime.strptime(data_final, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1) if data_final else data_inicio + timedelta(days=1) - timedelta(seconds=1)
        entradas = entradas.filter(data_entrada__range=(data_inicio, data_fim))
    else:
        # Filtro padrão: exibir apenas as entradas do dia atual
        entradas = entradas.filter(data_entrada__date=hoje)

    # Outros filtros
    nome = request.GET.get('nome')
    matricula = request.GET.get('matricula')
    dispositivo = request.GET.get('dispositivo')
    tipo_usuario = request.GET.get('tipo_usuario')

    if nome:
        entradas = entradas.filter(id_usuario__nome__icontains=nome)
    if matricula:
        entradas = entradas.filter(id_usuario__aluno__matricula__icontains=matricula)
    if dispositivo:
        entradas = entradas.filter(dispositivo__localizacao__icontains=dispositivo)
    if tipo_usuario:
        if tipo_usuario == 'estudante':
            entradas = entradas.filter(id_usuario__polymorphic_ctype__model='aluno')
        elif tipo_usuario == 'visitante':
            entradas = entradas.filter(id_usuario__polymorphic_ctype__model='visitante')

    paginator = Paginator(entradas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'pages/listar_entradas.html', context)


def exportar_entradas(request):
    today = localtime(now()).date()
    entradas = Entrada.objects.select_related('id_usuario', 'dispositivo').filter(data_entrada__date=today)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="entradas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Usuário', 'Matrícula', 'Dispositivo', 'Data'])

    for entrada in entradas:
        matricula = entrada.id_usuario.aluno.matricula if hasattr(entrada.id_usuario, 'aluno') else '---'
        writer.writerow([entrada.id_usuario.nome, matricula, entrada.dispositivo.localizacao, localtime(entrada.data_entrada).strftime('%d/%m/%Y %H:%M')])

    return response


def excluir_entrada(request, id_entrada):
    entrada = get_object_or_404(Entrada, pk=id_entrada)
    entrada.delete()
    return redirect('listar_entradas')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Username: {username}, Password: {password}")  # Debug
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect('index')
                else:
                    form.add_error(None, 'Acesso negado.')
            else:
                form.add_error(None, 'Username ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'pages/login.html', {'form': form})


def register_admin_view(request):
    if request.method == 'POST':
        form = RegisterAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterAdminForm()
    
    return render(request, 'pages/register_admin.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'pages/change_password.html', {'form': form})


def cadastrar_visitante(request):
    if request.method == 'POST':
        form = VisitanteForm(request.POST)
        if form.is_valid():
            visitante = form.save()
            dispositivo = Dispositivo.objects.first()
            entrada = Entrada.objects.create(id_usuario=visitante, dispositivo=dispositivo)
            entrada_data_local = obter_hora_local()
            logger.info(f"Entrada de visitante registrada com sucesso: {visitante.nome} às {entrada_data_local.strftime('%H:%M - %d/%m/%Y')} pelo {dispositivo}")
            return redirect('listar_entradas')
    else:
        form = VisitanteForm()
    
    return render(request, 'pages/cadastrar_visitante.html', {'form': form})
