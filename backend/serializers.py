"""DRF serializers for the backend API.

Each serializer is responsible for input validation at the API boundary.
Business-logic checks (specialty matching) live in the viewset, not here.
"""

from __future__ import annotations

import re

from rest_framework import serializers

from backend.models import MedicalEvent, RegistrationRequest


# ICD-10: letter + 2 digits + optional dot + up to 4 alphanumerics  (e.g. I49.9, A00, B20.0)
# ICD-11: alphanumeric stem of 3–5 chars (e.g. BA80, 5A11.0)
_ICD_PATTERN = re.compile(r"^[A-Z][0-9A-Z]{1,4}(\.[0-9A-Z]{1,4})?$")


class MedicalEventSerializer(serializers.ModelSerializer):
    """Serialize a MedicalEvent for creation and retrieval.

    On creation the caller must NOT supply author or is_validated — both are
    set by the viewset. Attempting to override them is silently ignored because
    those fields are read-only.

    Args (write):
        patient: PK of the PatientProfile.
        event_type: One of MedicalEvent.EventType choices.
        description: Narrative description of the clinical event.
        icd_code: ICD-10/11 code for the diagnosis (validated for format).
        event_date: ISO-8601 datetime when the event occurred.
        specialty: PK of the required Specialty for this event type.

    Returns (read):
        All write fields plus id, author (read-only), is_validated (read-only),
        and created_at (read-only).
    """

    class Meta:
        model = MedicalEvent
        fields = [
            "id",
            "patient",
            "event_type",
            "description",
            "icd_code",
            "event_date",
            "specialty",
            "author",
            "is_validated",
            "created_at",
        ]
        read_only_fields = ["author", "is_validated", "created_at"]

    def validate_icd_code(self, value: str) -> str:
        """Validate that the ICD code matches ICD-10/11 format.

        Args:
            value: Raw ICD code string from the request.

        Returns:
            Uppercased, validated ICD code.

        Raises:
            serializers.ValidationError: If the format does not match.
        """
        normalized = value.strip().upper()
        if not _ICD_PATTERN.match(normalized):
            raise serializers.ValidationError(
                "Invalid ICD-10/11 code. Expected format: letter + digits, "
                "optional dot + alphanumerics (e.g. I49.9, A00, BA80)."
            )
        return normalized


class RegistrationRequestSerializer(serializers.ModelSerializer):
    """Serialize a RegistrationRequest for creation and listing.

    On creation, requesting_doctor is injected by the viewset from the
    authenticated user and must not be supplied in the request body.

    Validates that:
    - The executing_doctor holds the required_specialty.
    - The requesting doctor's specialty differs from required_specialty
      (otherwise they should create the event directly via US-01).

    Args (write):
        patient: PK of the PatientProfile.
        executing_doctor: PK of the DoctorProfile who will execute the event.
        event_type: One of MedicalEvent.EventType choices.
        required_specialty: PK of the Specialty needed for the event.

    Returns (read):
        All write fields plus id, requesting_doctor (read-only), status (read-only),
        and created_at (read-only).
    """

    class Meta:
        model = RegistrationRequest
        fields = [
            "id",
            "requesting_doctor",
            "executing_doctor",
            "patient",
            "event_type",
            "required_specialty",
            "status",
            "created_at",
        ]
        read_only_fields = ["requesting_doctor", "status", "created_at"]

    def validate(self, data: dict) -> dict:
        """Cross-field validation for specialty consistency.

        Args:
            data: Deserialized field values.

        Returns:
            Validated data dict.

        Raises:
            serializers.ValidationError: If the executing doctor's specialty
                does not match the required specialty, or if the requesting
                doctor already holds the required specialty.
        """
        executing_doctor = data.get("executing_doctor")
        required_specialty = data.get("required_specialty")

        if executing_doctor and required_specialty:
            if executing_doctor.specialty_id != required_specialty.pk:
                raise serializers.ValidationError(
                    "The executing doctor's specialty does not match the required specialty."
                )

        # Requesting doctor is injected in perform_create; validate here only if present
        requesting_doctor = self.context.get("requesting_doctor")
        if requesting_doctor and required_specialty:
            if requesting_doctor.specialty_id == required_specialty.pk:
                raise serializers.ValidationError(
                    "Your specialty already matches the required specialty. "
                    "Create the medical event directly instead of a cross-specialty request."
                )

        return data


class RespondToRequestSerializer(serializers.Serializer):
    """Validate the action field for the respond endpoint (FR-17).

    Args (write):
        action: Either 'accept' or 'reject'.
    """

    ACTION_CHOICES = ["accept", "reject"]

    action = serializers.ChoiceField(
        choices=ACTION_CHOICES,
        error_messages={"invalid_choice": "action must be 'accept' or 'reject'."},
    )
