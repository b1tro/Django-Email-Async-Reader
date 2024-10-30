from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('message/<str:service>/<int:uid>/', views.detail, name='detail'),
    path('download/<str:service>/<int:message>/<int:file_id>/', views.downoald, name='download'),
]