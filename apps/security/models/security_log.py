from django.db import models
from django.conf import settings

class SecurityLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='security_logs'
    )
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)