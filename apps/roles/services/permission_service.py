def user_has_permission(user, permission_code: str) -> bool:
    """
    Vérifie si un user possède une permission via son rôle
    """
    if not user or not user.is_authenticated:
        return False

    if not hasattr(user, "role") or user.role is None:
        return False

    return user.role.permissions.filter(
        code=permission_code
    ).exists()
