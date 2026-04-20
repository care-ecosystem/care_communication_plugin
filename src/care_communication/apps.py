from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

PLUGIN_NAME = "care_communication"


class CareCommunicationConfig(AppConfig):
    name = PLUGIN_NAME
    verbose_name = _("Care communication")

    def ready(self):
        import care_communication.signals  # noqa F401
