from django.urls import path
from .views import StreakView, UserBadgesView, AllBadgesView, CheckInView, LeaderboardView

urlpatterns = [
    path('', StreakView.as_view(), name='streak'),
    path('badges/', UserBadgesView.as_view(), name='user_badges'),
    path('all-badges/', AllBadgesView.as_view(), name='all_badges'),
    path('checkin/', CheckInView.as_view(), name='checkin'),
    path('leaderboard/', LeaderboardView.as_view(), name='streak_leaderboard'),
]
