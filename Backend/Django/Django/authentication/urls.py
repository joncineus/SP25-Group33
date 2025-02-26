from django.urls import path
from .views import RegisterView
from .views import LoginView
from .views import QuizCreateView
from .views import QuizUpdateView
from authentication.views import TeacherQuizListView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('quizzes/', TeacherQuizListView.as_view(), name='teacher-quiz-list'),
    path('quizzes/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quizzes/<int:pk>/', QuizUpdateView.as_view(), name='quiz-update'),
]

