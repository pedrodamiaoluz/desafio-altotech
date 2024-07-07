from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

user_model = get_user_model()

# Register your models here.


class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('informações pessoais'), {
            'fields': (
                'nome_completo',
                'cpf',
                'data_nascimento',
                'telefone',
            )
        }),
        (_('Permissões'), {
            'fields': (
                'is_active',
                'is_admin',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        (_('Datas importantes'), {
            'fields': ('date_joined', 'last_login', )
        }),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    'nome_completo',
                    "email",
                    'cpf',
                    'data_nascimento',
                    'telefone',
                    'cep',
                    'estado',
                    'cidade',
                    'bairro',
                    'complemento',
                    'rua',
                    'numero',
                    'is_admin',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                    "password1", "password2"
                ),
            },
        ),
    )

    list_display = ('id', 'nome_completo', 'email', 'cpf', 'telefone',
                    'data_nascimento', 'is_admin')
    list_display_links = ('email',)
    list_filter = ('is_admin',)

    search_fields = ("email", 'nome_completo', 'cpf', 'telefone')
    ordering = ('nome_completo',)
    filter_horizontal = (
        'groups',
        'user_permissions',
    )
    readonly_fields = ('date_joined', 'last_login')


admin.site.register(user_model, CustomUserAdmin)
