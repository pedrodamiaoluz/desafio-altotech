from django import forms
import re
from .models import Pedido


class EnderecoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ('cep', 'estado', 'cidade', 'bairro', 'complemento', 'rua',
                  'numero')
