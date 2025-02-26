from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from .models import Quiz
from .serializers import QuizSerializer
from .permissions import IsTeacher 
from .utils import get_tokens_for_user
from django.utils import timezone
from rest_framework import generics, permissions, status



# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        # Extract username and password from request
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({
                "detail": "Username and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Use the function to generate tokens
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        
        # Return error if authentication fails
        return Response({
            "detail": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)


class QuizCreateView(generics.CreateAPIView):
    """
    API endpoint for teachers to create quizzes.
    """
    serializer_class = QuizSerializer
    permission_classes = [IsTeacher]

    def create(self, request, *args, **kwargs):
        print("Starting Quiz Create View") 
        print("Request Data:", request.data) 

        serializer = self.get_serializer(data=request.data)
        print("Serializer Data:", serializer.initial_data) 
        serializer.is_valid(raise_exception=True)

        print("Validated Data (before due_date check):", serializer.validated_data) #<--- Print statement 4

        if 'due_date' not in serializer.validated_data or not serializer.validated_data['due_date']:
            default_due_date = timezone.now() + timezone.timedelta(days=7)
            serializer.validated_data['due_date'] = default_due_date
            print("Due Date not provided, setting default:", default_due_date)
        
        print("Validated Data (after due_date check):", serializer.validated_data)

        serializer.validated_data['teacher'] = request.user
        print("Validated Data (after teacher set):", serializer.validated_data)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        print("Quiz Created Successfully")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        print("Performing Create (before save):", serializer.validated_data)
        serializer.save()
        print("Quiz Saved") 


class QuizUpdateView(generics.RetrieveUpdateDestroyAPIView):  
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsTeacher]

    def check_object_permissions(self, request, obj):
        """
        Override to ensure only the quiz creator can update.
        """
        if obj.teacher != request.user:
            self.permission_denied(request, message="You do not have permission to update this quiz.")
        return super().check_object_permissions(request, obj)

    def perform_update(self, serializer):
        serializer.save()

class QuizDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer  
    permission_classes = [IsTeacher]

    def check_object_permissions(self, request, obj):
        """
        Override to ensure only the quiz creator can delete.
        """
        if obj.teacher != request.user:
            self.permission_denied(request, message="You do not have permission to delete this quiz.")
        return super().check_object_permissions(request, obj)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # get the object
        self.check_object_permissions(request, instance) 
        self.perform_destroy(instance) # delete the object
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()