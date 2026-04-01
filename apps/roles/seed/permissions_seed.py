from apps.roles.models.permission import Permission

PERMISSIONS = [
    "view_dashboard",
    "create_user",
    "delete_view",
    "edit_user",
]

def seed_permission():
    for code in PERMISSIONS:
        Permission.objects.get_or_create(
            code=code,
            defaults={"name": code}
        )