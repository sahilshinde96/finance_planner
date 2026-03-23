from django.contrib import admin
from .models import Streak, Badge, UserBadge
admin.site.register(Streak)
admin.site.register(Badge)
admin.site.register(UserBadge)
