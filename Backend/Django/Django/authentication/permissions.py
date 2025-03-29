from rest_framework import permissions
from .models import Quiz

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to allow only teachers to create quizzes.
    """

    def has_permission(self, request, view):
        quiz_id = view.kwargs.get('quiz_id')
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            return quiz.teacher == request.user
        except Quiz.DoesNotExist:
            return False
