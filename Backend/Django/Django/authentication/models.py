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
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    def clean(self):
        if not self.title:
            raise ValidationError({"title": "Title cannot be blank."})
        if self.due_date and self.due_date < timezone.now():
            raise ValidationError({"due_date": "Due date cannot be in the past."})

    def __str__(self):
        return self.title

class QuizResponse(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_responses")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="responses")
    answers = models.JSONField()
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"

class Question(models.Model):
    QUESTION_TYPES = [
        ('MC', 'Multiple Choice'),
        ('WR', 'Written Answer'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPES,
        default='MC',
        verbose_name="Question Type"
    )
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_answer_mc = models.CharField(
        max_length=1,
        choices=[
            ('A', 'Option A'),
            ('B', 'Option B'),
            ('C', 'Option C'),
            ('D', 'Option D')
        ],
        blank=True,
        null=True
    )
    correct_answer_written = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"{self.question_text[:50]}... ({self.get_question_type_display()})"

    def clean(self):
        """Validate question based on its type"""
        super().clean()
        
        if self.question_type == 'MC':
            if not all([self.option_a, self.option_b, self.option_c, self.option_d]):
                raise ValidationError("All options (A-D) must be provided for multiple choice questions")
            if not self.correct_answer_mc:
                raise ValidationError("Correct answer must be specified for multiple choice questions")
        elif self.question_type == 'WR':
            if not self.correct_answer_written:
                raise ValidationError("Correct answer must be provided for written questions")

    def get_options(self):
        """Returns options based on question type"""
        if self.question_type == 'MC':
            return {
                'type': 'MC',
                'A': self.option_a,
                'B': self.option_b,
                'C': self.option_c,
                'D': self.option_d
            }
        return {
            'type': 'WR',
            'expected_length': len(self.correct_answer_written) if self.correct_answer_written else 0
        }