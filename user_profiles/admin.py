from django.contrib import admin
from user_profiles.models import UserProfile


@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    pass
