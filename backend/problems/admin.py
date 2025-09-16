from django.contrib import admin
from .models import Problem, UserProblem


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    """Admin for Problem model."""
    list_display = ['id', 'title', 'difficulty', 'created_at']
    list_filter = ['difficulty', 'created_at']
    search_fields = ['title', 'tags']
    ordering = ['id']


@admin.register(UserProblem)
class UserProblemAdmin(admin.ModelAdmin):
    """Admin for UserProblem model."""
    list_display = ['user', 'problem', 'confidence', 'next_due', 'attempts_count']
    list_filter = ['confidence', 'next_due', 'problem__difficulty']
    search_fields = ['user__email', 'problem__title']
    ordering = ['next_due']
