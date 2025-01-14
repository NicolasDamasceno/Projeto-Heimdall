from django.db import models
from polymorphic.models import PolymorphicModel

# Classe Pai Usuários
class Usuario(PolymorphicModel):
    nome = models.CharField(blank=False, null=False, max_length=200)
    cpf = models.BigIntegerField(blank=False, null=False)
    email = models.EmailField(blank=False, null=False, max_length=120)
    ALUNO = "AL"
    DOCENTE = "DC"
    VISITANTE = "VT"
    TIPO_DE_USUARIO_ESCOLHA = {
        ALUNO : "Aluno",
        DOCENTE : "Docente",
        VISITANTE : "Visitante",
    }
    tipo_usuario =models.CharField(
        max_length=2, 
        null=False, 
        blank=False,
        choices=TIPO_DE_USUARIO_ESCOLHA,
        default=ALUNO
    )
    def __str__(self):
        return f'{self.nome}'


# Classe Filha Aluno, herda as prpoiedades de usuario e acrescenta 2 novas
class Aluno(Usuario):
    matricula = models.CharField(blank=False,null=False, max_length=15)
    curso = models.CharField(blank=False, null=False, max_length=60)
    def __str__(self):
        return f'{self.nome} - {self.curso}'


# Classe Filha Docente
class Docente(Usuario):
    departamento = models.CharField(blank=False,null=False,max_length=40)
    def __str__(self):
        return f'{self.nome} - {self.departamento}'


# Classe Filha Visitante
class Visitante(Usuario):
    motivo_visita = models.CharField(blank=False,null=False, max_length=150)
    def __str__(self):
        return f'{self.nome} - {self.cpf}'


# Classe das cratracas que seram cadastradas no sistema
class Dispositivo(models.Model):
    localizacao = models.CharField(blank=False,null=False, max_length=15)
    COMPUTADOR = "PC"
    CATRACA = "CT"
    TIPO_DISPOSITIVO_ESCOLHA = {
        COMPUTADOR : "Computador",
        CATRACA : "Catraca",
    }
    tipo_dispositivo = models.CharField(
        max_length= 2,
        null=False,
        blank=False,
        choices=TIPO_DISPOSITIVO_ESCOLHA,
        default=CATRACA
    )
    def __str__(self):
        return f'{self.tipo_dispositivo}'


# Classe que irá validar a entrada das pessoas ao entrar
class Entrada(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_entrada = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.id_usuario} - {self.data_entrada}'

