from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from apps.security.services.otp_service import create_otp
from apps.security.tasks import send_email_task


@extend_schema(
    request=None,
    responses={
        200: inline_serializer(
            name='GenerateOTPResponse',
            fields={
                'message': serializers.CharField()
            }
        )
    }
)
class GenerateOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = create_otp(request.user)

        # Envoi asynchrone du mail via Celery
        send_email_task.delay(
            to_email=request.user.email,
            subject="Votre code de sécurité (OTP)",
            message=f"Bonjour,\n\nVoici votre code de vérification: {code}\nCe code expirera dans 5 minutes."
        )

        return Response({
            "message": "OTP generated and sent via email"
        })