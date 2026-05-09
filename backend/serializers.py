"""DRF serializers for the backend API.

Each serializer is responsible for input validation at the API boundary.
Business-logic checks (specialty matching) live in the viewset, not here.
"""

from __future__ import annotations

import re

from rest_framework import serializers

from backend.models import MedicalEvent


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
