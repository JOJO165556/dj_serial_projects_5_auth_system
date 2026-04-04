from rest_framework.views import APIView
from rest_framework.response import Response
from apps.roles.decorators.rbac_decorators import permission_required
from apps.security.services.security_service import log_security_event, get_client_ip


class DashboardView(APIView):

    @permission_required("view_dashboard")
    def get(self, request):

        log_security_event(
            request.user,
            "ACCESS DASHBOARD",
            get_client_ip(request)
        )

        return Response({
            "message": "Dashboard accessible"
        })


class DeleteUserView(APIView):
    @permission_required("delete_user")
    def get(self, request):
        return Response({
            "message": "User deleted"
        })