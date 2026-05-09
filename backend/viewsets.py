"""DRF ViewSets for the backend API.

Business logic that enforces clinical rules (specialty matching, FR-11/FR-12)
lives in perform_create so it runs on every POST regardless of how the view
is called.
"""

from __future__ import annotations

from django.db.models import Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from backend.models import MedicalEvent, Notification, RegistrationRequest, User
from backend.serializers import (
    MedicalEventSerializer,
    RegistrationRequestSerializer,
    RespondToRequestSerializer,
    ReviewEventSerializer,
    ValidationQueueSerializer,
)


class IsSupervisor(BasePermission):
    """Allow access only to authenticated users with role=supervisor and an existing SupervisorProfile."""

    def has_permission(self, request, view) -> bool:
        """Return True only for authenticated supervisors with a profile."""
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.SUPERVISOR
            and hasattr(request.user, "supervisor_profile")
        )


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


class RegistrationRequestViewSet(viewsets.ModelViewSet):
    """Create, list, and respond to cross-specialty registration requests.

    Implements US-02 / FR-15–FR-17:
    - Only doctors may create or respond to requests.
    - Requesting doctor's specialty must differ from the required specialty.
    - Executing doctor must hold the required specialty.
    - Only the designated executing doctor can accept or reject.
    - A Notification is created for the executing doctor on request creation (FR-16).
    """

    serializer_class = RegistrationRequestSerializer
    permission_classes = [IsAuthenticated, IsDoctor]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        """Return requests sent by or addressed to the authenticated doctor.

        Doctors see their own sent requests AND requests directed to them,
        so both parties have visibility into the workflow.
        """
        doctor = self.request.user.doctor_profile
        return RegistrationRequest.objects.filter(
            Q(requesting_doctor=doctor) | Q(executing_doctor=doctor)
        ).select_related("requesting_doctor", "executing_doctor", "patient", "required_specialty")

    def get_serializer_context(self):
        """Inject the requesting doctor into serializer context for cross-field validation."""
        context = super().get_serializer_context()
        if self.request.user.is_authenticated and hasattr(self.request.user, "doctor_profile"):
            context["requesting_doctor"] = self.request.user.doctor_profile
        return context

    def perform_create(self, serializer) -> None:
        """Save the request and create a notification for the executing doctor.

        Args:
            serializer: Validated RegistrationRequestSerializer instance.
        """
        doctor = self.request.user.doctor_profile
        instance = serializer.save(requesting_doctor=doctor)

        # FR-16: notify the executing doctor at the data layer
        # TODO(delivery): trigger Celery email task here once task queue is configured
        if instance.executing_doctor:
            Notification.objects.create(
                recipient=instance.executing_doctor.user,
                message=(
                    f"Dr. {doctor.user.get_full_name() or doctor.user.email} has requested "
                    f"that you record a '{instance.get_event_type_display()}' event "
                    f"(specialty: {instance.required_specialty.name}) for a patient."
                ),
                registration_request=instance,
            )

    @action(detail=True, methods=["post"], url_path="respond")
    def respond(self, request, pk=None) -> Response:
        """Accept or reject a pending registration request.

        Only the designated executing_doctor may respond. Requests that are
        already APPROVED or REJECTED cannot be re-responded.

        Args:
            request: DRF request with body {"action": "accept" | "reject"}.
            pk: Primary key of the RegistrationRequest.

        Returns:
            200 with updated request data on success.
            400 if the action is invalid or the request is already resolved.
            403 if the caller is not the executing doctor.
        """
        registration_request = self.get_object()
        doctor = request.user.doctor_profile

        if registration_request.executing_doctor != doctor:
            raise PermissionDenied("Only the designated executing doctor can respond to this request.")

        if registration_request.status != RegistrationRequest.Status.PENDING:
            return Response(
                {"detail": "This request has already been resolved."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RespondToRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action_value = serializer.validated_data["action"]
        if action_value == "accept":
            registration_request.status = RegistrationRequest.Status.APPROVED
        else:
            registration_request.status = RegistrationRequest.Status.REJECTED
        registration_request.save()

        return Response(
            RegistrationRequestSerializer(registration_request).data,
            status=status.HTTP_200_OK,
        )


class ValidationQueueViewSet(viewsets.ReadOnlyModelViewSet):
    """List pending medical events and allow supervisors to validate or reject them.

    Implements US-03 / FR-32–FR-36:
    - Only supervisors may access this viewset.
    - List returns only events with validation_status=PENDING (FR-32).
    - review action: validate → is_validated=True, validation_status=VALIDATED (FR-33).
    - review action: reject → validation_status=REJECTED, comment stored (FR-34).
    - Rejection creates a Notification for the event author (FR-35).
    - supervisor FK and validated_at timestamp recorded on review (FR-36).
    - Already-reviewed events cannot be reviewed again (guard).
    """

    serializer_class = ValidationQueueSerializer
    permission_classes = [IsAuthenticated, IsSupervisor]

    def get_queryset(self):
        """Return pending events for the list, all events for detail/review actions.

        The list endpoint only exposes PENDING events (FR-32). The review action
        must be able to fetch any event so it can return 400 instead of 404 when
        an already-reviewed event is submitted again.
        """
        qs = MedicalEvent.objects.select_related("patient", "author", "specialty")
        if self.action == "list":
            return qs.filter(validation_status=MedicalEvent.ValidationStatus.PENDING)
        return qs

    @action(detail=True, methods=["post"], url_path="review")
    def review(self, request, pk=None) -> Response:
        """Validate or reject a pending medical event.

        Args:
            request: DRF request with body {"action": "validate" | "reject", "comment": "..."}.
            pk: Primary key of the MedicalEvent.

        Returns:
            200 with updated event data on success.
            400 if the event is already reviewed or action/comment validation fails.
        """
        event = self.get_object()

        if event.validation_status != MedicalEvent.ValidationStatus.PENDING:
            return Response(
                {"detail": "This event has already been reviewed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ReviewEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action_value = serializer.validated_data["action"]
        comment = serializer.validated_data.get("comment", "")
        supervisor = request.user

        if action_value == "validate":
            event.is_validated = True
            event.validation_status = MedicalEvent.ValidationStatus.VALIDATED
            event.supervisor = supervisor
            event.validated_at = timezone.now()
        else:
            event.validation_status = MedicalEvent.ValidationStatus.REJECTED
            event.rejection_comment = comment
            event.supervisor = supervisor
            event.validated_at = timezone.now()
            # FR-35: notify the event author of the rejection
            Notification.objects.create(
                recipient=event.author.user,
                message=(
                    f"Your medical event (ID {event.pk}) was rejected by "
                    f"{supervisor.get_full_name() or supervisor.email}. "
                    f"Reason: {comment}"
                ),
            )

        event.save()
        return Response(ValidationQueueSerializer(event).data, status=status.HTTP_200_OK)

