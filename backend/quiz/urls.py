from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuizListView.as_view(), name='quiz_list'),
    path('<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('submit/', views.SubmitQuizView.as_view(), name='quiz_submit'),
    path('history/', views.QuizHistoryView.as_view(), name='quiz_history'),
    path('recommended-difficulty/', views.RecommendedDifficultyView.as_view(), name='quiz_recommended'),
    path('leaderboard/', views.QuizLeaderboardView.as_view(), name='quiz_leaderboard'),
]
