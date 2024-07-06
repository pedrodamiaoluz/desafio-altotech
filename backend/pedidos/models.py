from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator
from carrinho.models import Carrinho

from .validators import REGEX_ENDERECO, REGEX_NUMERO_ENDERECO, REGEX_CEP

user_model = get_user_model()

# Create your models here.


class Pedido(models.Model):
    STATUS_PEDIDO_PENDENTE = 'P'
    STATUS_PEDIDO_CANCELADO = 'C'
    STATUS_PEDIDO_FINALIZADO = 'F'

    STATUS = (
        (STATUS_PEDIDO_PENDENTE, 'Pendente'),
        (STATUS_PEDIDO_CANCELADO, 'Cancelado'),
        (STATUS_PEDIDO_FINALIZADO, 'Finalizado'),
    )
    user = models.ForeignKey(user_model, on_delete=models.DO_NOTHING,
                             related_name='pedidos', null=True)
    carrinho = models.OneToOneField(
        Carrinho, on_delete=models.DO_NOTHING, null=True)

    status = models.CharField(
        max_length=1,
        default=STATUS_PEDIDO_PENDENTE,
        choices=STATUS
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    ESTADO_CHOICES = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    )

    cep = models.CharField(max_length=8, default='', validators=[
                           REGEX_CEP, MinLengthValidator(8)])
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, default='')
    cidade = models.CharField(
        max_length=50, default='', validators=[REGEX_ENDERECO])
    bairro = models.CharField(
        max_length=50, default='', validators=[REGEX_ENDERECO])
    complemento = models.CharField(
        max_length=20, default='', validators=[REGEX_ENDERECO])
    rua = models.CharField(max_length=50, default='',
                           validators=[REGEX_ENDERECO])
    numero = models.CharField(max_length=10, default='', validators=[
                              REGEX_NUMERO_ENDERECO])

    def __str__(self):
        """ Retorna a representação do objeto como uma string """
        return f'Pedido N°{self.id}'

    def get_absolute_url(self):
        """ Retorna a URL de detalhe para o pedido """
        return reverse("pedidos:pedido_detalhe", kwargs={"pk": self.pk})

    @property
    def total(self):
        """ Retorna o valor total do pedido """
        return sum([
            item.produto.preco * item.quantidade
            for item in self.carrinho.itens.all()
        ])

    @property
    def quantidade(self):
        """ Retorna a quantidade total de itens do pedido """
        return sum([item.quantidade for item in self.carrinho.itens.all()])
