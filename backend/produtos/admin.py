from django.contrib import admin

from produtos.models import Carrinho, Categoria, ItemCarrinho, Produto

admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)
