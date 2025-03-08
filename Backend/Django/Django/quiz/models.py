from django.db import models  # ✅ Ensure this line is at the top
from django.contrib.auth import get_user_model
from authentication.models import CustomUser
class Quiz(models.Model):
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
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_quizzes')  # ✅ Changed related_name

    def clean(self):
        if not self.title:  
            raise ValidationError({"title": "Title cannot be blank."})

    def __str__(self):
        return self.title  
