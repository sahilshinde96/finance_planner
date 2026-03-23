from rest_framework import serializers
from .models import FinancialGoal


class FinancialGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.FloatField(read_only=True, source='progress_percentage')

    class Meta:
        model = FinancialGoal
        fields = ['id', 'name', 'target_amount', 'current_amount', 'target_date',
                  'status', 'priority', 'notes', 'progress_percentage', 'created_at']
        read_only_fields = ['id', 'created_at']


class SIPSerializer(serializers.Serializer):
    monthly_investment = serializers.FloatField(min_value=1)
    annual_rate = serializers.FloatField(min_value=0.1, max_value=50)
    years = serializers.IntegerField(min_value=1, max_value=50)


class EMISerializer(serializers.Serializer):
    principal = serializers.FloatField(min_value=1)
    annual_rate = serializers.FloatField(min_value=0.1, max_value=50)
    years = serializers.IntegerField(min_value=1, max_value=30)


class TaxSerializer(serializers.Serializer):
    annual_income = serializers.FloatField(min_value=0)
    deductions_80c = serializers.FloatField(default=0)
    deductions_80d = serializers.FloatField(default=0)
    other_deductions = serializers.FloatField(default=0)
    regime = serializers.ChoiceField(choices=['old', 'new'], default='new')


class RetirementSerializer(serializers.Serializer):
    current_age = serializers.IntegerField(min_value=18, max_value=65)
    retirement_age = serializers.IntegerField(min_value=40, max_value=75)
    monthly_expenses = serializers.FloatField(min_value=1)
    current_savings = serializers.FloatField(default=0)
    expected_return = serializers.FloatField(default=10.0)
    inflation_rate = serializers.FloatField(default=6.0)
