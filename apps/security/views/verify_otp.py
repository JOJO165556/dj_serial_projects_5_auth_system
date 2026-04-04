from rest_framework.response import Response
from rest_framework.views import APIView

from apps.security.services.otp_service import verify_otp


class VerifyOTPView(APIView):
    def post(self, request):
        code = request.data.get('code')

        is_valid = verify_otp(request.user, code)

        if not is_valid:
            return Response({"error": "Invalid or expired OTP"}, status=400)

        return Response({"message": "OTP verified"})