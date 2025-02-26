from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser 
from .models import Quiz
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)  # Enables logging    

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        user = self.user
        data["role"] = user.role  # ✅ Ensure role is included in token
        
        print("✅ Generated JWT Data:", data)  # Debugging log to verify
        
        return data



    
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class QuizSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    teacher = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'created_at', 'teacher', 'subject',
            'difficulty_level', 'time_limit', 'is_published', 'questions'
        ]
        
    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
    

