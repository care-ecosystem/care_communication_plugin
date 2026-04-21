from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from care_communication.api.auth.kiosk_auth import KioskDOBAuthentication

class KioskViewSet(GenericViewSet):
    authentication_classes = [KioskDOBAuthentication]
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"], url_path="validate-patient")
    def validate_patient(self, request):
        return Response({"detail": "Patient validated successfully."})

