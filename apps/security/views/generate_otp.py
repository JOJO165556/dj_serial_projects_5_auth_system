from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.security.services.otp_service import create_otp


class GenerateOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        otp = create_otp(request.user)

        return Response({
            "message": "OTP generated",
            "otp": otp.code  # En DEV UNIQUEMENT
        })