from django.db import models


class GovernmentScheme(models.Model):
    CATEGORY_CHOICES = [
        ('savings', 'Savings'), ('insurance', 'Insurance'), ('pension', 'Pension'),
        ('business', 'Business/MSME'), ('education', 'Education'),
        ('subsidy', 'Subsidy'), ('health', 'Healthcare'), ('housing', 'Housing'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    benefits = models.TextField()
    eligibility_criteria = models.TextField()
    min_age = models.PositiveIntegerField(null=True, blank=True)
    max_age = models.PositiveIntegerField(null=True, blank=True)
    max_income = models.PositiveIntegerField(null=True, blank=True, help_text='Annual income limit in INR')
    state = models.CharField(max_length=100, default='All India')
    applicable_categories = models.CharField(max_length=200, default='General,SC,ST,OBC')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
