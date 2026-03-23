from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from .serializers import RegisterSerializer, UserProfileSerializer, UserApprovalSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'Registration successful. Please wait for admin approval.',
            'username': user.username,
            'status': 'pending',
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()
        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid username or password.'}, status=401)

        if not user.is_staff and not user.is_superuser:
            if user.is_rejected:
                reason = user.rejection_reason or 'Contact the administrator.'
                return Response({'error': f'Registration rejected. {reason}', 'status': 'rejected'}, status=403)
            if not user.is_approved:
                return Response({'error': 'Account pending admin approval.', 'status': 'pending'}, status=403)

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'is_admin': user.is_staff or user.is_superuser,
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user


class AdminPendingUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        filter_status = request.query_params.get('status', 'pending')
        base = User.objects.filter(is_staff=False, is_superuser=False)
        if filter_status == 'pending':
            users = base.filter(is_approved=False, is_rejected=False)
        elif filter_status == 'approved':
            users = base.filter(is_approved=True)
        elif filter_status == 'rejected':
            users = base.filter(is_rejected=True)
        else:
            users = base.all()
        return Response(UserApprovalSerializer(users.order_by('-registered_at'), many=True).data)


class AdminApproveUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, is_staff=False, is_superuser=False)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        action = request.data.get('action')
        reason = request.data.get('reason', '')

        if action == 'approve':
            user.is_approved = True
            user.is_rejected = False
            user.rejection_reason = ''
            user.approved_by = request.user
            user.approved_at = timezone.now()
            user.save()
            return Response({'message': f'{user.username} approved.', 'user': UserApprovalSerializer(user).data})

        elif action == 'reject':
            user.is_approved = False
            user.is_rejected = True
            user.rejection_reason = reason
            user.save()
            return Response({'message': f'{user.username} rejected.', 'user': UserApprovalSerializer(user).data})

        return Response({'error': 'action must be approve or reject.'}, status=400)


class AdminStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        base = User.objects.filter(is_staff=False, is_superuser=False)
        return Response({
            'total_users': base.count(),
            'pending':  base.filter(is_approved=False, is_rejected=False).count(),
            'approved': base.filter(is_approved=True).count(),
            'rejected': base.filter(is_rejected=True).count(),
        })
