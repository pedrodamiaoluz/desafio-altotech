from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from produtos.api.serializers import (
    AdicionarItemCarrinhoSerializer,
    AtualizarItemCarrinhoSerializer,
    CarrinhoSerializer,
    CategoriaSerializer,
    ItemCarrinhoSerializer,
    ProdutoListRetrieveSerializer,
    ProdutoSerializer,
)
from produtos.models import Carrinho, Categoria, ItemCarrinho, Produto


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['categoria']
    search_fields = ['nome']

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ProdutoListRetrieveSerializer
        return ProdutoSerializer

    def get_permissions(self):
        permission_classes = []

        if self.action in ['list', 'retrieve']:
            permission_classes.append(IsAuthenticated)
        else:
            permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]


class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()

    def get_permissions(self):
        permission_classes = []

        if self.action in ['list', 'retrieve']:
            permission_classes.append(IsAuthenticated)
        else:
            permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]


class CarrinhoViewSet(viewsets.ModelViewSet):
    serializer_class = CarrinhoSerializer
    queryset = Carrinho.objects.all()

    http_method_names = ['get']

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ItemCarrinhoViewSet(viewsets.ModelViewSet):
    serializer_class = ItemCarrinhoSerializer
    queryset = ItemCarrinho.objects.all()

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdicionarItemCarrinhoSerializer
        if self.request.method == 'PATCH':
            return AtualizarItemCarrinhoSerializer
        return ItemCarrinhoSerializer

    def get_serializer_context(self):
        return {'carrinho_id': self.kwargs['carrinho_pk']}
