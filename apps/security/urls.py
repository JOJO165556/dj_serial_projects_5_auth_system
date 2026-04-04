from django.urls import path

from .views.generate_otp import GenerateOTPView
from .views.verify_otp import VerifyOTPView

urlpatterns = [
    path('generate/', GenerateOTPView.as_view()),
    path('verify/', VerifyOTPView.as_view()),
]
