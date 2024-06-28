from django.urls import path

from .views import contate_nos, sobre_nos

app_name = "landing_pages"

urlpatterns = [
    path('sobre-nos/', sobre_nos, name='sobre_nos'),
    path('contate-nos/', contate_nos, name='contate_nos'),
]
