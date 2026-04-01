def assign_role(user, role):
    """
    Assigne un rôle à un utilisateur
    """
    user.role = role
    user.save()