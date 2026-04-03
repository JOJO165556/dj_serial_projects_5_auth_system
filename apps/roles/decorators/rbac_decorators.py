from functools import wraps

from rest_framework.exceptions import PermissionDenied
from apps.roles.services.permission_service import user_has_permission

def permission_required(permission_code):
    """
    Bloque l'accès si la permission manque
    """
    def decorator(view_func):

        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):

            # Pour éviter le AnonymmousUser
            if not request.user or not request.user.is_authenticated:
                raise PermissionDenied("Authentication required")

            if not user_has_permission(request.user, permission_code):
                raise PermissionDenied(f"Missing permission: {permission_code}")

            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator