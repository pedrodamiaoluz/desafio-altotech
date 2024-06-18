from django.contrib import admin

from .models import Carrinho, ItemProduto

# Register your models here.

admin.site.register(Carrinho)
admin.site.register(ItemProduto)
