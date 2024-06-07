from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from produtos.api.views import (
    CarrinhoViewSet,
    CategoriaViewSet,
    ItemCarrinhoViewSet,
    ProdutoViewSet,
)

router = SimpleRouter()
router.register('produtos', ProdutoViewSet)
router.register('categorias', CategoriaViewSet)
router.register('carrinhos', CarrinhoViewSet)

router_carrinho = routers.NestedSimpleRouter(
    router, 'carrinhos', lookup='carrinho')
router_carrinho.register("itens", ItemCarrinhoViewSet,
                         basename='carrinho-itens')

urlpatterns = []

urlpatterns += router_carrinho.urls
urlpatterns += router.urls
