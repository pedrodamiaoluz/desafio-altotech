from django.urls import path

from .views import IdentificacaoView, PagamentoView, PedidoDetailView

app_name = 'pedidos'

urlpatterns = [
    path("pedido/<int:pk>/", PedidoDetailView.as_view(), name='pedido_detalhe'),
    path("identificacao/", IdentificacaoView.as_view(), name='identificacao'),
    path("pagamento/", PagamentoView.as_view(), name='pagamento'),
]
