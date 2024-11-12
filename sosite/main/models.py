from django.db import models
from django.contrib.auth.models import User

# Список городов России для выбора
CITIES = [
    ('Москва', 'Москва'),
    ('Санкт-Петербург', 'Санкт-Петербург'),
    ('Новосибирск', 'Новосибирск'),
    # Добавьте другие города по необходимости
]

# Модель профиля пользователя
class UserProfile(models.Model):
    # Связь с моделью User из Django для аутентификации
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Фамилия, имя, отчество пользователя
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)  # Отчество может быть не указано
    
    # Дата рождения
    birth_date = models.DateField()
    
    # Город проживания (выбор из списка)
    city = models.CharField(max_length=100, choices=CITIES)
    
    # Аватарка пользователя
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Дополнительные изображения пользователя
    additional_images = models.ManyToManyField('UserImage', blank=True)
    
    # Метод для отображения имени пользователя
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

# Модель изображения пользователя
class UserImage(models.Model):
    # Изображение пользователя
    image = models.ImageField(upload_to='user_images/')
    
    # Метод для отображения изображения
    def __str__(self):
        return self.image.name

# Модель поста
class Post(models.Model):
    # Связь с профилем пользователя, который создал пост
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    # Заголовок поста
    title = models.CharField(max_length=255)
    
    # Текст поста
    content = models.TextField()
    
    # Изображение поста
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    
    # Дата и время создания поста
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Метод для отображения поста
    def __str__(self):
        return f"Post by {self.author.user.username} at {self.created_at}"

# Модель сообщения
class Message(models.Model):
    # Отправитель сообщения
    sender = models.ForeignKey(UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    
    # Получатель сообщения
    receiver = models.ForeignKey(UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    
    # Текст сообщения
    content = models.TextField()
    
    # Дата и время отправки сообщения
    sent_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False) 
    
    # Метод для отображения сообщения
    def __str__(self):
        return f"Message from {self.sender.user.username} to {self.receiver.user.username} at {self.sent_at}"