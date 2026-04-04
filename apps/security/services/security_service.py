#Pour traquer ce qui se passe

from apps.security.models.security_log import SecurityLog

def log_security_event(user, action: str, ip=None):
    SecurityLog.objects.create(
        user=user,
        action=action,
        ip_address=ip
    )

# Récupérer IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]

    return request.META.get('REMOTE_ADDR')