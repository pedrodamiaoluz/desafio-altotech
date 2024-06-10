from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from pedidos.api.serializers import (
    CreatePedidoSerializer,
    PedidoSerializer,
    UpdatePedidoSerializer,
)
from pedidos.models import Pedido


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()

    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    ]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdatePedidoSerializer
        if self.request.method == 'POST':
            return CreatePedidoSerializer
        return PedidoSerializer

    def get_permissions(self):

        if self.request.method in ['DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
