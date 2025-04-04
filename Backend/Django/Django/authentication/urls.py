from django.urls import path
from .views import RegisterView
from .views import LoginView
from .views import QuizCreateView, TeacherStudentQuizPerformanceView
from .views import QuizUpdateView, QuizDeleteView,  QuizSubmitView,  StudentQuizResultsView, StudentPerformanceTrendView
from authentication.views import TeacherQuizListView
from authentication.views import AvailableQuizzesListView, QuizPerformanceView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('quizzes/', TeacherQuizListView.as_view(), name='teacher-quiz-list'),
    path('quizzes/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quizzes/<int:pk>/', QuizUpdateView.as_view(), name='quiz-update'),
    path('quizzes/available/', AvailableQuizzesListView.as_view(), name='available-quizzes'),
    path('quizzes/<int:quiz_id>/submit/', QuizSubmitView.as_view(), name='quiz-submit'),
    path('students/me/quiz-results/', StudentQuizResultsView.as_view(), name='student-quiz-results'),
    path('students/me/performance/', StudentPerformanceTrendView.as_view(), name='student-performance-trend'),
    path('teachers/quizzes/<int:quiz_id>/students/<str:last_name>/', TeacherStudentQuizPerformanceView.as_view(), name='teacher_student_performance'),
    path('teachers/quizzes/<int:quiz_id>/performance/', QuizPerformanceView.as_view(), name='quiz-performance'), # Add this line




]

