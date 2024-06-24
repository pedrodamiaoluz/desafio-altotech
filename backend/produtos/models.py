from django.db import models
from django.urls import reverse

from .utils import redimencionar_imagem

# Create your models here.


class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True)

    imagem_principal = models.ImageField(
        upload_to='categoria_imagem_principal/%Y/%m',
        null=True,
        blank=True,
        help_text="Imagem que será exibida na home page")

    imagem_categorias = models.ImageField(
        upload_to='categoria_imagem_sub_categorias/%Y/%m',
        null=True,
        blank=True,
        help_text='Imagem que será exibida na página da categoria')

    descricao = models.TextField(default='')

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        nova_largura = 600

        if self.imagem_principal:
            redimencionar_imagem(self.imagem_principal, nova_largura)

        if self.imagem_categorias:
            redimencionar_imagem(self.imagem_categorias, nova_largura)

    def get_absolute_url(self):
        return reverse('produtos:categoria', args=[self.slug])


class SubCategoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True)
    destaque = models.BooleanField(
        default=False,
        help_text=
        'Destina a categoria que ficará em exibição na home page. obs: se mais de uma categoria for destinada para ser destaque, a categoria escolhida será feita por ordem alfabetica'
    )
    categoria = models.ForeignKey(Categoria,
                           on_delete=models.CASCADE,
                           related_name='sub_categorias')

    descricao = models.TextField(default='')

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('produtos:sub_categoria', args=[self.categoria.slug, self.slug])


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
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    estoque = models.PositiveIntegerField(default=1)
    categorias = models.ManyToManyField(SubCategoria, related_name='produtos')
    ingredientes = models.ManyToManyField(Ingrediente)
    imagem = models.ImageField(upload_to='produto_imagem/%Y/%m',
                               null=True,
                               blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        nova_largura = 600

        if self.imagem:
            redimencionar_imagem(self.imagem, nova_largura)

    def __str__(self):
        return self.nome
