from django.urls import path
from .views import PaginaInicial, listar_entradas, validar_entrada


# Aqui criaremos as url, juntando o endereço dela, a View para renderizar e o nome da URL
urlpatterns = [
    path('', PaginaInicial.as_view(), name='index'),
    path('validar-entrada/', validar_entrada, name='validar_entrada'),
    path('listar-entradas/', listar_entradas, name='listar_entradas'),
]