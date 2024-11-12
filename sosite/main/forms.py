from django import forms
from .models import Post, Message
from django.contrib.auth.models import User
from .models import UserProfile, CITIES

# Форма для регистрации пользователя
class RegistrationForm(forms.ModelForm):
    # Поле для пароля с виджетом PasswordInput
    password = forms.CharField(widget=forms.PasswordInput)
    # Поле для подтверждения пароля с виджетом PasswordInput
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    # Поле для даты рождения с виджетом DateInput
    birth_date = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))
    # Поле для выбора города из списка CITIES
    city = forms.ChoiceField(label='Город', choices=CITIES)
    # Поле для загрузки аватарки, необязательное
    avatar = forms.ImageField(label='Аватарка', required=False)

    class Meta:
        model = User  # Используем модель User для создания формы
        fields = ['username', 'email', 'password', 'password2', 'birth_date', 'city', 'avatar']  # Поля формы

    # Метод для проверки совпадения паролей
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

# Форма для создания поста
class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # Используем модель Post для создания формы
        fields = ['title', 'content', 'image']  # Поля формы

# Форма для отправки сообщения
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message  # Используем модель Message для создания формы
        fields = ['content']  # Поля формы