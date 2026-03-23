from django.contrib import admin
from .models import GovernmentScheme
@admin.register(GovernmentScheme)
class GovernmentSchemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'state', 'is_active']
    list_filter = ['category', 'is_active']
