from rest_framework import serializers

from care.facility.models import Facility

from care_communication.models.templates import NotificationTemplate


class NotificationTemplateSerializer(serializers.ModelSerializer):
    facility = serializers.SlugRelatedField(
        queryset=Facility.objects.all(),
        slug_field="external_id"
    )

    class Meta:
        model = NotificationTemplate
        fields = "__all__"
