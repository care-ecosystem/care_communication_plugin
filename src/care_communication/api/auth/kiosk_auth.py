from datetime import datetime
import re

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from care.emr.models import Patient


class KioskDOBAuthentication(BaseAuthentication):
    def authenticate(self, request):
        method = request.method

        if method == "POST":
            patient_id = request.data.get("patient_id")
            birth_year = request.data.get("birth_year")
        else:
            patient_id = request.query_params.get("patient_id")
            birth_year = request.query_params.get("birth_year")

        if not patient_id or not birth_year:
            raise AuthenticationFailed("Missing credentials")

        try:
            patient = Patient.objects.get(external_id=patient_id)
        except Patient.DoesNotExist:
            raise AuthenticationFailed("User is not authorized to access patient data")

        try:
            birth_year = int(birth_year)
        except ValueError:
            raise AuthenticationFailed("Invalid birth year")

        if patient.date_of_birth.year != birth_year:
            raise AuthenticationFailed("User is not authorized to access patient data")

        return (patient, None)
