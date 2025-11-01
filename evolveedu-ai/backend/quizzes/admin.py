from django.contrib import admin
from .models import QuizCategory, Quiz, Question, QuizAttempt, QuizResponse


@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quiz_count')
    search_fields = ('name',)
    
    def quiz_count(self, obj):
        return obj.quizzes.count()
    quiz_count.short_description = 'Total Quizzes'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'category', 'difficulty_level', 'times_taken', 'created_at')
    list_filter = ('difficulty_level', 'quiz_type', 'is_public', 'created_at')
    search_fields = ('title', 'created_by__email', 'description')
    readonly_fields = ('times_taken', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'description', 'category', 'created_by')}),
        ('Settings', {'fields': ('difficulty_level', 'quiz_type', 'time_limit_minutes', 'is_public')}),
        ('Content', {'fields': ('tags', 'passing_score_percentage')}),
        ('Statistics', {'fields': ('times_taken', 'average_score', 'created_at', 'updated_at')}),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'order', 'question_type', 'points')
    list_filter = ('quiz', 'question_type')
    search_fields = ('text', 'quiz__title')
    ordering = ('quiz', 'order')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'status', 'score_percentage', 'started_at')
    list_filter = ('status', 'started_at', 'completed_at')
    search_fields = ('user__email', 'quiz__title')
    readonly_fields = ('started_at', 'completed_at')


@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'is_correct', 'points_earned')
    list_filter = ('is_correct',)
    search_fields = ('attempt__user__email', 'question__text')
    readonly_fields = ('answered_at',)
