"""URL routing for the backend app."""

from __future__ import annotations

from rest_framework.routers import DefaultRouter

from backend.viewsets import MedicalEventViewSet, RegistrationRequestViewSet

router = DefaultRouter()
router.register(r"medical-events", MedicalEventViewSet, basename="medical-event")
router.register(r"registration-requests", RegistrationRequestViewSet, basename="registration-request")

urlpatterns = router.urls
