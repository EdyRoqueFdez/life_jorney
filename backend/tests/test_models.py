"""Unit tests for domain model defaults and constraints (US-01 / FR-13, FR-14)."""

from __future__ import annotations

import pytest

from backend.models import MedicalEvent, RegistrationRequest


@pytest.mark.django_db
def test_medical_event_is_validated_defaults_to_false(doctor_user, patient_user, cardiology):
    """MedicalEvent.is_validated must be False on creation — FR-13."""
    event = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        description="Test event.",
        icd_code="I49.9",
        event_date="2026-05-09T10:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
    )
    assert event.is_validated is False


@pytest.mark.django_db
def test_medical_event_created_at_set_automatically(doctor_user, patient_user, cardiology):
    """MedicalEvent.created_at must be set automatically on save — FR-14."""
    event = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        description="Test event.",
        icd_code="I49.9",
        event_date="2026-05-09T10:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
    )
    assert event.created_at is not None


@pytest.mark.django_db
def test_registration_request_status_defaults_to_pending(doctor_user, patient_user, neurology):
    """RegistrationRequest.status must default to PENDING on creation."""
    request = RegistrationRequest.objects.create(
        requesting_doctor=doctor_user.doctor_profile,
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        required_specialty=neurology,
    )
    assert request.status == RegistrationRequest.Status.PENDING


@pytest.mark.django_db
def test_specialty_str_returns_name(cardiology):
    """Specialty.__str__ must return the specialty name."""
    assert str(cardiology) == "Cardiology"
