from django import forms
import re
from .models import Pedido

from django.core.validators import RegexValidator


class EnderecoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ('cep', 'estado', 'cidade', 'bairro', 'complemento', 'rua',
                  'numero')

