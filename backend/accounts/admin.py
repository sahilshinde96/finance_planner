from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'category', 'age', 'risk_level']
    fieldsets = UserAdmin.fieldsets + (
        ('Financial Profile', {'fields': ('age', 'income_range', 'risk_level', 'financial_goals', 'category', 'location')}),
    )
