from datetime import datetime
import re

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from care.emr.models import Patient


class KioskDOBAuthentication(BaseAuthentication):
    def authenticate(self, request):
        patient_id = request.headers.get("X-Patient-UUID")
        dob = request.headers.get("X-Patient-DOB")

        if not patient_id or not dob:
            raise AuthenticationFailed("Missing credentials")

        try:
            patient = Patient.objects.get(external_id=patient_id)
        except Patient.DoesNotExist:
            raise AuthenticationFailed("User is not authorized to access patient data")

        try:
            cleaned_dob = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            raise AuthenticationFailed("Invalid date format. Expected YYYY-MM-DD")

        if patient.date_of_birth != cleaned_dob:
            raise AuthenticationFailed("User is not authorized to access patient data")

        return (patient, None)
