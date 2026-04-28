from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from care_communication.models.templates import NotificationTemplate
from care_communication.api.serializers.template import NotificationTemplateSerializer

class NotificationTemplateViewSet(ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAdminUser]
