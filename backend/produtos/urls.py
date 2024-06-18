from django.urls import path

from .views import CategoriaListView, CompraPorCategoriaListView, HomeView

app_name = "produtos"

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('compra-por-categoria/', CompraPorCategoriaListView.as_view(), name='compra_por_categoria'),
    path('categoria/<int:categoria_id>', CategoriaListView.as_view(), name='categoria'),
]
