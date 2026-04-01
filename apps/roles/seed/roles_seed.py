from apps.roles.models.role import Role
from apps.roles.models.permission import Permission

def seed_roles():
    #ADMIN
    admin, _ = Role.objects.get_or_create(name="admin")

    admin.permissions.set(Permission.objects.all())

    #USER
    user, _ = Role.objects.get_or_create(name="user")
    user.permissions.set(
        Permission.objects.filter(
            code__in=["view_dashboard"]
        )
    )