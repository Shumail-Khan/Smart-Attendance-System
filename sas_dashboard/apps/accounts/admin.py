from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'can_manage_persons', 'can_manage_cameras')
    search_fields = ('user__username', 'role', 'department')
    list_filter = ('role', 'can_manage_persons', 'can_manage_cameras')
