from django.urls import path

from .views import (
    CategoriaListView,
    CompraPorCategoriaListView,
    HomeView,
    ProdutoListView,
    SubCategoriaListView,
)

app_name = "produtos"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('compra-por-categoria/',
         CompraPorCategoriaListView.as_view(),
         name='compra_por_categoria'),
    path('categoria/<str:categoria_slug>/',
         CategoriaListView.as_view(),
         name='categoria'),
    path('categoria/<str:categoria_slug>/<str:sub_categoria_slug>/',
         SubCategoriaListView.as_view(),
         name='sub_categoria'),
    path("produtos/", ProdutoListView.as_view(), name='produtos'),
]
