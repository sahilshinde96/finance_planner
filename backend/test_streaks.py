#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from streaks.models import Streak, Badge

# Create test user
User = get_user_model()
user = User.objects.filter(username='testuser').first()
if not user:
    user = User.objects.create_user(username='testuser', email='test@example.com', password='test123')
    user.is_approved = True
    user.save()

# Create test badge
badge = Badge.objects.first() or Badge.objects.create(
    name='First Badge',
    description='Your first achievement',
    icon='🏆',
    requirement='Complete any action',
    points_value=50
)

# Create/get streak
streak, _ = Streak.objects.get_or_create(user=user)

print(f"✅ Test user: {user.username}")
print(f"✅ Test streak: {streak.current_streak} days")
print(f"✅ Test badge: {badge.name}")
print(f"✅ All systems ready for testing")
