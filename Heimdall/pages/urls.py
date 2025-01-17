from django.urls import path
from .views import PaginaInicial
from . import views

# Aqui criaremos as url, juntando o endereço dela, a View para renderizar e o nome da URL
urlpatterns = [
    # path('endereço/', MinhaViewParaRenderizar.as_view(), name='nome da URL'),
    path('', views.registrar_entrada, name='resgitrar_entrada'),
]