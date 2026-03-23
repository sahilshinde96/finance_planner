from django.contrib import admin
from .models import Quiz, Question, QuizAttempt

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'user_type', 'level', 'difficulty', 'is_active']
    list_filter = ['user_type', 'level', 'difficulty']
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'correct_option', 'difficulty_score']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total_questions', 'xp_earned', 'stars']
