"""DRF ViewSets for the backend API.

Business logic that enforces clinical rules (specialty matching, FR-11/FR-12)
lives in perform_create so it runs on every POST regardless of how the view
is called.
"""

from __future__ import annotations

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, IsAuthenticated

from backend.models import MedicalEvent, RegistrationRequest, User
from backend.serializers import MedicalEventSerializer


class IsDoctor(BasePermission):
    """Allow access only to authenticated users with role=doctor and an existing DoctorProfile.

    Denying non-doctors here keeps the viewset clean and makes the permission
    intent explicit in the API layer.
    """

    def has_permission(self, request, view) -> bool:
        """Return True only for authenticated doctors with a profile."""
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.DOCTOR
            and hasattr(request.user, "doctor_profile")
        )


class MedicalEventViewSet(viewsets.ModelViewSet):
    """Create and retrieve medical events.

    Implements US-01 / FR-11–FR-14:
    - Only doctors may create events.
    - The doctor's specialty must match the event's required specialty.
    - An APPROVED RegistrationRequest can bypass the specialty check (FR-12).
    - is_validated is always False on creation (FR-13).
    - author is always set from the authenticated user (FR-14).
    """

    serializer_class = MedicalEventSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        """Return only events authored by the current doctor.

        Doctors can only see their own events; broader access (supervisor,
        patient read) is handled by future viewsets with separate permissions.
        """
        return MedicalEvent.objects.filter(author__user=self.request.user).select_related(
            "patient", "author", "specialty"
        )

    def perform_create(self, serializer) -> None:
        """Enforce specialty validation before saving the event.

        Args:
            serializer: Validated MedicalEventSerializer instance.

        Raises:
            PermissionDenied: If the doctor's specialty does not match the required
                specialty and no APPROVED RegistrationRequest covers this case.
        """
        doctor = self.request.user.doctor_profile
        specialty = serializer.validated_data["specialty"]
        patient = serializer.validated_data["patient"]
        event_type = serializer.validated_data["event_type"]

        # FR-11: check specialty match
        if doctor.specialty_id != specialty.pk:
            # FR-12: approved cross-specialty request is the only bypass
            has_approved_request = RegistrationRequest.objects.filter(
                requesting_doctor=doctor,
                patient=patient,
                event_type=event_type,
                required_specialty=specialty,
                status=RegistrationRequest.Status.APPROVED,
            ).exists()

            if not has_approved_request:
                raise PermissionDenied(
                    "Your specialty does not match the required specialty for this event type. "
                    "An approved cross-specialty registration request is required."
                )

        # FR-13 + FR-14: author and is_validated are set here, never from the request
        serializer.save(author=doctor, is_validated=False)
