from django.db import models
from care.utils.models.base import BaseModel

from care_communication.models.choices import Channel, EventType, ReferenceType

class NotificationTemplate(BaseModel):

    class TriggerType(models.TextChoices):
        IMMEDIATE = "IMMEDIATE"
        DELAYED = "DELAYED"

    name = models.CharField(max_length=255)
    channel = models.CharField(max_length=20, choices=Channel.choices)

    facility = models.ForeignKey("facility.Facility", null=False, on_delete=models.CASCADE)

    template_id = models.CharField(max_length=255, blank=True, null=True)

    template_body = models.JSONField(null=True, blank=True)

    reference_type = models.CharField(max_length=50, choices=ReferenceType.choices)
    event_type = models.CharField(max_length=50, choices=EventType.choices)

    conditions = models.JSONField(null=True, blank=True)

    trigger_type = models.CharField(
        max_length=20, choices=TriggerType.choices, default=TriggerType.IMMEDIATE
    )
    delay_in_minutes = models.PositiveIntegerField(null=True, blank=True)
    priority = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=10, default="en")
    active = models.BooleanField(default=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} [{self.channel} | {self.event_type}]"
