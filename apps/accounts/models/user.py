from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey('roles.Role', on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']