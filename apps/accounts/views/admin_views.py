from rest_framework.views import APIView
from rest_framework.response import Response

from apps.roles.decorators.rbac_decorators import permission_required

class AdminOnlyView(APIView):

    @permission_required("view_dashboard")
    def get(self, request):
        return Response({"message": "Bienvenue dans le dashboard admin"})