from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from produtos.models import Produto

from .models import Carrinho, ItemProduto

# Create your views here.


class CarrinhoMixinView(View):
    """
        class mixin define alguns methods que seram herdados por outras views.
    """
    template_name = 'carrinho/carrinho.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            produto_id = request.POST.get("produto_id", None)
            self.produto = get_object_or_404(Produto, id=produto_id)

        self.carrinho = Carrinho.objects.get_or_create(request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_item_carrinho_or_404(
            self, carrinho: Carrinho = None, produto_id=None):
        """
            Tenta pegar o produto que está no carrinho ou lança um Http 404.
        """
        if carrinho and produto_id:
            return get_object_or_404(carrinho.itens.all(),
                                     produto_id=produto_id)
        return get_object_or_404(self.carrinho.itens.all(),
                                 produto_id=self.produto.id)

    def get_quantidade_ou_redirect(self):
        """
            retorna a quantidade e diz se deve redirecionar ou não dependendo
            se a quantidade for válida.
        """
        quantidade = self.request.POST.get("quantidade", None)
        redirecionar = True
        if quantidade is not None:
            try:
                quantidade = int(quantidade)
                if quantidade <= 0:
                    messages.warning(
                        self.request,
                        "A quantidade do produto deve ser maior que Zero")
                else:
                    redirecionar = False
            except ValueError:
                messages.error(
                    self.request,
                    "A quantidade do produto não é um número inteiro"
                )
        else:
            messages.warning(
                self.request, "Quantidade do produto não fornecida")

        return (redirecionar, quantidade)


class CarrinhoView(CarrinhoMixinView):

    def get(self, request, *args, **kwargs):
        itens_deletados = []
        itens_quantidade_alterada = []

        for item in self.carrinho.itens.all():
            # verifica se o produto ainda está disponível
            if item.produto.estoque == 0:
                itens_deletados.append(item.produto.name)
                item.delete()
            # verifica se a quantidade do item está acima do estoque do produto
            elif item.quantidade > item.produto.estoque:
                itens_quantidade_alterada.append(item.produto.name)
                item.quantidade = item.produto.estoque
                item.save()

        if itens_deletados:
            messages.warning(
                request,
                ("Alguns produtos do seu carrinho não estão mais disponíveis:"
                 f"{itens_deletados}")

            )
        if itens_quantidade_alterada:
            messages.warning(
                request,
                ("Alguns produtos do seu carrinho estavam com estoque "
                    "insuficiente então a quantidade desses produtos foram "
                    "ajustadas para a quantidade disponível: "
                    f"{itens_quantidade_alterada}"))

        return render(request, self.template_name, {'carrinho': self.carrinho})


class CarrinhoAtualizarProdutoView(CarrinhoMixinView):

    def post(self, request, *args, **kwargs):
        redirecionar, quantidade = self.get_quantidade_ou_redirect()
        if redirecionar:
            return redirect(request.META.get('HTTP_REFERER'))

        item = self.get_item_carrinho_or_404()
        item.quantidade = quantidade
        item.save()
        messages.success(request, "A quantidade do produto foi atualizada")
        return redirect(reverse('carrinho:carrinho'))


class CarrinhoAdicionarProdutoView(CarrinhoMixinView):

    def post(self, request, *args, **kwargs):
        redirecionar, quantidade = self.get_quantidade_ou_redirect()
        _redirect = redirect(request.META.get('HTTP_REFERER'))
        if redirecionar:
            return _redirect

        try:
            # pegar o item do carrinho em que o produto estive
            item = self.carrinho.itens.get(produto_id=self.produto.id)
            item_quantidade_anterior = item.quantidade
            item.quantidade += quantidade

            # verifica se o produto tem quantidade suficiente para ser
            # adicionado ao carrinho.
            if item.quantidade > item.produto.estoque:
                produto_estoque = item.produto.estoque
                quantidade_adicionada = (
                    produto_estoque - item_quantidade_anterior)

                # é adicionada a quantidade disponível do produto ao item
                item.quantidade = produto_estoque
                item.save()

                mensagem = (f"Há apenas {produto_estoque} unidades do produto,"
                            " Em seu carrinho já haviam "
                            f"{item_quantidade_anterior} unidades")
                if quantidade_adicionada != 0:
                    mensagem += (
                        f'apenas {quantidade_adicionada} foram adicionadas')
                mensagem += '.'

                messages.warning(request, mensagem)
                return _redirect

            item.save()
        except ItemProduto.DoesNotExist:
            # se não existir, cria um novo item
            item = ItemProduto.objects.create(carrinho=self.carrinho,
                                              produto=self.produto,
                                              quantidade=quantidade)

        messages.success(
            request, f"Adicionamos ao carrinho {self.produto}X{quantidade}")
        return _redirect


class CarrinhoRemoverProdutoView(CarrinhoMixinView):

    def post(self, request, *args, **kwargs):
        item = self.get_item_carrinho_or_404()
        item.delete()
        messages.success(
            request, f"Produto {self.produto} Removido do carrinho")
        return redirect(reverse('carrinho:carrinho'))
