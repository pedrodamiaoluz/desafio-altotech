from rest_framework.routers import SimpleRouter

from pedidos.api.views import PedidoViewSet

router = SimpleRouter()

router.register('', PedidoViewSet)

urlpatterns = router.urls
