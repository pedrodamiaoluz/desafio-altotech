from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("usuarios/", include("usuarios.urls")),
    path("produtos/", include("produtos.urls")),
    path("carrinho/", include("carrinho.urls")),

    path("admin/", admin.site.urls),
]
