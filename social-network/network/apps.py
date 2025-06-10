from django.apps import AppConfig


class NetworkConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "network"
    verbose_name = "Social Network"

    def ready(self):
        import network.signals
