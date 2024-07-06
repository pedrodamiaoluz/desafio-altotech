from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from produtos.models import (
    Categoria,
    Ingrediente,
    Marca,
    Produto,
    SubCategoria
)

# Register your models here.


class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        'marca',
        'preco',
        'estoque',
    )
    list_display_links = (
        "nome",
        'marca',
    )
    list_per_page = 50
    list_filter = ("categorias", )

    search_fields = ('nome', )
    ordering = ('nome', 'preco', 'estoque')

    filter_horizontal = ('categorias', 'ingredientes')


class CategoriaAdmin(SummernoteModelAdmin):
    summernote_fields = ('descricao',)

    list_display = 'nome', 'slug'
    list_display_links = 'nome', 'slug'
    search_fields = ('nome',)
    ordering = ('nome',)
    list_per_page = 20
    prepopulated_fields = {
        'slug': ('nome', ),
    }


class SubCategoriaAdmin(SummernoteModelAdmin):
    summernote_fields = ('descricao',)

    list_display = 'nome', 'slug', 'destaque'
    list_display_links = 'nome', 'slug'
    list_filter = ('categoria',)
    search_fields = ('nome',)
    list_filter = ('destaque',)
    ordering = ('nome',)
    prepopulated_fields = {
        'slug': ('nome', ),
    }


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Marca)
admin.site.register(Ingrediente)
