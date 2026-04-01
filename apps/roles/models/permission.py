from django.db import models

class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True, default="unknown")
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name