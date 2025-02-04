from django.db import migrations, models
from polymorphic.models import PolymorphicModel
from django.core.exceptions import ValidationError
from validate_docbr import CPF


def create_default_dispositivo(apps, schema_editor):
    Dispositivo = apps.get_model('pages', 'Dispositivo')
    default_dispositivo = Dispositivo.objects.create(tipo_dispositivo='Padrão', localizacao='Desconhecida')
    Entrada = apps.get_model('pages', 'Entrada')
    for entrada in Entrada.objects.all():
        entrada.dispositivo = default_dispositivo
        entrada.save()

class Migration(migrations.Migration):

    dependencies = [
        ('pages', 'previous_migration_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='dispositivo',
            field=models.ForeignKey(default=1, to='pages.Dispositivo', on_delete=models.CASCADE),
            preserve_default=False,
        ),
        migrations.RunPython(create_default_dispositivo),
    ]

# Classe Pai Usuários
class Usuario(PolymorphicModel):
    nome = models.CharField(blank=False, null=False, max_length=200)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(blank=False, null=False, unique=True, max_length=120)
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

    def clean(self):
        cpf_validator = CPF()
        if not cpf_validator.validate(str(self.cpf)):
            raise ValidationError({'cpf': 'CPF inválido'})

    def __str__(self):
        return f'{self.nome}'
    

class Curso(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    turno = models.CharField(
        max_length=20,
        choices=[
            ('manha', 'Manhã'),
            ('tarde', 'Tarde'),
            ('noite', 'Noite'),
        ]
    )

    def __str__(self):
        return f'{self.nome} ({self.turno})'


# Classe Filha Aluno, herda as prpoiedades de usuario e acrescenta 2 novas
class Aluno(Usuario):
    matricula = models.CharField(blank=False, null=False, unique=True, max_length=15)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    SITUACAO_CHOICES = [
        ('Deferida', 'Deferida'),
        ('Indeferida', 'Indeferida'),
    ]
    situacao_matricula = models.CharField(
        max_length=10,
        choices=SITUACAO_CHOICES,
        default='Deferida'
    )

    def clean(self):
        super().clean()
        if len(self.matricula) != 15:
            raise ValidationError({'matricula': 'Matrícula deve ter exatamente 15 dígitos.'})

    def __str__(self):
        return f'{self.nome} - {self.curso.nome}'
    
    def save(self, *args, **kwargs):
        curso_nome = self.curso.nome
        curso_turno = self.curso.turno

        curso, created = Curso.objects.get_or_create(nome=curso_nome, turno=curso_turno)
        self.curso = curso

        super().save(*args, **kwargs)


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
        return f'{self.localizacao}'


# Classe que irá validar a entrada das pessoas ao entrar
class Entrada(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_entrada = models.DateTimeField(auto_now_add=True)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.id_usuario} - {self.data_entrada} - {self.dispositivo}'

