from .permissions_seed import seed_permission
from .roles_seed import seed_roles

def run_seed():
    seed_permission()
    seed_roles()

    print("RBAC seed completed successfully")