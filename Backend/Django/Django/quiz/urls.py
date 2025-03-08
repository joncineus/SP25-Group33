from django.urls import path  # ✅ Import path
from .views import TeacherQuizListView, QuizCreateView, QuizUpdateView, QuizDeleteView

urlpatterns = [
    path('quizzes/', TeacherQuizListView.as_view(), name='teacher-quizzes'),
    path('quizzes/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quizzes/<int:pk>/edit/', QuizUpdateView.as_view(), name='quiz-update'),
    path('quizzes/<int:pk>/delete/', QuizDeleteView.as_view(), name='quiz-delete'),
]
