from django.contrib.auth import get_user_model
from django.db import models

from produtos.models import Produto

user_model = get_user_model()

# Create your models here.


class Pedido(models.Model):
    STATUS_PEDIDO_PENDENTE = 'P'
    STATUS_PEDIDO_CANCELADO = 'C'
    STATUS_PEDIDO_FINALIZADO = 'F'

    STATUS=(
        (STATUS_PEDIDO_PENDENTE, 'Pendente'),
        (STATUS_PEDIDO_CANCELADO, 'Cancelado'),
        (STATUS_PEDIDO_FINALIZADO, 'Finalizado'),
    )
    user = models.ForeignKey(user_model, on_delete=models.DO_NOTHING, related_name='pedidos') # PROTECT

    # total = models.FloatField()
    status = models.CharField(
        max_length=1,
        default=STATUS_PEDIDO_PENDENTE,
        choices=STATUS
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido N°{self.id}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"Item: {self.produto} pertence ao {self.pedido}"
