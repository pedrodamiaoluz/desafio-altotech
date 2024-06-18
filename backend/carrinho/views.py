from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import render

from .models import Carrinho

# Create your views here.


class CarrinhoView(LoginRequiredMixin, View):
    template_name = 'carrinho/carrinho.html'

    login_url = "usuarios:login"


    def get(self, request, *args, **kwargs):
        carrinho = Carrinho.objects.get_or_create(request.user)
        self.carrinho = carrinho
        return render(request, self.template_name, {'carrinho': carrinho})
  