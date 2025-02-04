from django.test import TestCase
from pages.models import Aluno, Curso, Usuario

# Create your tests here.
class AlunoModelTest(TestCase):
    def setUp(self):
        curso = Curso.objects.create(nome="Engenharia", turno="manhã")
        Aluno.objects.create(nome="João", cpf="12345678901", email="joao@example.com", matricula="123456789012345", curso=curso)

    def test_aluno_creation(self):
        aluno = Aluno.objects.get(nome="João")
        self.assertEqual(aluno.nome, "João")
        self.assertEqual(aluno.cpf, "12345678901")
        self.assertEqual(aluno.email, "joao@example.com")
        self.assertEqual(aluno.matricula, "123456789012345")
        self.assertEqual(aluno.curso.nome, "Engenharia")    