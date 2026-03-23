from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/',       views.RegisterView.as_view(),           name='register'),
    path('login/',          views.LoginView.as_view(),              name='login'),
    path('profile/',        views.ProfileView.as_view(),            name='profile'),
    path('token/refresh/',  TokenRefreshView.as_view(),             name='token_refresh'),
    # Admin endpoints
    path('admin/users/',                    views.AdminPendingUsersView.as_view(),  name='admin_users'),
    path('admin/users/<int:user_id>/action/', views.AdminApproveUserView.as_view(), name='admin_approve'),
    path('admin/stats/',                    views.AdminStatsView.as_view(),         name='admin_stats'),
]
