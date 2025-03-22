from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings


class CustomUser(AbstractUser):
    # Inherits fields like `username`, `password`, `first_name`, `last_name`, `email`, and others from AbstractUser.

    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    # Overriding the `email` field to make it unique and required.
    email = models.EmailField(unique=True, blank=False)  

    # Custom field to specify whether the user is a teacher or student.
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')  

    def __str__(self):
        return f"{self.username} ({self.role})"



class Quiz(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255, blank=False, null=False) 
    description = models.TextField(blank=True, null=True)  
    subject = models.CharField(max_length=100, blank=True, null=True) 
    difficulty_level = models.CharField(
        max_length=10,
        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
        default="medium"
    )
    time_limit = models.IntegerField(blank=True, null=True, help_text="Time limit in minutes")
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set timestamp
    due_date = models.DateTimeField()
    is_published = models.BooleanField(default=False) 

    def clean(self):
     if not self.title:  
        raise ValidationError({"title": "Title cannot be blank."})

    def __str__(self):
        return self.title  

class QuizResponse(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_responses")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="responses")
    answers = models.JSONField()  # Stores student's answers as a JSON object
    score = models.IntegerField(default=0)  # Calculated score, default 0
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp when submitted

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"
