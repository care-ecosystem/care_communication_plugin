from datetime import timedelta

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django.db import transaction

from care.emr.models.encounter import Encounter
from care.emr.resources.encounter.constants import StatusChoices
from care.emr.resources.encounter.spec import EncounterListSpec
from care.utils.shortcuts import get_object_or_404
from care.utils.time_util import care_now

from care_communication.api.auth.kiosk_auth import KioskDOBAuthentication
from care_communication.api.serializers.template import NotificationTemplateSerializer
from care_communication.models.communication import CommunicationSession
from care_communication.models.feedback import PatientFeedback
from care_communication.models.templates import NotificationTemplate


class KioskViewSet(GenericViewSet):
    authentication_classes = [KioskDOBAuthentication]
    permission_classes = [AllowAny]

    def validate_reference(self, reference_id, reference_type):
        if reference_type == "ENCOUNTER":
            get_object_or_404(Encounter, external_id=reference_id)


    @action(detail=False, methods=["post"], url_path="validate-patient")
    def validate_patient(self, request):
        return Response({"detail": "Patient validated successfully."})


    @action(detail=False, methods=["get"], url_path="encounters")
    def encounters(self, request):
        valid_statuses = [
            StatusChoices.in_progress.value,
            StatusChoices.completed.value,
            StatusChoices.discharged.value,
            StatusChoices.discontinued.value
        ]

        encounters = Encounter.objects.filter(
            patient=request.user,
            status__in=valid_statuses,
        ).select_related("facility").order_by("-created_date")

        data = [
            EncounterListSpec.serialize(obj).to_json()
            for obj in encounters
        ]
        return Response(data)


    @action(detail=False, methods=["get"], url_path="feedback-template")
    def feedback_template(self, request):
        reference_id = request.query_params.get("reference_id")
        reference_type = request.query_params.get("reference_type")
        event_type = request.query_params.get("event_type")

        self.validate_reference(reference_id, reference_type)

        template = NotificationTemplate.objects.filter(
            reference_type=reference_type,
            event_type=event_type,
            channel="KIOSK",
            active=True
        ).order_by("-version").first()

        if not template:
            return Response({"detail": "No feedback template found."}, status=404)

        with transaction.atomic():
            session = CommunicationSession.objects.filter(
                patient=request.user,
                reference_id=reference_id,
                reference_type=reference_type,
                channel="KIOSK",
                expires_at__gt=care_now()
            ).first()

            if not session:
                session = CommunicationSession.objects.create(
                    patient=request.user,
                    reference_id=reference_id,
                    reference_type=reference_type,
                    channel="KIOSK",
                    expires_at=care_now() + timedelta(hours=24)
                )

        return Response(NotificationTemplateSerializer(template).data)


    @action(detail=False, methods=["post"], url_path="save-feedback")
    def save_feedback(self, request):
        feedback_fields = request.data.get("feedback")
        reference_id = request.data.get("reference_id")
        reference_type = request.data.get("reference_type")

        self.validate_reference(reference_id, reference_type)

        session = get_object_or_404(
            CommunicationSession,
            patient=request.user,
            reference_id=reference_id,
            reference_type=reference_type,
            channel="KIOSK",
            expires_at__gt=care_now()
        )

        for field in feedback_fields:
            PatientFeedback.objects.get_or_create(
                patient=request.user,
                reference_id=reference_id,
                reference_type=reference_type,
                issue_category=field["issue_category"],
                defaults={
                    "session": session,
                    "rating": field.get("rating"),
                    "comment": field.get("comment", "")
                }
            )

        return Response({"detail": "Feedback saved successfully."})
