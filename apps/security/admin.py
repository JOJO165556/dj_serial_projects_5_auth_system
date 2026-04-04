from django.contrib import admin
from .models.security_log import SecurityLog

@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "ip_address", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("action")