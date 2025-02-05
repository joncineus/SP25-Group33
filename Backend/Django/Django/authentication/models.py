from django.contrib.auth.models import AbstractUser
from django.db import models

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
