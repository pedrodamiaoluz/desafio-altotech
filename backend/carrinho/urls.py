from django.urls import path

from .views import CarrinhoView

app_name = 'carrinho'

urlpatterns = [
    path('', CarrinhoView.as_view(), name='carrinho'),
]
