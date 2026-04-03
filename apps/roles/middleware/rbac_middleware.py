# protège auto certaines routes
from django.http import JsonResponse

class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        #Exemple: protéger /api/protected/
        if request.path.startswith("/api/protected/"):
            user = request.user

            if not user or not user.is_authenticated:
                return JsonResponse({"error": "Unauthorized"}, status=401)

            if not hasattr(user, "role") or not user.role:
                return JsonResponse({"error": "No role assigned"}, status=403)

            return self.get_response(request)