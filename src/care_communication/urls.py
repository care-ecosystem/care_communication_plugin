from rest_framework.routers import DefaultRouter, SimpleRouter

from django.conf import settings

from care_communication.api.viewsets.kiosk import KioskViewSet
from care_communication.api.viewsets.template import NotificationTemplateViewSet
from care_communication.api.viewsets.feedback import PatientFeedbackViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("kiosk", KioskViewSet, basename="kiosk")
router.register("templates", NotificationTemplateViewSet, basename="templates")
router.register("feedback", PatientFeedbackViewSet, basename="feedback")

urlpatterns = router.urls
