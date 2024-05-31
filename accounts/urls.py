from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('api/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', views.profile, name='profile'),
    path('api/register/', views.register, name='register'),
    path('api/update-account/<str:uid>/', views.updateAccount, name='updateAccount'),
    path('api/get-user/', views.get_user, name='get-user')
]