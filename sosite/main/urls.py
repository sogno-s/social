from django.urls import path, include
from . import views

app_name = 'socials'

urlpatterns = [
    # Главная страница с постами
    path('', views.home_view, name='home'),
    # Страница регистрации пользователя
    path('register/', views.register_view, name='register'),
    # Страница входа пользователя
    path('login/', views.login_view, name='login'),
    # Страница выхода пользователя
    path('logout/', views.logout_view, name='logout'),
    # Страница профиля пользователя
    path('profile/', views.profile_view, name='profile'),
    # Страница создания поста
    path('create_post/', views.create_post, name='create_post'),
    # Страница поиска пользователей
    path('search_users/', views.search_users, name='search_users'),
    # Страница отправки сообщения
    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    # Страница списка чатов
    path('chats/', views.chat_list, name='chat_list'),
]