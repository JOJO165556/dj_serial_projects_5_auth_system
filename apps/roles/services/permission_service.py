from infrastructure.redis.redis_client import client
import json

def get_user_permissions(user):
    key = f"user:{user.id}:permissions"

    cached = client.get(key)

    if cached:
        return json.loads(cached)

    permissions = list(
        user.role.permissions.values_list("code", flat=True)
    )

    client.set(key, json.dumps(permissions), ex=3600)

    return permissions

def user_has_permission(user, permission_code: str) -> bool:
    """
    Vérifie si un user possède une permission via son rôle
    """
    if not user or not user.is_authenticated:
        return False

    permissions = get_user_permissions(user)

    return permission_code in permissions
