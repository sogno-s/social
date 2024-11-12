from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .models import UserProfile, Post, Message
from .serializers import UserProfileSerializer, PostSerializer, MessageSerializer, MyTokenObtainPairSerializer
from .forms import PostForm, MessageForm, RegistrationForm
from django.db.models import Q, Case, When, F, IntegerField, OuterRef, Subquery, Max

# Класс для работы с профилями пользователей через API
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()  # Получаем все профили пользователей
    serializer_class = UserProfileSerializer  # Используем сериализатор для преобразования данных

# Класс для работы с постами через API
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  # Получаем все посты
    serializer_class = PostSerializer  # Используем сериализатор для преобразования данных

# Класс для работы с сообщениями через API
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()  # Получаем все сообщения
    serializer_class = MessageSerializer  # Используем сериализатор для преобразования данных

# Представление для главной страницы с постами
def home_view(request):
    posts = Post.objects.all().order_by('-created_at')  # Получаем все посты, отсортированные по дате создания (сначала новые)
    paginator = Paginator(posts, 10)  # Показывать 10 постов на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-параметра
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы
    return render(request, 'socials/home.html', {'page_obj': page_obj})  # Рендерим шаблон с постами

# Представление для регистрации пользователя
def register_view(request):
    if request.method == 'POST':  # Если метод запроса POST
        form = RegistrationForm(request.POST, request.FILES)  # Создаем форму с данными из запроса
        if form.is_valid():  # Если форма валидна
            user = form.save(commit=False)  # Создаем пользователя, но не сохраняем в базу данных
            user.set_password(form.cleaned_data['password'])  # Устанавливаем пароль
            user.save()  # Сохраняем пользователя в базу данных
            # Создание профиля пользователя
            UserProfile.objects.create(
                user=user,
                birth_date=form.cleaned_data['birth_date'],
                city=form.cleaned_data['city'],
                avatar=form.cleaned_data['avatar']
            )
            username = form.cleaned_data.get('username')  # Получаем имя пользователя
            raw_password = form.cleaned_data.get('password')  # Получаем пароль
            user = authenticate(username=username, password=raw_password)  # Аутентифицируем пользователя
            login(request, user)  # Входим в систему
            return redirect('socials:profile')  # Перенаправляем на страницу профиля
    else:  # Если метод запроса GET
        form = RegistrationForm()  # Создаем пустую форму
    return render(request, 'socials/register.html', {'form': form})  # Рендерим шаблон с формой регистрации

# Представление для входа пользователя
def login_view(request):
    if request.method == 'POST':  # Если метод запроса POST
        username = request.POST['username']  # Получаем имя пользователя из POST-данных
        password = request.POST['password']  # Получаем пароль из POST-данных
        user = authenticate(request, username=username, password=password)  # Аутентифицируем пользователя
        if user is not None:  # Если пользователь найден
            login(request, user)  # Входим в систему
            return redirect('socials:profile')  # Перенаправляем на страницу профиля
        else:  # Если пользователь не найден
            return render(request, 'socials/login.html', {'error': 'Invalid credentials'})  # Рендерим шаблон с ошибкой
    return render(request, 'socials/login.html')  # Рендерим шаблон с формой входа

# Представление для выхода пользователя
@login_required  # Декоратор, требующий аутентификации
def logout_view(request):
    logout(request)  # Выходим из системы
    return redirect('socials:login')  # Перенаправляем на страницу входа

# Представление для получения токена JWT
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer  # Используем свой сериализатор для получения токена
    permission_classes = (AllowAny,)  # Разрешаем доступ всем пользователям

# Представление для профиля пользователя
@login_required  # Декоратор, требующий аутентификации
def profile_view(request):
    # Получаем профиль текущего пользователя
    profile = get_object_or_404(UserProfile, user=request.user)
    # Получаем посты пользователя
    posts = Post.objects.filter(author=profile)
    return render(request, 'socials/profile.html', {'profile': profile, 'posts': posts})  # Рендерим шаблон с профилем и постами

# Представление для создания поста
@login_required  # Декоратор, требующий аутентификации
def create_post(request):
    if request.method == 'POST':  # Если метод запроса POST
        form = PostForm(request.POST, request.FILES)  # Создаем форму с данными из запроса
        if form.is_valid():  # Если форма валидна
            post = form.save(commit=False)  # Создаем пост, но не сохраняем в базу данных
            post.author = request.user.userprofile  # Устанавливаем автора поста
            post.save()  # Сохраняем пост в базу данных
            return redirect('socials:profile')  # Перенаправляем на страницу профиля
    else:  # Если метод запроса GET
        form = PostForm()  # Создаем пустую форму
    return render(request, 'socials/create_post.html', {'form': form})  # Рендерим шаблон с формой создания поста

# Представление для поиска пользователей
@login_required  # Декоратор, требующий аутентификации
def search_users(request):
    query = request.GET.get('q')  # Получаем запрос из GET-параметра
    if query:  # Если запрос не пустой
        users = UserProfile.objects.filter(user__username__icontains=query)  # Ищем пользователей по имени
    else:  # Если запрос пустой
        users = UserProfile.objects.all()  # Получаем всех пользователей
    paginator = Paginator(users, 10)  # Показывать 10 пользователей на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-параметра
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы
    return render(request, 'socials/search_users.html', {'page_obj': page_obj})  # Рендерим шаблон с результатами поиска

# Представление для отправки сообщения
@login_required  # Декоратор, требующий аутентификации
def send_message(request, receiver_id):
    receiver = get_object_or_404(UserProfile, id=receiver_id)  # Получаем профиль получателя
    messages = Message.objects.filter(Q(sender=request.user.userprofile, receiver=receiver) | Q(sender=receiver, receiver=request.user.userprofile)).order_by('sent_at')  # Получаем все сообщения между пользователями
    # Отметить сообщения как прочитанные
    Message.objects.filter(sender=receiver, receiver=request.user.userprofile, is_read=False).update(is_read=True)
    if request.method == 'POST':  # Если метод запроса POST
        form = MessageForm(request.POST)  # Создаем форму с данными из запроса
        if form.is_valid():  # Если форма валидна
            message = form.save(commit=False)  # Создаем сообщение, но не сохраняем в базу данных
            message.sender = request.user.userprofile  # Устанавливаем отправителя сообщения
            message.receiver = receiver  # Устанавливаем получателя сообщения
            message.save()  # Сохраняем сообщение в базу данных
            return redirect('socials:send_message', receiver_id=receiver_id)  # Перенаправляем на страницу чата
    else:  # Если метод запроса GET
        form = MessageForm()  # Создаем пустую форму
    return render(request, 'socials/send_message.html', {'form': form, 'receiver': receiver, 'messages': messages})  # Рендерим шаблон с формой отправки сообщения и историей чата

from django.db.models import OuterRef, Subquery, Max

# Представление для списка чатов
@login_required  # Декоратор, требующий аутентификации
def chat_list(request):
    user_profile = request.user.userprofile  # Получаем профиль текущего пользователя
    # Получаем все сообщения, где пользователь является отправителем или получателем
    messages = Message.objects.filter(Q(sender=user_profile) | Q(receiver=user_profile))
    
    # Получаем последнее сообщение для каждого чата
    last_messages = messages.annotate(
        other_user_id=Case(
            When(sender=user_profile, then=F('receiver')),  # Если текущий пользователь - отправитель, то другой пользователь - получатель
            default=F('sender'),  # Иначе другой пользователь - отправитель
            output_field=IntegerField()  # Тип данных для другого пользователя
        )
    ).values('other_user_id').annotate(
        last_message_id=Max('id')  # Получаем максимальный id сообщения для каждого чата
    ).values('last_message_id')
    
    # Получаем полную информацию о последних сообщениях
    last_messages_info = Message.objects.filter(id__in=Subquery(last_messages)).order_by('-sent_at')
    
    chat_list = []
    for message in last_messages_info:
        other_user = message.sender if message.sender != user_profile else message.receiver  # Определяем другого пользователя в чате
        chat_list.append({
            'other_user': other_user,  # Профиль другого пользователя
            'last_message': message,  # Последнее сообщение в чате
        })
    
    return render(request, 'socials/chat_list.html', {'chat_list': chat_list})  # Рендерим шаблон со списком чатов