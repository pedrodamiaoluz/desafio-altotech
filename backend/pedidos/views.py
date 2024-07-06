from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

# Create your views here.

from carrinho.models import Carrinho

from .models import Pedido
from .forms import EnderecoForm


@method_decorator(decorator=login_required, name="dispatch")
class PedidoDetailView(DetailView):
    template_name = 'pedidos/pedido_detalhe.html'
    model = Pedido


@method_decorator(decorator=login_required, name="dispatch")
class PagamentoView(View):
    template_name = "pedidos/pagamento.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # implmentar a lógica de pagamento

        user = request.user

        carrinho = Carrinho.objects.get_or_create(request.user)

        # verifica se tem produtos no carrinho
        if not carrinho.itens.exists():
            messages.warning(
                request, "Não a produtos no seu carrinho, adicione primeiro")
            return redirect(reverse("produtos:home"))

        endereco = request.session.get('endereco', None)
        # verifica se o endereço foi prenchido
        if not endereco:
            messages.warning(
                request, 'Não foi possível identificar o endereço, adicione primeiro')
            return redirect(reverse('pedidos:identificacao'))

        # diminui o estoque do produto e verifica se o estoque não é suficiente
        # para realizar o pedido
        for item in carrinho.itens.all():
            item.produto.estoque -= item.quantidade
            if item.produto.estoque < 0:
                return redirect(reverse("carrinho:carrinho"))

        try:
            # caso ocorra algum erro nesse bloco de código as alterções não
            # seram salvas no banco.
            with transaction.atomic():
                # salva as alterações no estoque dos produtos
                for item in carrinho.itens.all():
                    item.produto.save()

                # desativa o carrinho
                carrinho.ativado = False
                carrinho.save()

                # cria o pedido
                pedido = Pedido.objects.create(
                    user=user, carrinho=carrinho, **endereco)

                # limpa os campos de endereço
                del request.session['endereco']

                messages.success(request, 'Pedido realizado com sucesso')
                return redirect(pedido.get_absolute_url())
        except transaction.TransactionManagementError:
            messages.warning(
                request, 'Ouve um problema ao realizar seu pedido')
            return redirect(reverse('carrinho:carrinho'))


@method_decorator(decorator=login_required, name="dispatch")
class IdentificacaoView(View):
    template_name = "pedidos/identificacao.html"
    form_class = EnderecoForm
    success_url = 'pedidos:pagamento'

    def get(self, request, *args, **kwargs):
        if endereco := request.session.get('endereco', {}):
            form = self.form_class(initial=endereco)
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            # salva o endereço para ser utilizado na criação do pedido
            request.session['endereco'] = form.cleaned_data
            messages.success(request, 'Endereço salvo com sucesso')
            return redirect(reverse(self.success_url))

        return render(request, self.template_name, {'form': form})
