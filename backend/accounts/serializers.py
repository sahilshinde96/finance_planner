from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_approved = False   # always starts unapproved
        user.is_active = True      # can exist in DB, just not approved
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    approval_status = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'age', 'income_range', 'risk_level', 'financial_goals',
            'category', 'location', 'approval_status', 'is_admin',
        ]
        read_only_fields = ['id', 'username', 'email', 'approval_status', 'is_admin']

    def get_approval_status(self, obj):
        return obj.approval_status()

    def get_is_admin(self, obj):
        return obj.is_staff or obj.is_superuser


class UserApprovalSerializer(serializers.ModelSerializer):
    approval_status = serializers.SerializerMethodField()
    approved_by_username = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'category', 'location',
            'registered_at', 'approval_status', 'is_approved', 'is_rejected',
            'rejection_reason', 'approved_at', 'approved_by_username',
        ]

    def get_approval_status(self, obj):
        return obj.approval_status()

    def get_approved_by_username(self, obj):
        return obj.approved_by.username if obj.approved_by else None
