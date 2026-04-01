from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers.auth_serializer import LoginSerializer
from ..services.auth_service import login_user, logout_user


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = login_user(
            serializer.validated_data['email'],
            serializer.validated_data['password']
        )
        return Response(tokens, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data['refresh_token']

        if not refresh_token:
            return Response({"error": "No token"}, status=400)

        logout_user(refresh_token)

        return Response({"message": "Logged out"})
