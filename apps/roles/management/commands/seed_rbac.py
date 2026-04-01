from django.core.management.base import BaseCommand
from apps.roles.seed.run_seed import run_seed

class Command(BaseCommand):
    help = "Seed RBAC roles and permissions"

    def handle(self, *args, **kwargs):
        run_seed()