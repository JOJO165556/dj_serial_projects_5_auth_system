from rest_framework.views import APIView
from rest_framework.response import Response
from apps.roles.decorators.rbac_decorators import permission_required

class DashboardView(APIView):

    @permission_required("view_dashboard")
    def get(self, request):
        return Response({
            "message": "Dashboard accessible"
        })

class DeleteUserView(APIView):
    @permission_required("delete_user")
    def get(self, request):
        return Response({
            "message": "User deleted"
        })