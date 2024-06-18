from django.db import models
from django.urls import reverse

from produtos.managers import CategoriaManager

from .utils import redimencionar_imagem

# Create your models here.


class Categoria(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    principal = models.BooleanField(default=False, help_text='Define quais categorias iraão aparece na página home')
    imagem = models.ImageField(upload_to='categoria_imagem/%Y/%m', null=True, blank=True)

    objects = CategoriaManager()

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        nova_largura = 600

        if self.imagem:
            redimencionar_imagem(self.imagem, nova_largura)

    def get_absolute_url(self):
        return reverse('produtos:categoria', args=[self.id])


class Ingrediente(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome


class Marca(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(max_length=255)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    preco = models.DecimalField(max_digits=5,decimal_places=2)
    estoque = models.PositiveIntegerField(default=1)
    categorias = models.ManyToManyField(Categoria, related_name='produtos')
    ingredientes = models.ManyToManyField(Ingrediente)
    imagem = models.ImageField(upload_to='produto_imagem/%Y/%m', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        nova_largura = 600

        if self.imagem:
            redimencionar_imagem(self.imagem, nova_largura)

    def __str__(self):
        return self.nome

