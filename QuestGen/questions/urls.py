from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('api/topics/<int:course_id>/', views.TopicsByCourseView.as_view(), name='topics_by_course'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('quiz/start/<int:topic_id>/', views.QuizStartView.as_view(), name='quiz_start'),
    path('quiz/question/', views.QuizQuestionView.as_view(), name='quiz_question'),
    path('quiz/results/', views.QuizResultsView.as_view(), name='quiz_results'),
]
