from django.contrib import admin
from pages.models import Aluno, Docente, Visitante, Entrada, Dispositivo
# Register your models here.

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    search_fields = ('nome','cpf', 'matricula', 'email')
    list_display = ('nome', 'curso')


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    search_fields = ('nome', 'cpf', 'email')
    list_display = ('nome', 'departamento')


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    search_fields = ('nome', 'cpf', 'email')
    list_display = ('nome', 'motivo_visita')


@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    search_fields = ('tipo_dispositivo', 'localizacao')
    list_display = ('tipo_dispositivo', 'localizacao')


@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    search_fields = ('data_entrada',)
    list_display = ('data_entrada',)
