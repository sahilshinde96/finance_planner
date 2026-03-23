from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model with financial profile fields."""
    RISK_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    CATEGORY_CHOICES = [
        ('general', 'General Public'), ('farmer', 'Farmer'),
        ('corporate', 'Corporate'), ('student', 'Student'), ('business', 'Business Owner'),
    ]

    age = models.PositiveIntegerField(null=True, blank=True)
    income_range = models.CharField(max_length=20, blank=True)
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, default='medium')
    financial_goals = models.JSONField(default=dict, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    location = models.CharField(max_length=100, blank=True)

    # ── Approval fields ───────────────────────────────────────────────────────
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    rejection_reason = models.CharField(max_length=300, blank=True)
    approved_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='approved_users'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def approval_status(self):
        if self.is_superuser or self.is_staff:
            return 'admin'
        if self.is_rejected:
            return 'rejected'
        if self.is_approved:
            return 'approved'
        return 'pending'

    def __str__(self):
        return f"{self.username} ({self.approval_status()})"
