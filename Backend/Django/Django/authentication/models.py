from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    # Inherits fields like `username`, `password`, `first_name`, `last_name`, `email`, and others from AbstractUser.
    # `AbstractUser` also includes built-in password hashing and authentication methods.

    # Choices for role-based access (used to distinguish between teachers and students).
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    # Overriding the `email` field to make it unique and required.
    email = models.EmailField(unique=True, blank=False)  

    # Custom field to specify whether the user is a teacher or student.
    # This field will be used for role-based functionality in the platform.
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')  

    # String representation of the user (used for debugging, reccommended by gpt)
    def __str__(self):
        return f"{self.username} ({self.role})"


# Get the custom user model
User = get_user_model()

class Quiz(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)  # Title cannot be blank
    description = models.TextField(blank=True, null=True)  # Description is optional
    due_date = models.DateTimeField(blank=False, null=False)  # Due date cannot be blank
    is_published = models.BooleanField(default=False)  # Default to unpublished
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')  # Foreign key to the User model

    def clean(self):
        # Custom validation: Ensure title and due_date are not blank
        if not self.title:
            raise ValidationError({"title": "Title cannot be blank."})
        if not self.due_date:
            raise ValidationError({"due_date": "Due date cannot be blank."})
        if self.due_date < timezone.now():
            raise ValidationError({"due_date": "Due date cannot be in the past."})

    def __str__(self):
        return self.title  # String representation of the Quiz model