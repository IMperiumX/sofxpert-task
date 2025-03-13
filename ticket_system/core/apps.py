import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ticket_system.core"

    def ready(self):
        with contextlib.suppress(ImportError):
            import ticket_system.core.signals  # noqa: F401
