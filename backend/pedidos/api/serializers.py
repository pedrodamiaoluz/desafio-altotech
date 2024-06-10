from rest_framework import serializers
from django.db import transaction
from produtos.models import Carrinho, ItemCarrinho

from ..models import Pedido, ItemPedido

from produtos.api.serializers.produto_serializer import ProdutoListRetrieveSerializer


class ItemPedidoSerializer(serializers.ModelSerializer):
    produto = ProdutoListRetrieveSerializer(many=False)

    class Meta:
        model = ItemPedido
        fields = ('id', 'produto', 'quantidade')


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ('id', 'user', 'itens', 'status', 'data_criacao')


class UpdatePedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ('status', )

    def validate_status(self, valor):
        return valor

    def validate(self, attrs):
        if self.instance.status in [
                Pedido.STATUS_PEDIDO_FINALIZADO, Pedido.STATUS_PEDIDO_CANCELADO
        ]:
            raise serializers.ValidationError(
                "Não pode alterar o status de pagamento pois o pedido já foi finalizado ou cancelado"
            )
        return attrs

    def save(self, **kwargs):
        status = self.context['status']
        self.instance.status = status
        self.instance.save()
        if status == Pedido.STATUS_PEDIDO_CANCELADO:
            itens_pedido = self.instance.itens.all()
            for item in itens_pedido:
                item.produto.estoque += item.quantidade
                item.produto.save()
        return self.instance


class CreatePedidoSerializer(serializers.ModelSerializer):
    carrinho_id = serializers.IntegerField()

    class Meta:
        model = Pedido
        fields = ('carrinho_id', )

    def validate_carrinho_id(self, valor):
        if not Carrinho.objects.filter(id=valor).exists():
            return serializers.ValidationError('Carrinho não existe')
        if not ItemCarrinho.objects.filter(carrinho_id=valor).exists():
            return serializers.ValidationError('Carrinho vazio')
        return valor

    def validate(self, attrs):
        carrinho_id = self.validated_data['carrinho_id']
        itens_carrinho = ItemCarrinho.objects.all(carrinho_id=carrinho_id)

        erros = []
        for item in itens_carrinho:
            if item.produto.estoque < item.quantiade:
                erros.append(item.produto.nome)
        if erros:
            raise serializers.ValidationError({'produtos indisponíveis': erros})

        return attrs

    def save(self, **kwargs):
        with transaction.atomic():
            carrinho_id = self.validated_data['carrinho_id']
            user_id = self.context['user_id']
            pedido = Pedido.objects.create(user_id=user_id)
            itens_carrinho = ItemCarrinho.objects.all(carrinho_id=carrinho_id)
            itens_pedido = [
                ItemPedido(pedido=pedido,
                           produto=item.produto,
                           quantidade=item.quantidade)
                for item in itens_carrinho
            ]
            ItemPedido.objects.bunk_create(itens_pedido)

            for item in itens_carrinho:
                item.produto.estoque -= item.quantidade
                item.produto.save()
                item.delete()

            return pedido
