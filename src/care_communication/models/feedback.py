from django.db import models

from care.utils.models.base import BaseModel

from care_communication.models.choices import ReferenceType
from care_communication.models.communication import CommunicationSession

class PatientFeedback(BaseModel):

    class IssueCategory(models.TextChoices):
        CLEANLINESS = "CLEANLINESS"
        STAFF_BEHAVIOR = "STAFF_BEHAVIOR"
        WAIT_TIME = "WAIT_TIME"
        TREATMENT_SATISFACTION = "TREATMENT_SATISFACTION"
        OTHER = "OTHER"

    patient = models.ForeignKey("emr.Patient", on_delete=models.SET_NULL)
    reference_id = models.UUIDField()
    reference_type = models.CharField(max_length=50, choices=ReferenceType.choices)
    session = models.OneToOneField(
        CommunicationSession, null=True, blank=True, on_delete=models.SET_NULL
    )
    rating = models.PositiveIntegerField(null=True, blank=True)
    issue_category = models.CharField(max_length=20, choices=IssueCategory.choices)
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ["patient", "reference_type", "issue_category"]
