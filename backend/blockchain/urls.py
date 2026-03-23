from django.urls import path
from .views import BlockchainRecordsView, VerifyChainView
urlpatterns = [
    path('records/', BlockchainRecordsView.as_view(), name='blockchain_records'),
    path('verify/', VerifyChainView.as_view(), name='blockchain_verify'),
]
