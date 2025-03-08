
# Create your views here.
from django.utils import timezone
from rest_framework import generics, permissions, filters
from .models import Quiz
from .serializers import QuizSerializer
from .permissions import IsTeacher
from datetime import datetime

class TeacherQuizListView(generics.ListAPIView):
    """List all quizzes created by the logged-in teacher."""
    serializer_class = QuizSerializer
    permission_classes = [IsTeacher]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['due_date', 'title', 'created_at']
    ordering = ['due_date']

    def get_queryset(self):
        teacher = self.request.user
        queryset = Quiz.objects.filter(teacher=teacher)

        is_published_str = self.request.query_params.get('is_published')
        if is_published_str is not None:
            queryset = queryset.filter(is_published=is_published_str.lower() == 'true')

        due_date_str = self.request.query_params.get('due_date')
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(due_date__lte=due_date)
            except ValueError:
                return queryset.none()

        return queryset


class QuizCreateView(generics.CreateAPIView):
    """Allows teachers to create a quiz."""
    serializer_class = QuizSerializer
    permission_classes = [IsTeacher]

    def perform_create(self, serializer):
        if not serializer.validated_data.get('due_date'):
            serializer.validated_data['due_date'] = timezone.now() + timezone.timedelta(days=7)
        serializer.save(teacher=self.request.user)


class QuizUpdateView(generics.RetrieveUpdateAPIView):
    """Allows teachers to update their quizzes."""
    serializer_class = QuizSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return Quiz.objects.filter(teacher=self.request.user)


class QuizDeleteView(generics.DestroyAPIView):
    """Allows teachers to delete their quizzes."""
    serializer_class = QuizSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return Quiz.objects.filter(teacher=self.request.user)
