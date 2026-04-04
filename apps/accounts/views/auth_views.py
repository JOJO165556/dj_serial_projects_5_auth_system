from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

from apps.security.services.security_service import log_security_event, get_client_ip
from apps.security.services.rate_limit_service import rate_limit
from ..serializers.auth_serializer import LoginSerializer, RegisterSerializer
from ..services.auth_service import login_user, logout_user
from apps.common.utils.response import success_response, error_response
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers


@extend_schema(
    request=LoginSerializer,
    responses={
        200: inline_serializer(
            name='LoginResponse',
            fields={
                'access': serializers.CharField(),
                'refresh': serializers.CharField()
            }
        )
    }
)
class LoginView(APIView):

    def post(self, request):
        ip = get_client_ip(request)

        # Rate limit, limiter les tentatives de login
        rate_limit(f"login:{ip}", limit=5, window=60)
        rate_limit(f"user:{request.data.get('email')}")

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user, tokens = login_user(
                email,
                serializer.validated_data['password']
            )
        except AuthenticationFailed:
            log_security_event(
                user=None,
                action=f"FAILED_LOGIN: {email}",
                ip=ip
            )
            raise  # On relance l'erreur pour garder le comportement normal de DRF

        log_security_event(
            user,
            action="LOGIN",
            ip=ip
        )

        return success_response(data=tokens)

@extend_schema(
    request=inline_serializer(
        name='LogoutRequest',
        fields={'refresh_token': serializers.CharField()}
    ),
    responses={
        200: inline_serializer(
            name='LogoutResponse',
            fields={'message': serializers.CharField()}
        )
    }
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return error_response("No token")

        logout_user(refresh_token)

        log_security_event(
            request.user,
            "LOGOUT",
            get_client_ip(request)
        )

        return success_response(message="Logged out")

@extend_schema(
    request=RegisterSerializer,
    responses={
        201: inline_serializer(
            name='RegisterResponse',
            fields={'message': serializers.CharField()}
        )
    }
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        rate_limit(f"register:{get_client_ip(request)}", limit=3, window=300)

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="User created successfully", status=201)
        return error_response(str(serializer.errors))
