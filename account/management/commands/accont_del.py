from typing import Any
from django.core.management.base import  BaseCommand
from django.contrib.auth import get_user_model

User=get_user_model()

class Command(BaseCommand):
    help="To delete all user with False"

    def handle(self, *args: Any, **options: Any) -> str | None:
        User.objects.filter(is_verified=False).delete()
        return 