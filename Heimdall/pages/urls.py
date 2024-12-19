from django.urls import path
from .views import PaginaInicial

# Aqui criaremos as url, juntando o endereço dela, a View para renderizar e o nome da URL
urlpatterns = [
    # path('endereço/', MinhaViewParaRenderizar.as_view(), name='nome da URL'),
    path('', PaginaInicial.as_view(), name='inicio'),
]