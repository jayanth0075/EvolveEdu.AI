from django.contrib import admin
from .models import Note, NoteCategory, NoteShare, StudySession


@admin.register(NoteCategory)
class NoteCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'is_public', 'views', 'created_at')
    list_filter = ('is_public', 'created_at', 'category')
    search_fields = ('title', 'content', 'user__email')
    readonly_fields = ('views', 'created_at', 'updated_at')
    fieldsets = (
        ('Content', {'fields': ('title', 'content', 'category', 'user')}),
        ('Settings', {'fields': ('is_public', 'tags')}),
        ('Statistics', {'fields': ('views', 'likes')}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(NoteShare)
class NoteShareAdmin(admin.ModelAdmin):
    list_display = ('note', 'shared_by', 'shared_with', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('note__title', 'shared_by__email', 'shared_with__email')
    readonly_fields = ('created_at',)


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'duration_minutes', 'start_time')
    list_filter = ('start_time',)
    search_fields = ('user__email', 'title')
    readonly_fields = ()
