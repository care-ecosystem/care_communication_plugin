from rest_framework import serializers

from care_communication.models.feedback import PatientFeedback


class PatientFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientFeedback
        fields = "__all__"
