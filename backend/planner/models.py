from django.db import models
from django.conf import settings


class FinancialGoal(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('completed', 'Completed'), ('paused', 'Paused')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='financial_goal_records')
    name = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return round(float(self.current_amount) / float(self.target_amount) * 100, 1)

    def __str__(self):
        return f"{self.user.username} — {self.name}"
