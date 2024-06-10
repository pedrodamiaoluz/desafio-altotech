from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/redoc/',
         SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),

    # Minhas urls
    path("api/usuarios/", include("usuarios.urls")),
    path("api/produtos/", include("produtos.urls")),
    path("api/pedidos/", include("pedidos.urls")),

    path("admin/", admin.site.urls),
]
