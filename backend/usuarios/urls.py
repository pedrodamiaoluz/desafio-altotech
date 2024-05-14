from django.urls import path
from rest_framework import routers

from usuarios.api.views import UserViewSet, LoginAPIView, LogoutAPIView

route = routers.SimpleRouter()

route.register(r'', UserViewSet)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]

urlpatterns += route.urls
