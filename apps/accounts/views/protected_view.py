from rest_framework.views import APIView
from rest_framework.response import Response


class ProtectedTestView(APIView):
    """Route de test pour valider le RBACMiddleware"""

    def get(self, request):
        return Response({
            "message": "Accès autorisé",
            "user": request.user.email,
            "role": request.user.role.name if request.user.role else None
        })
