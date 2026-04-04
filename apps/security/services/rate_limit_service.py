from infrastructure.redis.redis_client import client
from rest_framework.exceptions import Throttled

def rate_limit(key: str, limit: int = 5, window: int = 60):
    """
    key: ex login:127.0.0.1
    limit: nombre max de requêtes
    window: durée en secondes
    """

    current = client.get(key)

    if current:
        current = int(current)

        if current >= limit:
            raise Throttled(detail="Too many requests, try again later")

        client.incr(key)

    else:
        client.set(key, 1, ex=window)
