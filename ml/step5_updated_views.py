"""
ARTH — Updated planner/views.py
Replace your existing planner/views.py with this file.
The MLFinancePlannerView now uses the trained ML models (with rule-based fallback).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ml'))

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FinancialGoal
from .serializers import (
    FinancialGoalSerializer, SIPSerializer, EMISerializer,
    TaxSerializer, RetirementSerializer,
)
from .calculators import calculate_sip, calculate_emi, calculate_tax, calculate_retirement


# ── Standard Calculators ───────────────────────────────────────────────────────
class FinancialGoalListCreateView(generics.ListCreateAPIView):
    serializer_class = FinancialGoalSerializer
    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FinancialGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FinancialGoalSerializer
    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)


class SIPCalculatorView(APIView):
    def post(self, request):
        s = SIPSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(calculate_sip(**s.validated_data))


class EMICalculatorView(APIView):
    def post(self, request):
        s = EMISerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(calculate_emi(**s.validated_data))


class TaxCalculatorView(APIView):
    def post(self, request):
        s = TaxSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(calculate_tax(**s.validated_data))


class RetirementCalculatorView(APIView):
    def post(self, request):
        s = RetirementSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(calculate_retirement(**s.validated_data))


# ── ML Finance Planner ─────────────────────────────────────────────────────────
class MLFinancePlannerView(APIView):
    """
    POST /api/planner/ml-plan/
    Uses trained ML models from ml/models/ if available.
    Falls back to rule-based engine if models not trained yet.
    """
    def post(self, request):
        try:
            from ml_predictor import FinancePlanner
            result = FinancePlanner.predict(request.data)
            return Response(result)
        except Exception as e:
            return Response(
                {'error': f'Prediction failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
