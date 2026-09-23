from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from common.responses import APIResponse
from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ProfileUpdateSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: OpenApiResponse(description="User registered successfully")},
        summary="Register a new user",
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user, context={'request': request}).data
            return APIResponse.success(
                data={
                    "user": user_data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                message="Account registered successfully.",
                status_code=status.HTTP_201_CREATED,
            )
        return APIResponse.error(
            message="Registration failed.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: OpenApiResponse(description="Login successful with JWT tokens")},
        summary="User login",
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user, context={'request': request}).data
            return APIResponse.success(
                data={
                    "user": user_data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                message="Login successful.",
            )
        return APIResponse.error(
            message="Invalid credentials.",
            errors=serializer.errors,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="User logout and token revocation")
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return APIResponse.success(message="Logged out successfully.")
        except Exception as e:
            return APIResponse.error(message="Invalid token or already logged out.", errors=str(e))


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @extend_schema(summary="Get current user profile")
    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Profile retrieved successfully.")

    @extend_schema(request=ProfileUpdateSerializer, summary="Update user profile")
    def put(self, request):
        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user, context={'request': request}).data
            return APIResponse.success(data=user_data, message="Profile updated successfully.")
        return APIResponse.error(message="Failed to update profile.", errors=serializer.errors)

    @extend_schema(summary="Delete user account")
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return APIResponse.success(message="Account successfully deactivated.")


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=ChangePasswordSerializer, summary="Change account password")
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return APIResponse.error(message="Current password is incorrect.")
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return APIResponse.success(message="Password changed successfully.")
        return APIResponse.error(message="Invalid data.", errors=serializer.errors)


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=ForgotPasswordSerializer, summary="Request password reset token")
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            # In development/console mode, log the reset token or send email
            subject = "Movie Site - Password Reset Request"
            message = f"Hello {user.username},\n\nUse this reset token to change your password: {token}\n\nIf you did not request this, please ignore."
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER or 'noreply@moviesite.com', [email])
            except Exception:
                pass
            return APIResponse.success(
                data={"token_preview": token if settings.DEBUG else None},
                message="Password reset instructions sent to your email.",
            )
        return APIResponse.error(message="Error sending reset instructions.", errors=serializer.errors)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=ResetPasswordSerializer, summary="Reset password using token")
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return APIResponse.error(message="User not found.")

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return APIResponse.success(message="Password reset successfully. You can now login.")
            return APIResponse.error(message="Invalid or expired reset token.")
        return APIResponse.error(message="Invalid data provided.", errors=serializer.errors)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return APIResponse.success(data=response.data, message="Token refreshed successfully.")
        return APIResponse.error(message="Token refresh failed.", errors=response.data, status_code=response.status_code)
