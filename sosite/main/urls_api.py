from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, PostViewSet, MessageViewSet
from rest_framework_simplejwt.views import TokenRefreshView

# Создание роутера для API
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    # Включение маршрутов API
    path('api/', include(router.urls)),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]