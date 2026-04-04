#Pour sécurité 2FA
import random
from datetime import timedelta
from django.utils import timezone

from apps.security.models.otp import OTP

def generate_otp():
    return str(random.randint(100000, 999999))

def create_otp(user):
    code = generate_otp()
    otp = OTP.objects.create(
        user=user,
        code=code,
        expires_at=timezone.now() + timedelta(minutes=5)
    )
    return otp

def verify_otp(user, code: str):
    otp = OTP.objects.filter(
        user=user,
        code=code,
        is_used=False
    ).order_by("-created_at").first()

    if not otp:
        return False

    if timezone.now() > otp.expires_at:
        return False

    otp.is_used = True
    otp.save()

    return True