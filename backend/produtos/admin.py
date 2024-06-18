from django.contrib import admin

from produtos.models import Categoria, Ingrediente, Marca, Produto

# Register your models here.


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", 'marca', 'preco', 'estoque',)
    list_display_links = ("nome", 'marca',)

    list_filter = ("categorias",)

    search_fields = ('nome', )
    ordering = ('nome', 'preco', 'estoque')

    filter_horizontal = ('categorias', )


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Ingrediente)
