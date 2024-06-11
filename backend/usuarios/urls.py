from django.urls import path

from .views import CadastroView, EsqueceuSenhaView, LoginView, NovaSenhaView

app_name='usuarios'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('esqueceu-senha/', EsqueceuSenhaView.as_view(), name='esqueceu_senha'),
    path('nova-senha/<str:uid>/<str:token>/', NovaSenhaView.as_view(), name='nova_senha'),
]
