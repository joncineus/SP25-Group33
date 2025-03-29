from rest_framework.generics import CreateAPIView 
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Quiz
from .serializers import QuizSerializer, UserRegistrationSerializer, QuizResponseSerializer,  QuizCreateSerializer, QuizResponseListSerializer, PerformanceTrendSerializer
from .permissions import IsTeacher 
from .utils import get_tokens_for_user
from django.utils import timezone
from rest_framework import generics, permissions, filters 
from datetime import datetime 
from .models import QuizResponse
from rest_framework import serializers
from authentication.models import CustomUser
from django.db.models import Q






class TeacherQuizListView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsTeacher]

  
    def get_queryset(self):
        teacher = self.request.user
        queryset = Quiz.objects.filter(teacher=teacher)

        is_published_str = self.request.query_params.get('is_published')
        if is_published_str is not None:
            try:
                is_published = bool(is_published_str.lower() == 'true')
                queryset = queryset.filter(is_published=is_published)
            except ValueError:
                return Response({"error": "Invalid value for is_published"}, status=status.HTTP_400_BAD_REQUEST)

    
        due_date_str = self.request.query_params.get('due_date')
        if due_date_str is not None:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()  # Convert to date object
                queryset = queryset.filter(due_date__lte=due_date)
            except ValueError:
                return Response({"error": "Invalid date format for due_date. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        return queryset

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['due_date', 'title', 'created_at']
    ordering = ['due_date']


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):

    permission_classes = [AllowAny]  # This is crucial

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
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        
        return Response({
            "detail": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)


class QuizCreateView(generics.CreateAPIView):
    serializer_class = QuizCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if 'due_date' not in serializer.validated_data:
            serializer.validated_data['due_date'] = timezone.now() + timezone.timedelta(days=7)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        instance = self.get_object() 
        self.check_object_permissions(request, instance) 
        self.perform_destroy(instance) 
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class AvailableQuizzesListView(generics.ListAPIView):
    """
    API endpoint to list all published quizzes that are within their due date.
    Only authenticated users can access this endpoint.
    """
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(is_published=True, due_date__gt=timezone.now())


class QuizSubmitView(CreateAPIView):
    serializer_class = QuizResponseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        quiz_id = kwargs.get('quiz_id')
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            
            # Check for existing submission
            if QuizResponse.objects.filter(student=request.user, quiz=quiz).exists():
                return Response(
                    {"error": "You've already submitted this quiz"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify all questions are answered
            questions = quiz.questions.all()
            submitted_questions = set(request.data.get('answers', {}).keys())
            required_questions = {str(q.id) for q in questions}
            
            if submitted_questions != required_questions:
                return Response(
                    {"error": f"Please answer all {len(required_questions)} questions"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            request.data['quiz'] = quiz.id
            return super().create(request, *args, **kwargs)
            
        except Quiz.DoesNotExist:
            return Response(
                {"error": "Quiz not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class StudentQuizResultsView(generics.ListAPIView):
    serializer_class = QuizResponseListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuizResponse.objects.filter(student=self.request.user).order_by('-submitted_at')


class StudentPerformanceTrendView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get the logged-in student (user)
        student = request.user
        
        # Define the time range for the data (e.g., last month or all-time)
        period = self.request.query_params.get('period', 'all_time')  # Default to all_time
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30) if period == 'last_month' else None
        
        # Query the QuizResponse model for the logged-in student's scores
        queryset = QuizResponse.objects.filter(student=student)
        
        if start_date:
            queryset = queryset.filter(submitted_at__gte=start_date)
            
        # Get the data: ordered by the submission date
        performance_data = queryset.values('submitted_at', 'score').order_by('submitted_at')

        # Format the data into a list of dictionaries
        trend_data = [{"date": response['submitted_at'].date(), "score": response['score']} for response in performance_data]

        # Serialize the data using the PerformanceTrendSerializer
        serializer = PerformanceTrendSerializer(trend_data, many=True)

        # Return the serialized data as the response
        return Response(serializer.data)



class TeacherStudentQuizPerformanceView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request, quiz_id, last_name):
        try:
            # Ensure that the quiz exists
            quiz = Quiz.objects.get(id=quiz_id)

            # Check if the current user is the teacher of the quiz
            if quiz.teacher != request.user:
                return Response({
                    "detail": "You do not have permission to view this quiz's student's performance."
                }, status=status.HTTP_403_FORBIDDEN)

            # Get the student by their last name (you can also match first name if necessary)
            students = CustomUser.objects.filter(last_name=last_name)
            
            if students.count() != 1:
                # If no student or multiple students are found with that last name, handle the error
                return Response({"error": "Student not found or multiple students with the same last name"}, status=status.HTTP_404_NOT_FOUND)
            
            student = students.first()  # If there’s exactly one student with the last name
            
            # Get the quiz response for the specific student
            response = QuizResponse.objects.get(quiz=quiz, student=student)

            # Serialize the response (this will include the student's score and answers)
            serializer = QuizResponseSerializer(response)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:  # Handle CustomUser exception
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except QuizResponse.DoesNotExist:
            return Response({"error": "Student has not submitted a response for this quiz"}, status=status.HTTP_404_NOT_FOUND)