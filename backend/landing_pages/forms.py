import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from usuarios.validators import (
    PADRA_REGEX_EMAIL,
    PADRA_REGEX_LETRAS,
    PADRA_REGEX_TELEFONE,
)

user_model = get_user_model()


def valida_valor(valor, mensagem_erro, padrao_regex):
    """
        Retorna o valor ou lança ValidationError se não dê match com o
        regex passado
    """
    regex = re.compile(padrao_regex, re.I)
    if not regex.match(valor):
        raise forms.ValidationError(mensagem_erro)
    return valor


class ContateNosForm(forms.Form):
    nome = forms.CharField(max_length=255)
    email = forms.EmailField()
    telefone = forms.CharField(max_length=15)
    mensagem = forms.CharField()

    def clean_nome(self):
        data = self.cleaned_data["nome"]
        return valida_valor(
            data, "O nome não pode conter números ou caracteres especais",
            PADRA_REGEX_LETRAS)

    def clean_email(self):
        data = self.cleaned_data["email"]
        return valida_valor(
            data, "Email inválido, por favor informa um email válido",
            PADRA_REGEX_EMAIL)

    def clean_telefone(self):
        data = self.cleaned_data["telefone"]
        return valida_valor(data, "Telefone inválido", PADRA_REGEX_TELEFONE)

    def send_email_admins(self):
        """
            Envia as informações do formulário de contate nos para
            os administradores.
        """
        cleaned_data = self.cleaned_data

        message = render_to_string("pages/email/contate_nos.txt",
                                   context=cleaned_data)

        html_message = render_to_string("pages/email/contate_nos.html",
                                        context=cleaned_data)

        send_mail(
            subject=f"{cleaned_data['nome']} está compartilhar suas ideias",
            message=message,
            html_message=html_message,
            from_email=None,
            recipient_list=user_model.objects.filter(is_admin=True),
            fail_silently=False)
