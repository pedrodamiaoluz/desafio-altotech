import re
from django import forms
from django.contrib.auth import authenticate, get_user_model

from usuarios.utils import Util
from usuarios.validators import PADRA_REGEX_CPF

user_model = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': "E-mail"}))
    senha = forms.CharField(max_length=255,
                            widget=forms.TextInput(attrs={
                                'type': "password",
                                'placeholder': "Senha"
                            }))

    def usuario_ehAutenticado(self):
        email = self.cleaned_data['email']
        senha = self.cleaned_data['senha']
        user = authenticate(email=email, password=senha)
        return user


class UserForm(forms.ModelForm):
    senha = forms.CharField(max_length=255, min_length=8,
                            widget=forms.TextInput(attrs={
                                'type': "password",
                                'placeholder': "Senha",
                            }))

    class Meta:
        model = user_model
        fields = ("nome_completo", 'cpf', 'data_nascimento', 'telefone',
                  'email', 'senha')
        widgets = {
            'nome_completo': forms.TextInput(attrs={'placeholder': "Informe seu nome completo"}),
            'cpf': forms.TextInput(attrs={'placeholder': "000.000.000-00"}),
            'telefone': forms.TextInput(attrs={'placeholder': "(DDD) 00000-0000"}),
            'data_nascimento': forms.DateInput(attrs={'placeholder': "Informe sua data de nascimento"}),
            'email': forms.EmailInput(attrs={'placeholder': "Exemplo@exemplo.com"}),
        }

    def save(self, **kwargs):
        password = self.cleaned_data.pop('senha')
        user = user_model.objects.create_user(
            password=password, **self.cleaned_data)
        return user


class EnviarEmailResetSenhaForm(forms.Form):
    email_ou_cpf = forms.CharField(max_length=255, label="E-mail ou cpf",
                                   widget=forms.TextInput(attrs={
                                       'placeholder': "E-mail ou cpf",
                                   }))

    class Meta:
        fields = ('email_ou_cpf', )

    def clean_email_ou_cpf(self):
        email_ou_cpf = self.cleaned_data['email_ou_cpf']
        return email_ou_cpf

    def clean(self):
        cleaned_data = super().clean()
        email_ou_cpf = cleaned_data['email_ou_cpf']
        regex_cpf = re.compile(PADRA_REGEX_CPF)

        if '@' not in email_ou_cpf and not regex_cpf.match(email_ou_cpf):
            raise forms.ValidationError("credencial inválida")

        self.user = None

        if user_model.objects.filter(email=email_ou_cpf).exists():
            self.user = user_model.objects.get(email=email_ou_cpf)

        elif user_model.objects.filter(cpf=email_ou_cpf).exists():
            self.user = user_model.objects.get(cpf=email_ou_cpf)

        if self.user is None:
            raise forms.ValidationError('Usuário não registrado no sistema')

        return cleaned_data

    def get_link_reset_password(self):
        return Util.get_link_reset_senha(self.user)


class ChangePasswordSerializer(forms.Form):
    senha = forms.CharField(
        min_length=8,
        max_length=255, label="Informe a nova senha",
        widget=forms.TextInput(attrs={
            'type': "password",
            'placeholder': "Nova senha",
        })
    )

    senha2 = forms.CharField(
        min_length=8,
        max_length=255, label="Confirme a nova senha",
        widget=forms.TextInput(attrs={
            'type': "password",
            'placeholder': "Confirme a nova senha",
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data['senha']
        senha2 = cleaned_data['senha2']

        if senha != senha2:
            self.add_error(None, 'Senha e confirmar senha devem ser iguais')

        return cleaned_data
