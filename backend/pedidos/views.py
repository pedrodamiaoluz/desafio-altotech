from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from carrinho.models import Carrinho
from django.contrib import messages
# Create your views here.

from usuarios.forms import UserEnderecoForm
from .models import Pedido


# def pedido_detalhe(request):
#     return render(request, 'pedidos/pedido_detalhe.html')
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

        if not carrinho.itens.exists:
            messages.warning(request, "Não a produtos no seu carrinho, adicione primeiro")
            return redirect(reverse("produtos:home"))

        for item in carrinho.itens.all():
            item.produto.estoque -= item.quantidade
            if item.produto.estoque < 0:
                return redirect(reverse("carrinho:carrinho"))

        for item in carrinho.itens.all():
            item.produto.save()
        
        carrinho.ativado = False
        carrinho.save()

        pedido = Pedido.objects.create(user=user, carrinho=carrinho)

        return redirect(pedido.get_absolute_url())


@method_decorator(decorator=login_required, name="dispatch")
class IdentificacaoView(View):
    template_name = "pedidos/identificacao.html"
    form_class = UserEnderecoForm
    success_url = 'pedidos:pagamento'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class(instance=request.user)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse(self.success_url))

        return render(request, self.template_name, {'form': form})
