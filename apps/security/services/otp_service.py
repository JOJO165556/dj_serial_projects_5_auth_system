# OTP stocké dans Redis (TTL 5min) — pas de modèle en base
import random
from infrastructure.redis.redis_client import client
from apps.security.tasks import send_email_task

def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def create_otp(user) -> str:
    code = generate_otp()
    key = f"otp:{user.id}"
    client.set(key, code, ex=300)  # expire après 5 minutes
    return code


def verify_otp(user, code: str) -> bool:
    key = f"otp:{user.id}"
    stored = client.get(key)

    if not stored:
        return False

    if str(stored) != str(code) and (isinstance(stored, bytes) and stored.decode() != code):
        # Pour gérer au cas où c'est bytes ou str selon config redis
        if isinstance(stored, bytes):
            stored = stored.decode()
        if str(stored) != str(code):
            return False

    client.delete(key)  # usage unique, invalide après vérification
    return True
