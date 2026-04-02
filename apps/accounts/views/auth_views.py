from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers.auth_serializer import LoginSerializer, RegisterSerializer
from ..services.auth_service import login_user, logout_user
from rest_framework.permissions import AllowAny


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
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({"error": "No token"}, status=400)

        logout_user(refresh_token)

        return Response({"message": "Logged out"})

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message" : "User created successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
