# api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes, name='get_routes'),
    path('students/', views.get_students, name='get_students'),
    path('ongoing-courses/', views.get_ongoing_courses, name='get_ongoing_courses'),
    path('student-details/', views.get_student_details, name='student_details'),
    path('student-average/', views.get_student_average, name='student_average'),
    path('student-ongoing-courses/', views.get_student_ongoing_courses, name='student_ongoing_courses'),
    path('student-completed-courses/', views.get_student_completed_courses, name='student_completed_courses'),
    path('course-grade/', views.get_course_grade, name='course_grade'),
]