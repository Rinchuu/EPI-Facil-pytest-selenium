from django import forms
from .models import Acao


class AcaoForm(forms.ModelForm):
    class Meta:
        model = Acao
        fields = ['nome_equipamento', 'usuario', 'data_emprestimo', 'data_prevista_devolucao',
                  'status', 'condicoes_emprestimo', 'data_devolucao', 'observacoes_devolucao']
        widgets = {
            'nome_equipamento': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'data_emprestimo': forms.DateInput(attrs={'type': 'date'}),  # Para inputs de data
            'data_prevista_devolucao': forms.DateInput(attrs={'type': 'date'}),
            'data_devolucao': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'condicoes_emprestimo': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes_devolucao': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }