from django.urls import path
from .views import RegisterView
from .views import LoginView
from .views import QuizCreateView
from .views import QuizUpdateView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('quizzes/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quizzes/<int:pk>/', QuizUpdateView.as_view(), name='quiz-update'), 

]

