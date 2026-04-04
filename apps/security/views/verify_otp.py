from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from apps.security.services.otp_service import verify_otp


@extend_schema(
    request=inline_serializer(
        name='VerifyOTPRequest',
        fields={'code': serializers.CharField()}
    ),
    responses={
        200: inline_serializer(
            name='VerifyOTPResponse',
            fields={'message': serializers.CharField()}
        )
    }
)
class VerifyOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')

        is_valid = verify_otp(request.user, code)

        if not is_valid:
            return Response({"error": "Invalid or expired OTP"}, status=400)

        return Response({"message": "OTP verified"})