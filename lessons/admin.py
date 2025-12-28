from django.contrib import admin
from .models import Lesson, StudentProgress


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'student', 'instructor', 'vehicle_type', 'status']
    list_filter = ['status', 'vehicle_type', 'date']
    search_fields = ['student__full_name', 'instructor__full_name', 'location']
    date_hierarchy = 'date'


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'skill', 'progress']
    list_filter = ['skill']
    search_fields = ['student__full_name']

