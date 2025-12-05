# api/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Student, OngoingCourse, CompletedCourse
from .serializers import (
    StudentSerializer,
    StudentBasicSerializer,
    OngoingCourseSerializer,
    CompletedCourseSerializer
)


@api_view(['GET'])
def get_routes(request):
    """Return all available API routes"""
    routes = [
        {
            'Endpoint': '/api/',
            'method': 'GET',
            'description': 'Returns all available routes'
        },
        {
            'Endpoint': '/api/students/',
            'method': 'GET',
            'description': 'Returns all students'
        },
        {
            'Endpoint': '/api/ongoing-courses/',
            'method': 'GET',
            'description': 'Returns all ongoing courses'
        },
        {
            'Endpoint': '/api/student-details/',
            'method': 'POST',
            'body': {'student_id': 'id'},
            'description': 'Returns student details'
        },
        {
            'Endpoint': '/api/student-average/',
            'method': 'POST',
            'body': {'student_id': 'id'},
            'description': 'Returns student average grade'
        },
        {
            'Endpoint': '/api/student-ongoing-courses/',
            'method': 'POST',
            'body': {'student_id': 'id'},
            'description': 'Returns student ongoing courses'
        },
        {
            'Endpoint': '/api/student-completed-courses/',
            'method': 'POST',
            'body': {'student_id': 'id'},
            'description': 'Returns student completed courses'
        },
        {
            'Endpoint': '/api/course-grade/',
            'method': 'POST',
            'body': {'student_id': 'id', 'course_name': 'name'},
            'description': 'Returns grade for a specific completed course'
        },
    ]
    return Response(routes)


@api_view(['GET'])
def get_students(request):
    """Get all students"""
    students = Student.objects.all()
    serializer = StudentBasicSerializer(students, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_ongoing_courses(request):
    """Get all ongoing courses"""
    courses = OngoingCourse.objects.all()
    serializer = OngoingCourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def get_student_details(request):
    """Get detailed information about a specific student"""
    student_id = request.data.get('student_id')

    if not student_id:
        return Response(
            {'error': 'student_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        student = Student.objects.get(id=student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def get_student_average(request):
    """Get student's average grade"""
    student_id = request.data.get('student_id')

    if not student_id:
        return Response(
            {'error': 'student_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        student = Student.objects.get(id=student_id)
        average = student.calculate_average_grade()
        return Response({
            'student_id': student_id,
            'student_name': student.name,
            'average_grade': average
        })
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def get_student_ongoing_courses(request):
    """Get student's ongoing courses"""
    student_id = request.data.get('student_id')

    if not student_id:
        return Response(
            {'error': 'student_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        student = Student.objects.get(id=student_id)
        courses = student.courses_enrolled.all()
        serializer = OngoingCourseSerializer(courses, many=True)
        return Response({
            'student_id': student_id,
            'student_name': student.name,
            'ongoing_courses': serializer.data
        })
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def get_student_completed_courses(request):
    """Get student's completed courses"""
    student_id = request.data.get('student_id')

    if not student_id:
        return Response(
            {'error': 'student_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        student = Student.objects.get(id=student_id)
        courses = student.courses_completed.all()
        serializer = CompletedCourseSerializer(courses, many=True)
        return Response({
            'student_id': student_id,
            'student_name': student.name,
            'completed_courses': serializer.data
        })
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def get_course_grade(request):
    """Get grade for a specific completed course"""
    student_id = request.data.get('student_id')
    course_name = request.data.get('course_name')

    if not student_id or not course_name:
        return Response(
            {'error': 'Both student_id and course_name are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        student = Student.objects.get(id=student_id)
        course = student.courses_completed.filter(name__icontains=course_name).first()

        if not course:
            return Response(
                {'error': f'Course "{course_name}" not found in completed courses'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            'student_id': student_id,
            'student_name': student.name,
            'course_name': course.name,
            'grade': course.grade_achieved,
            'grade_points': course.get_grade_points()
        })
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )