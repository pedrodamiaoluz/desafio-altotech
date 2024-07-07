from django.contrib import admin

from .models import Pedido

# Register your models here.


class PedidoAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "user",
        'status',
        'data_criacao',
    )
    list_display_links = (
        "__str__",
    )
    list_per_page = 50
    list_filter = ("status", )

    search_fields = ('user', )
    ordering = ('data_criacao', 'user')

    readonly_fields = ("data_criacao",)

    fieldsets = (
        (None, {
            'fields': (
                'status',
                'data_criacao',
                'user',
            )
        }),
        ("endereco", {
            'fields': (
                ('rua', 'numero',),
                ('cidade', 'bairro',),
                ('complemento', 'estado', 'cep',)
            )
        }),
        ("carrinho", {
            'fields': (
                'carrinho',
            )
        }),
    )


admin.site.register(Pedido, PedidoAdmin)
