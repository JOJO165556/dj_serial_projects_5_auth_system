from infrastructure.redis.redis_client import client
from apps.roles.models.role import Role

def invalidate_user_permissions_cache(user):
    key = f"user:{user.id}:permissions"
    client.delete(key)

def assign_role(user, role :Role):
    """
    Assigne un rôle à un utilisateur
    """
    user.role = role
    user.save()