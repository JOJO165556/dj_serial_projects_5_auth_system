from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views.user_views import MeView
from .views.auth_views import LoginView, LogoutView, RegisterView
from .views.protected_view import ProtectedTestView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('refresh/', TokenObtainPairView.as_view()),
    path('me/', MeView.as_view()), #Route protégée
    path('protected/', ProtectedTestView.as_view()),
]