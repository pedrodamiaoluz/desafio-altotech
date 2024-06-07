from rest_framework import serializers

from produtos.models import Categoria, Produto


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = ('id', 'nome')


class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = 'id', 'nome', 'descricao', 'categoria', 'preco', 'estoque', 'imagem'


class ProdutoListRetrieveSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(many=True)

    class Meta:
        model = Produto
        fields = 'id', 'nome', 'descricao', 'categoria', 'preco', 'estoque', 'imagem'


class ProdutoItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'preco', 'imagem')
