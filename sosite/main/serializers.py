from rest_framework import serializers
from .models import UserProfile, UserImage, Post, Message
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['id', 'image']

class UserProfileSerializer(serializers.ModelSerializer):
    # Дополнительные изображения пользователя
    additional_images = UserImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'last_name', 'first_name', 'middle_name', 'birth_date', 'city', 'avatar', 'additional_images']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'sent_at']