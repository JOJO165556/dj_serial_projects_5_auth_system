from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from security.utils.token_blacklist import blacklist_token


def login_user(email, password):
    user = authenticate(email=email, password=password)

    if user is None:
        raise AuthenticationFailed("Invalid credentials")

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh":  str(refresh)
    }

def logout_user(refresh_token):
    blacklist_token(refresh_token)