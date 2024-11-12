from django.contrib import admin
from .models import UserProfile, UserImage, Post, Message

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'birth_date', 'city')
    search_fields = ('user__username', 'last_name', 'first_name')
    list_filter = ('city',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserImage)
admin.site.register(Post)
admin.site.register(Message)