from django import forms
from .models import Dispositivo
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
