from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to allow only teachers to create quizzes.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"
