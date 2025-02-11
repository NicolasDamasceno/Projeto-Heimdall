from django.contrib import admin
from django.urls import path
from .views import PaginaInicial, listar_entradas, validar_entrada, login_view, register_admin_view, logout_view, change_password, exportar_entradas, excluir_entrada, cadastrar_visitante


# Aqui criaremos as url, juntando o endereço dela, a View para renderizar e o nome da URL
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PaginaInicial.as_view(), name='index'),
    path('validar-entrada/', validar_entrada, name='validar_entrada'),
    path('listar-entradas/', listar_entradas, name='listar_entradas'),
    path('login/', login_view, name='login'),
    path('register-admin/', register_admin_view, name='register_admin'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password, name='change_password'),
    path('exportar-csv/', exportar_entradas, name='exportar_csv'),
    path('excluir-entrada/<int:id_entrada>/', excluir_entrada, name='excluir_entrada'),
    path('cadastrar-visitante/', cadastrar_visitante, name='cadastrar_visitante'),
]