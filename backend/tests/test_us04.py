"""Integration tests for US-04: patient consultation of medical history (RF-06).

Run before implementing the viewset to confirm all tests fail (Red),
then implement until all pass (Green).
"""

from __future__ import annotations

import pytest

from backend.models import MedicalEvent

HISTORY_URL = "/api/patient-history/"


# ---------------------------------------------------------------------------
# RF-06: Patient sees their own validated events — basic access
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_patient_can_list_own_history_returns_200(patient_client, validated_event):
    """GET /api/patient-history/ returns 200 for an authenticated patient."""
    response = patient_client.get(HISTORY_URL)
    assert response.status_code == 200


@pytest.mark.django_db
def test_patient_history_only_returns_validated_events(patient_client, validated_event, pending_event):
    """List includes validated events only; pending events are excluded."""
    response = patient_client.get(HISTORY_URL)
    ids = [e["id"] for e in response.data]
    assert validated_event.pk in ids
    assert pending_event.pk not in ids


@pytest.mark.django_db
def test_patient_history_excludes_other_patients_events(
    patient_client, validated_event, doctor_user, cardiology, db
):
    """Patient A cannot see events belonging to Patient B."""
    from django.contrib.auth import get_user_model
    from backend.models import PatientProfile

    User = get_user_model()
    other_user = User.objects.create_user(
        email="other_patient@example.com",
        password="Str0ng!Pass",
        role=User.Role.PATIENT,
    )
    other_profile = PatientProfile.objects.create(user=other_user, date_of_birth="1990-01-01")
    other_event = MedicalEvent.objects.create(
        patient=other_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        description="Other patient event.",
        icd_code="A00",
        event_date="2026-05-01T08:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
        is_validated=True,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
    )
    response = patient_client.get(HISTORY_URL)
    ids = [e["id"] for e in response.data]
    assert validated_event.pk in ids
    assert other_event.pk not in ids


# ---------------------------------------------------------------------------
# RF-06: Chronological ordering
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_patient_history_ordered_by_event_date_descending(
    patient_client, doctor_user, patient_user, cardiology, db
):
    """Events are returned with the most recent event_date first."""
    older = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        description="Older event.",
        icd_code="I10",
        event_date="2026-01-01T08:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
        is_validated=True,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
    )
    newer = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.DIAGNOSIS,
        description="Newer event.",
        icd_code="I11",
        event_date="2026-05-09T08:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
        is_validated=True,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
    )
    response = patient_client.get(HISTORY_URL)
    ids = [e["id"] for e in response.data]
    assert ids.index(newer.pk) < ids.index(older.pk)


# ---------------------------------------------------------------------------
# RF-06: Filters
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_filter_by_event_type(patient_client, doctor_user, patient_user, cardiology, db):
    """?event_type=consultation returns only consultation events."""
    consultation = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        description="Consultation event.",
        icd_code="I49.9",
        event_date="2026-05-01T09:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
        is_validated=True,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
    )
    vaccine = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.VACCINE,
        description="Vaccine administered.",
        icd_code="Z23",
        event_date="2026-05-02T09:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
        is_validated=True,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
    )
    response = patient_client.get(HISTORY_URL, {"event_type": "consultation"})
    ids = [e["id"] for e in response.data]
    assert consultation.pk in ids
    assert vaccine.pk not in ids


@pytest.mark.django_db
def test_filter_by_specialty(patient_client, doctor_user, patient_user, cardiology, neurology, db):
    """?specialty=<pk> returns only events of that specialty."""
    from backend.models import DoctorProfile
    from django.contrib.auth import get_user_model

    User = get_user_model()
    neuro_user = User.objects.create_user(
        email="neuro2@example.com",
        password="Str0ng!Pass",
        role=User.Role.DOCTOR,
    )
    neuro_profile = DoctorProfile.objects.create(
        user=neuro_user, specialty=neurology, license_number="MED-9001"
    )
    cardio_event = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        description="Cardiology event.",
        icd_code="I10",
        event_date="2026-05-01T09:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
        is_validated=True,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
    )
    neuro_event = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.DIAGNOSIS,
        description="Neurology event.",
        icd_code="G40",
        event_date="2026-05-02T09:00:00Z",
        author=neuro_profile,
        specialty=neurology,
        is_validated=True,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
    )
    response = patient_client.get(HISTORY_URL, {"specialty": cardiology.pk})
    ids = [e["id"] for e in response.data]
    assert cardio_event.pk in ids
    assert neuro_event.pk not in ids


@pytest.mark.django_db
def test_filter_by_date_from(patient_client, doctor_user, patient_user, cardiology, db):
    """?date_from=2026-03-01 excludes events before that date."""
    before = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        description="Before cutoff.",
        icd_code="I10",
        event_date="2026-02-01T08:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
        is_validated=True,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
    )
    after = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        description="After cutoff.",
        icd_code="I11",
        event_date="2026-04-01T08:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
        is_validated=True,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
    )
    response = patient_client.get(HISTORY_URL, {"date_from": "2026-03-01"})
    ids = [e["id"] for e in response.data]
    assert after.pk in ids
    assert before.pk not in ids


@pytest.mark.django_db
def test_filter_by_date_to(patient_client, doctor_user, patient_user, cardiology, db):
    """?date_to=2026-03-31 excludes events after that date."""
    before = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        description="Before cutoff.",
        icd_code="I10",
        event_date="2026-02-01T08:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
        is_validated=True,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
    )
    after = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        description="After cutoff.",
        icd_code="I11",
        event_date="2026-04-01T08:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
        is_validated=True,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
    )
    response = patient_client.get(HISTORY_URL, {"date_to": "2026-03-31"})
    ids = [e["id"] for e in response.data]
    assert before.pk in ids
    assert after.pk not in ids


# ---------------------------------------------------------------------------
# RF-06: Read-only — no write operations
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_patient_cannot_create_event_returns_405(patient_client, valid_event_payload):
    """POST /api/patient-history/ returns 405 — history is read-only."""
    response = patient_client.post(HISTORY_URL, valid_event_payload, format="json")
    assert response.status_code == 405


# ---------------------------------------------------------------------------
# Permission guards
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_doctor_cannot_access_patient_history_returns_403(doctor_client):
    """GET /api/patient-history/ returns 403 for a doctor."""
    response = doctor_client.get(HISTORY_URL)
    assert response.status_code == 403


@pytest.mark.django_db
def test_unauthenticated_cannot_access_patient_history_returns_403(api_client):
    """GET /api/patient-history/ returns 403 for unauthenticated requests."""
    response = api_client.get(HISTORY_URL)
    assert response.status_code == 403
