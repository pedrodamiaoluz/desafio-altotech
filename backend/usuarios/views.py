from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views import View
from django.http import Http404

from usuarios.forms import ChangePasswordSerializer, EnviarEmailResetSenhaForm, LoginForm, UserForm
from usuarios.utils import Util

# Create your views here.


class LoginView(View):
    template_name = 'usuarios/login.html'

    def post(self, request,  *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.usuario_ehAutenticado()
            if user:
                login(request, user)
                return redirect(reverse('produtos:home'))
            messages.error(request, 'Usuário não encontrado')
        return render(request, self.template_name, {'form': form})

    def get(self, request,  *args, **kwargs):
        return render(request, self.template_name, {'form': LoginForm()})


class CadastroView(View):
    template_name = 'usuarios/cadastro.html'

    def post(self, request,  *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('produtos:home'))
        return render(request, self.template_name, {'form': form})

    def get(self, request,  *args, **kwargs):
        return render(request, self.template_name, {'form': UserForm()})


class EsqueceuSenhaView(View):
    template_name = 'usuarios/esqueceu_senha.html'

    def post(self, request,  *args, **kwargs):
        form = EnviarEmailResetSenhaForm(request.POST)
        if form.is_valid():
            link = form.get_link_reset_password()
            Util.send_email_reset_password(form.user, link)
            messages.success(request, 'Email enviar acesse o link para redefinir sua senha')
            return redirect(reverse('usuarios:esqueceu_senha'))
        return render(request, self.template_name, {'form': form})

    def get(self, request,  *args, **kwargs):
        return render(request, self.template_name, {'form': EnviarEmailResetSenhaForm()})


class NovaSenhaView(View):
    template_name = 'usuarios/nova_senha.html'

    def get(self, request, uid, token, *args, **kwargs):
        if not Util.eh_valido_uid_token(uid, token):
            raise Http404("Acesso Negado")
        context =  {
            'form': ChangePasswordSerializer(),
            'uid': uid,
            'token': token
        }
        return render(request, self.template_name, context)

    def post(self, request, uid, token, *args, **kwargs):
        form = ChangePasswordSerializer(request.POST)
        if form.is_valid():
            user = Util.get_user(uid)
            if not user:
                raise Http404("Acesso Negado")
            user.set_password(form.data['senha'])
            user.save()
            return redirect(reverse('usuarios:login'))
        context =  {
            'form': form,
            'uid': uid,
            'token': token
        }
        return render(request, self.template_name, context)
