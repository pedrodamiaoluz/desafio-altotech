from rest_framework import serializers

from produtos.api.serializers.produto_serializer import ProdutoItemSerializer
from produtos.models import Carrinho, ItemCarrinho, Produto


class ItemCarrinhoSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField(method_name="total_item")
    produto = ProdutoItemSerializer(many=False)

    class Meta:
        model = ItemCarrinho
        fields = ('id', "carrinho", "produto", "quantidade", 'total')

    def total_item(self, itemCarrinho):
        return itemCarrinho.produto.preco * itemCarrinho.quantidade


class AdicionarItemCarrinhoSerializer(serializers.ModelSerializer):
    produto_id = serializers.IntegerField()

    class Meta:
        model = ItemCarrinho
        fields = ['id', 'produto_id', 'quantidade']

    def validate_produto_id(self, valor):
        if not Produto.objects.filter(id=valor).exists():
            raise serializers.ValidationError("Produto não encontarado")
        return valor

    def save(self, **kwargs):
        carrinho_id = self.context['carrinho_id']
        produto_id = self.validated_data['produto_id']
        quantidade = self.validated_data['quantidade']

        try:
            self.instance = ItemCarrinho.objects.get(carrinho_id=carrinho_id,
                                                     produto_id=produto_id)
            self.instance.quantidade += quantidade

        except ItemCarrinho.DoesNotExist:
            self.instance = ItemCarrinho(
                carrinho_id=carrinho_id, **self.validated_data)

        if self.instance.quantidade > self.instance.produto.estoque:
            raise serializers.ValidationError(
                f"O produto { self.instance.produto.nome} não tem essa quantidade disponivel")

        self.instance.save()
        return self.instance


class AtualizarItemCarrinhoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemCarrinho
        fields = ['quantidade']

    def save(self, **kwargs):
        quantidade = self.validated_data['quantidade']
        self.instance.quantidade = quantidade
        if self.instance.quantidade > self.instance.produto.estoque:
            raise serializers.ValidationError(
                f"O produto { self.instance.produto.nome} não tem essa quantidade disponivel")
        self.instance.save()
        return self.instance


class CarrinhoSerializer(serializers.ModelSerializer):
    itens = ItemCarrinhoSerializer(many=True, read_only=True)
    quantidade = serializers.SerializerMethodField(
        method_name='quantidade_total')
    total = serializers.SerializerMethodField(method_name='preco_total')

    class Meta:
        model = Carrinho
        fields = ('id', "itens",
                  'total',
                  'quantidade',
                  )

    def preco_total(self, carrinho):
        return sum([item.quantidade * item.produto.preco for item in carrinho.itens.all()])

    def quantidade_total(self, carrinho):
        return carrinho.itens.count()
