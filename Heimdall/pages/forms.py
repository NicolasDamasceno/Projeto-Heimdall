from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Dispositivo, Visitante, Aluno, Curso, Docente
from validate_docbr import CPF


class EntradaForm(forms.Form):
    cpf_ou_matricula = forms.CharField(
        label='CPF ou Matrícula',
        max_length= 30,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu CPF ou Matrícula'})
    )
    dispositivo = forms.ModelChoiceField(
        queryset=Dispositivo.objects.all(),
        label='Localização'
    )

    def clean_cpf_ou_matricula(self):
        data = self.cleaned_data['cpf_ou_matricula']
        cpf_validator = CPF()
        if not cpf_validator.validate(data) and len(data) != 15:
            raise forms.ValidationError('CPF ou Matrícula inválidos.')
        return data


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)


class RegisterAdminForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('A senha é muito curta. Ela precisa conter pelo menos 8 caracteres.')
        if password.isdigit():
            raise ValidationError('A senha não pode ser composta apenas por números.')
        return password
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('As senhas não coincidem.')
        return password_confirm
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user
    

class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ['nome', 'cpf', 'motivo_visita']


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'email', 'matricula', 'curso', 'situacao_matricula']


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'turno']


class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ['nome', 'cpf', 'email', 'departamento']


class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = ['localizacao', 'tipo_dispositivo']
