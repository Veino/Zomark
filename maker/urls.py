from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload'),
    path('', views.getRoutes, name='routes'),
    path('download/', views.download_image, name='download'),
]