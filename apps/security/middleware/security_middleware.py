import hashlib

from django.http import JsonResponse
from infrastructure.redis.redis_client import client

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

class TokenBlacklistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = request.headers.get("Authorization")

        if auth:
            parts = auth.split(" ")

            #vérification format "Bearer <token>"
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]
                hashed = hash_token(token)

                if client.exists(hashed):
                    return JsonResponse(
                        {"error": "Token blacklisted"},
                        status=401
                    )

        return self.get_response(request)