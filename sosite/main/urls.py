from django.urls import path, include
from . import views

app_name = 'socials'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('search_users/', views.search_users, name='search_users'),
    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('chats/', views.chat_list, name='chat_list'),
]


   