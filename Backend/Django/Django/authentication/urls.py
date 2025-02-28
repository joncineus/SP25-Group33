from django.urls import path
from .views import RegisterView
from .views import LoginView
from .views import QuizCreateView
from .views import QuizUpdateView


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/quizzes/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('auth/quizzes/<int:pk>/', QuizUpdateView.as_view(), name='quiz-update'), 

]

