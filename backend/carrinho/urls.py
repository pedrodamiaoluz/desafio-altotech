from django.urls import path

from .views import (
    CarrinhoAdicionarProdutoView,
    CarrinhoAtualizarProdutoView,
    CarrinhoRemoverProdutoView,
    CarrinhoView,
)

app_name = 'carrinho'

urlpatterns = [
    path('', CarrinhoView.as_view(), name='carrinho'),
    path('adicionar-produto',
         CarrinhoAdicionarProdutoView.as_view(),
         name='adicionar_produto'),
    path('atualizar-produto',
         CarrinhoAtualizarProdutoView.as_view(),
         name='atualizar_produto'),
    path('remover-produto',
         CarrinhoRemoverProdutoView.as_view(),
         name='remover_produto'),
]
