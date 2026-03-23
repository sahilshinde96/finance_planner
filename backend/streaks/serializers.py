from rest_framework import serializers
from .models import Streak, Badge, UserBadge

class StreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streak
        fields = ['current_streak', 'longest_streak', 'total_points', 'last_activity_date']

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'icon', 'requirement', 'points_value', 'badge_type']

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    class Meta:
        model = UserBadge
        fields = ['badge', 'earned_at']
