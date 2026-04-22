from rest_framework.routers import DefaultRouter, SimpleRouter

from django.conf import settings

from care_communication.api.viewsets.kiosk import KioskViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("kiosk", KioskViewSet, basename="kiosk")

urlpatterns = router.urls
