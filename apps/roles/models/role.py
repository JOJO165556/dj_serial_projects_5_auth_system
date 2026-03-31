from django.db import models
from .permission import Permission

class Role(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')

    def __str__(self):
        return self.name
