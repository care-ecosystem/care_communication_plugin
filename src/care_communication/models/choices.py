from django.db import models

class Channel(models.TextChoices):
    WHATSAPP = "WHATSAPP"
    SMS = "SMS"
    EMAIL = "EMAIL"
    KIOSK = "KIOSK"


class ReferenceType(models.TextChoices):
    ENCOUNTER = "ENCOUNTER"
    SERVICE_REQUEST = "SERVICE_REQUEST"


class EventType(models.TextChoices):
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    RESULT_READY = "RESULT_READY"
