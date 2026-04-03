#Pour éviter les queries dans les views
from django.contrib.auth import get_user_model

User = get_user_model()

def get_user_by_email(email):
    return User.objects.filter(email=email).first()