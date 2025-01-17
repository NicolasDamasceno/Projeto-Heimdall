from django import forms

class EntradaForm(forms.Form):
    cpf_ou_matricula = forms.CharField(
        label='CPF ou Matrícula',
        max_length= 30,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu CPF ou Matrícula'})
    )