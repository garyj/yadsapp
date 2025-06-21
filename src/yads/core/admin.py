from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (*UserAdmin.list_display, 'date_joined')
    list_filter = (*UserAdmin.list_filter, 'date_joined')
    ordering = ('-date_joined',)
