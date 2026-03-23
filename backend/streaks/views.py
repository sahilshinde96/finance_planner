from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Streak, Badge, UserBadge, ActivityLog
from .serializers import StreakSerializer, BadgeSerializer, UserBadgeSerializer


class StreakView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        streak, _ = Streak.objects.get_or_create(user=request.user)
        return Response(StreakSerializer(streak).data)

    def post(self, request):
        """Daily check-in"""
        streak, _ = Streak.objects.get_or_create(user=request.user)
        checked_in = streak.check_in()
        return Response({
            'checked_in': checked_in,
            'current_streak': streak.current_streak,
            'total_points': streak.total_points,
            'message': f'🔥 {streak.current_streak} day streak!' if checked_in else 'Already checked in today.',
        })


class UserBadgesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        badges = UserBadge.objects.filter(user=request.user).select_related('badge')
        return Response(UserBadgeSerializer(badges, many=True).data)


class AllBadgesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        all_badges = Badge.objects.all()
        user_badge_ids = set(UserBadge.objects.filter(user=request.user).values_list('badge_id', flat=True))
        return Response([
            {**BadgeSerializer(b).data, 'earned': b.id in user_badge_ids}
            for b in all_badges
        ])


class CheckInView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Daily check-in endpoint"""
        streak, _ = Streak.objects.get_or_create(user=request.user)
        checked_in = streak.check_in()
        return Response({
            'checked_in': checked_in,
            'current_streak': streak.current_streak,
            'total_points': streak.total_points,
            'longest_streak': streak.longest_streak,
            'message': f'🔥 {streak.current_streak} day streak!' if checked_in else 'Already checked in today.',
        })


class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from django.db.models import Sum
        top = (Streak.objects
               .select_related('user')
               .order_by('-total_points')[:15])
        return Response([
            {
                'rank': i + 1,
                'username': s.user.username,
                'total_points': s.total_points,
                'current_streak': s.current_streak,
                'longest_streak': s.longest_streak,
                'is_me': s.user.id == request.user.id,
            }
            for i, s in enumerate(top)
        ])
