from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..serializers.auth_serializer import LoginSerializer, RegisterSerializer
from ..services.auth_service import login_user, logout_user
from apps.common.utils.response import success_response, error_response


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = login_user(
            serializer.validated_data['email'],
            serializer.validated_data['password']
        )
        return success_response(data=tokens)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return error_response("No token")

        logout_user(refresh_token)

        return success_response(message="Logged out")

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="User created successfully", status=201)
        return error_response(str(serializer.errors))
