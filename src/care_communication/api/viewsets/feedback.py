from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from care_communication.models.feedback import PatientFeedback
from care_communication.api.serializers.feedback import PatientFeedbackSerializer

class PatientFeedbackViewSet(ModelViewSet):
    queryset = PatientFeedback.objects.all()
    serializer_class = PatientFeedbackSerializer
    permission_classes = [IsAdminUser]
