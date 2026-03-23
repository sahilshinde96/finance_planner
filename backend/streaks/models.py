from django.db import models
from django.conf import settings
from django.utils import timezone


class Streak(models.Model):
    """Tracks daily engagement streaks."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)

    def check_in(self):
        today = timezone.now().date()
        if self.last_activity_date == today:
            return False
        if self.last_activity_date and (today - self.last_activity_date).days == 1:
            self.current_streak += 1
        else:
            self.current_streak = 1
        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_activity_date = today
        self.total_points += 10
        self.save()
        return True

    def __str__(self):
        return f"{self.user.username}: {self.current_streak} day streak"


class Badge(models.Model):
    BADGE_TYPE_CHOICES = [
        ('quiz', 'Quiz'),
        ('streak', 'Streak'),
        ('achievement', 'Achievement'),
        ('feature', 'Feature'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🏆')
    requirement = models.CharField(max_length=200, help_text='e.g., "Complete 5 quizzes"')
    points_value = models.PositiveIntegerField(default=50)
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPE_CHOICES, default='achievement')

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} earned {self.badge.name}"


class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    date = models.DateField()
    activity_type = models.CharField(max_length=50)
    points_earned = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date', 'activity_type')
        ordering = ['-date']
