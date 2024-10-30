from django.urls import path
from .consumers import WSEmailReader

ws_urlpatterns = [
    path('ws/email_reader/<str:email>/<str:service>', WSEmailReader.as_asgi())
]