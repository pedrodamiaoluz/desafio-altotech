from django.contrib.auth import get_user_model
from django.db import models

from carrinho.models import Carrinho
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
    user = models.ForeignKey(user_model, on_delete=models.DO_NOTHING, related_name='pedidos', null=True) # PROTECT
    carrinho = models.OneToOneField(Carrinho, on_delete=models.DO_NOTHING, null=True)

    # total = models.FloatField()
    status = models.CharField(
        max_length=1,
        default=STATUS_PEDIDO_PENDENTE,
        choices=STATUS
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido N°{self.id}'
