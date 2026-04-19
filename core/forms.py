from django import forms
from .models import Corrida
from .models import Despesa

class CorridaForm(forms.ModelForm):
    class Meta:
        model = Corrida
        fields = ['plataforma', 'valor', 'data']

        widgets = {
            'data': forms.DateInput(attrs={
                'type': 'date'
            })
        }

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'data']

        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'data']

        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }