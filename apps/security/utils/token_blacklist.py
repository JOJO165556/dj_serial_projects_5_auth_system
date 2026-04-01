import time

from rest_framework.exceptions import AuthenticationFailed

from infrastructure.redis.redis_client import client
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
import hashlib

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def blacklist_token(token: str):
    """
    Ajoute un token dans Redis pour le bloquer
    """
    try:
        UntypedToken(token) #type: ignore
        refresh = RefreshToken(token) #type: ignore
        exp = refresh['exp']
    except Exception:
        raise AuthenticationFailed("Invalid token")

    ttl = max(exp - int(time.time()), 0)

    hashed = hash_token(token)
    client.set(hashed, "blacklisted", ex=ttl)

def is_token_blacklisted(token: str) -> bool:
    """
    Vérifie si un token est blacklisté
    """
    hashed = hash_token(token)
    return bool(client.exists(hashed))