from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        # Import signals to ensure profile creation hooks are registered.
        from . import signals  # noqa: F401
