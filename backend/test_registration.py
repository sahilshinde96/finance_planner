#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.serializers import RegisterSerializer

# Test registration
data = {
    'username': 'testuser123', 
    'email': 'test@example.com', 
    'password': 'testpassword123'
}

serializer = RegisterSerializer(data=data)
print(f"Valid: {serializer.is_valid()}")
print(f"Errors: {serializer.errors}")

if serializer.is_valid():
    user = serializer.save()
    print(f"✅ User created - Username: {user.username}, Email: {user.email}, Approved: {user.is_approved}")
else:
    print("❌ Registration failed")
