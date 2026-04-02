from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.roles.services.role_service import assign_role
from apps.roles.models.role import Role

class AssignRoleView(APIView):
    def post(self, request):
        user = request.user
        role_id = request.data.get("role_id")

        if not role_id:
            return Response(
                {"error": "role id required"},
                status=400
            )

        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            raise NotFound("Role not found")

        assign_role(user, role)

        return Response({
            "message": f"Role '{role.name}' assigned successfully"
        })