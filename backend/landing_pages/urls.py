from django.urls import path

from .views import ContateNosView, sobre_nos

app_name = "landing_pages"

urlpatterns = [
    path('sobre-nos/', sobre_nos, name='sobre_nos'),
    path('contate-nos/', ContateNosView.as_view(), name='contate_nos'),
]
