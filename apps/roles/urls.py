from django.urls import path, include

from .views.test_views import DashboardView
from .views.role_views import AssignRoleView

urlpatterns = [
    path("assign/", AssignRoleView.as_view(), name="assign"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]