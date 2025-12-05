# api/models.py

from django.db import models


class Course(models.Model):
    """Base course model with common attributes"""
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.department}"

    class Meta:
        ordering = ['name']


class CompletedCourse(Course):
    """Course that has been completed with a grade"""
    grade_achieved = models.CharField(max_length=2, choices=[
        ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
        ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
        ('D', 'D'), ('F', 'F')
    ])

    def get_grade_points(self):
        """Helper method to convert letter grade to points"""
        grade_map = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D': 1.0, 'F': 0.0
        }
        return grade_map.get(self.grade_achieved, 0.0)


class OngoingCourse(Course):
    """Course currently being taken"""
    remaining_seats = models.IntegerField(default=30)

    def is_full(self):
        """Check if course is full"""
        return self.remaining_seats <= 0


class Student(models.Model):
    """Student model with course relationships"""
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    courses_enrolled = models.ManyToManyField(OngoingCourse, blank=True, related_name='enrolled_students')
    courses_completed = models.ManyToManyField(CompletedCourse, blank=True, related_name='students_completed')

    def __str__(self):
        return f"{self.name} - {self.department}"

    def calculate_average_grade(self):
        """Calculate the student's GPA"""
        completed = self.courses_completed.all()
        if not completed:
            return 0.0

        total_points = sum(course.get_grade_points() for course in completed)
        return round(total_points / len(completed), 2)

    class Meta:
        ordering = ['name']
