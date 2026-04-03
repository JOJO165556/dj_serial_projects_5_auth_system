#Pour traquer ce qui se passe

from apps.security.models.security_log import SecurityLog

def log_security_event(user, action: str, ip=None):
    SecurityLog.objects.create(
        user=user,
        action=action,
        ip_address=ip
    )