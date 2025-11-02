from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProgress


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('role', 'phone', 'date_of_birth', 'profile_picture', 
                      'bio', 'current_education', 'current_job', 'skills', 'interests')
        }),
        ('Learning Statistics', {
            'fields': ('total_quizzes_taken', 'total_notes_generated', 'current_level')
        }),
    )
    list_display = ('email', 'username', 'role', 'current_level', 'is_staff')
    list_filter = ('role', 'current_level', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_study_time')
    list_filter = ('user',)
    search_fields = ('user__email', 'user__username')
    readonly_fields = ()
