from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, PostViewSet, MessageViewSet
from rest_framework_simplejwt.views import TokenRefreshView

# Создание роутера для API
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)  # Маршрут для профилей пользователей
router.register(r'posts', PostViewSet)  # Маршрут для постов
router.register(r'messages', MessageViewSet)  # Маршрут для сообщений

urlpatterns = [
    # Включение маршрутов API
    path('api/', include(router.urls)),
    # Маршрут для получения токена JWT
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Маршрут для обновления токена JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]