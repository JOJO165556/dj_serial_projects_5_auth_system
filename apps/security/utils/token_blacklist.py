from infrastructure.redis.redis_client import client

def black_list_token(token: str):
    """
    Ajoute un token dans Redis pour le bloquer
    """
    client.set(token, "blacklisted", ex=3600)

def is_token_blacklisted(token: str) -> bool:
    """
    Vérifie si un token est blacklisté
    """
    return client.exists(token) == 1