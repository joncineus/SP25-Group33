from rest_framework import serializers
from .models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source="teacher.username")

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "due_date", "is_published", "teacher"]
