from django.contrib.auth import get_user_model
from django.db import models

from .utils import redimencionar_imagem

user_model = get_user_model()


class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(max_length=255)
    preco = models.FloatField()
    imagem = models.ImageField(
        upload_to='produto_imagem/%Y/%m', null=True, blank=True)
    estoque = models.PositiveIntegerField(default=1)
    categoria = models.ManyToManyField(Categoria)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        nova_largura = 600

        if self.imagem:
            redimencionar_imagem(self.imagem, nova_largura)

    def __str__(self):
        return self.nome


class Carrinho(models.Model):
    proprietario = models.OneToOneField(user_model, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrinho do usuario: {self.proprietario.nome_completo}"


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(
        Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name='carrinho_itens')
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Item: {self.produto}, está no {self.carrinho}"
