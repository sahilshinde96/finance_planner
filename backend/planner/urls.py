from django.urls import path
from . import views

urlpatterns = [
    path('goals/', views.FinancialGoalListCreateView.as_view(), name='goal_list'),
    path('goals/<int:pk>/', views.FinancialGoalDetailView.as_view(), name='goal_detail'),
    path('calculate/sip/', views.SIPCalculatorView.as_view(), name='calc_sip'),
    path('calculate/emi/', views.EMICalculatorView.as_view(), name='calc_emi'),
    path('calculate/tax/', views.TaxCalculatorView.as_view(), name='calc_tax'),
    path('calculate/retirement/', views.RetirementCalculatorView.as_view(), name='calc_retirement'),
    path('ml-plan/', views.MLFinancePlannerView.as_view(), name='ml_finance_plan'),
]
