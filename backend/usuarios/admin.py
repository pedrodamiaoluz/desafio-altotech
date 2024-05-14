from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

user_model = get_user_model()

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'nome_completo', 'email', 'cpf', 'telefone',
                    'data_nascimento', 'is_staff')
    list_display_links = ('email',)

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
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        (_('Importantes datas'), {
            'fields': ('date_joined', 'last_login', )
        }),
    )
    list_filter = ('is_staff',)

    search_fields = ("email", 'nome_completo', 'cpf', 'telefone')
    ordering = ('nome_completo',)
    filter_horizontal = (
        'groups',
        'user_permissions',
    )

    readonly_fields = ('date_joined', 'last_login')


admin.site.register(user_model, CustomUserAdmin)
