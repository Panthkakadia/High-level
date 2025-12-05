# api/admin.py

from django.contrib import admin
from .models import Student, Course, CompletedCourse, OngoingCourse

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department', 'semester']
    list_filter = ['department', 'semester']
    search_fields = ['name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department']
    list_filter = ['department']
    search_fields = ['name']

@admin.register(CompletedCourse)
class CompletedCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department', 'grade_achieved']
    list_filter = ['department', 'grade_achieved']

@admin.register(OngoingCourse)
class OngoingCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department', 'remaining_seats']
    list_filter = ['department']