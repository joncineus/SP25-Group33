from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to allow only teachers to create, update, and delete quizzes.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"

    def has_object_permission(self, request, view, obj):
        return obj.teacher == request.user
