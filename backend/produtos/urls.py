from django.urls import path

from .views import index

app_name = "produtos"

urlpatterns = [
    path('home/', index, name='home')
]
