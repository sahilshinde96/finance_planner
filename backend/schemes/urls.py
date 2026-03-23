from django.urls import path
from .views import SchemeListView
urlpatterns = [path('', SchemeListView.as_view(), name='scheme_list')]
