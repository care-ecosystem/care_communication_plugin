from django.db import models

from care.utils.models.base import BaseModel

from care_communication.models.choices import Channel, ReferenceType

class CommunicationSession(BaseModel):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE"
        COMPLETED = "COMPLETED"
        EXPIRED = "EXPIRED"

    patient = models.ForeignKey("emr.Patient", on_delete=models.PROTECT)
    reference_id = models.UUIDField()
    reference_type = models.CharField(max_length=50, choices=ReferenceType.choices)
    channel = models.CharField(max_length=20, choices=Channel.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    flow_id = models.CharField(max_length=100, null=True, blank=True)
    current_step = models.PositiveIntegerField(default=1)
    context = models.JSONField(default=dict)
    expires_at = models.DateTimeField()

    @property
    def started_at(self):
        return self.created_at

    @property
    def last_interaction_at(self):
        return self.updated_at

    class Meta:
        indexes = [models.Index(fields=["patient", "channel", "status"])]
