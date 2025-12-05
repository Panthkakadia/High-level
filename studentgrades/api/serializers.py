# api/serializers.py

from rest_framework import serializers
from .models import Student, Course, CompletedCourse, OngoingCourse


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'department', 'description']


class CompletedCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedCourse
        fields = ['id', 'name', 'department', 'description', 'grade_achieved']


class OngoingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OngoingCourse
        fields = ['id', 'name', 'department', 'description', 'remaining_seats']


class StudentSerializer(serializers.ModelSerializer):
    courses_enrolled = OngoingCourseSerializer(many=True, read_only=True)
    courses_completed = CompletedCourseSerializer(many=True, read_only=True)
    average_grade = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'department', 'semester',
                  'courses_enrolled', 'courses_completed', 'average_grade']

    def get_average_grade(self, obj):
        return obj.calculate_average_grade()


class StudentBasicSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""

    class Meta:
        model = Student
        fields = ['id', 'name', 'department', 'semester']