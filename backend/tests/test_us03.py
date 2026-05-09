"""Integration tests for US-03: supervisor event validation (FR-32–FR-36).

Run before implementing the viewset to confirm all tests fail (Red),
then implement until all pass (Green).
"""

from __future__ import annotations

import pytest

from backend.models import MedicalEvent, Notification

QUEUE_URL = "/api/validation-queue/"


def review_url(pk: int) -> str:
    """Return the review action URL for a given event pk."""
    return f"/api/validation-queue/{pk}/review/"


# ---------------------------------------------------------------------------
# FR-32: Supervisor sees list of pending events
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_supervisor_can_list_pending_events_returns_200(supervisor_client, pending_event):
    """GET /api/validation-queue/ returns 200 for an authenticated supervisor."""
    response = supervisor_client.get(QUEUE_URL)
    assert response.status_code == 200


@pytest.mark.django_db
def test_pending_list_only_includes_pending_events(supervisor_client, pending_event, doctor_user, patient_user, cardiology):
    """GET /api/validation-queue/ excludes already-validated events."""
    validated = MedicalEvent.objects.create(
        patient=patient_user.patient_profile,
        event_type=MedicalEvent.EventType.CONSULTATION,
        description="Already validated event.",
        icd_code="I10",
        event_date="2026-05-09T09:00:00Z",
        author=doctor_user.doctor_profile,
        specialty=cardiology,
        validation_status=MedicalEvent.ValidationStatus.VALIDATED,
        is_validated=True,
    )
    response = supervisor_client.get(QUEUE_URL)
    ids = [e["id"] for e in response.data]
    assert pending_event.pk in ids
    assert validated.pk not in ids


@pytest.mark.django_db
def test_doctor_cannot_access_validation_queue_returns_403(doctor_client):
    """GET /api/validation-queue/ returns 403 for a doctor."""
    response = doctor_client.get(QUEUE_URL)
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# FR-33: Validate event
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_supervisor_can_validate_event_returns_200(supervisor_client, pending_event):
    """POST /review/ with action=validate returns 200."""
    response = supervisor_client.post(review_url(pending_event.pk), {"action": "validate"}, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_validated_event_is_validated_is_true(supervisor_client, pending_event):
    """Validating an event sets is_validated=True on the MedicalEvent — FR-33."""
    supervisor_client.post(review_url(pending_event.pk), {"action": "validate"}, format="json")
    pending_event.refresh_from_db()
    assert pending_event.is_validated is True


@pytest.mark.django_db
def test_validated_event_records_supervisor_and_timestamp(supervisor_client, supervisor_user, pending_event):
    """Validating records the supervisor FK and validated_at timestamp — FR-33, FR-36."""
    supervisor_client.post(review_url(pending_event.pk), {"action": "validate"}, format="json")
    pending_event.refresh_from_db()
    assert pending_event.supervisor == supervisor_user
    assert pending_event.validated_at is not None


@pytest.mark.django_db
def test_validated_event_validation_status_is_validated(supervisor_client, pending_event):
    """Validating sets validation_status=VALIDATED."""
    supervisor_client.post(review_url(pending_event.pk), {"action": "validate"}, format="json")
    pending_event.refresh_from_db()
    assert pending_event.validation_status == MedicalEvent.ValidationStatus.VALIDATED


# ---------------------------------------------------------------------------
# FR-34: Reject event with mandatory comment
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_supervisor_can_reject_event_returns_200(supervisor_client, pending_event):
    """POST /review/ with action=reject and a comment returns 200."""
    response = supervisor_client.post(
        review_url(pending_event.pk),
        {"action": "reject", "comment": "ICD code does not match the described diagnosis."},
        format="json",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_rejected_event_validation_status_is_rejected(supervisor_client, pending_event):
    """Rejecting sets validation_status=REJECTED and is_validated remains False — FR-34."""
    supervisor_client.post(
        review_url(pending_event.pk),
        {"action": "reject", "comment": "Incomplete description."},
        format="json",
    )
    pending_event.refresh_from_db()
    assert pending_event.validation_status == MedicalEvent.ValidationStatus.REJECTED
    assert pending_event.is_validated is False


@pytest.mark.django_db
def test_rejection_without_comment_returns_400(supervisor_client, pending_event):
    """POST /review/ with action=reject but no comment returns 400 — FR-34 mandatory comment."""
    response = supervisor_client.post(review_url(pending_event.pk), {"action": "reject"}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_rejection_stores_comment(supervisor_client, pending_event):
    """Rejection comment is persisted on the MedicalEvent — FR-34."""
    comment = "ICD code does not match the described diagnosis."
    supervisor_client.post(
        review_url(pending_event.pk),
        {"action": "reject", "comment": comment},
        format="json",
    )
    pending_event.refresh_from_db()
    assert pending_event.rejection_comment == comment


# ---------------------------------------------------------------------------
# FR-35: Notify author on rejection
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_notification_created_for_author_on_rejection(supervisor_client, pending_event, doctor_user):
    """Rejecting creates a Notification for the event author — FR-35."""
    supervisor_client.post(
        review_url(pending_event.pk),
        {"action": "reject", "comment": "Needs correction."},
        format="json",
    )
    assert Notification.objects.filter(recipient=doctor_user).exists()


# ---------------------------------------------------------------------------
# Guard: already-reviewed events cannot be reviewed again
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_already_validated_event_cannot_be_reviewed_returns_400(supervisor_client, pending_event):
    """POST /review/ on an already VALIDATED event returns 400."""
    supervisor_client.post(review_url(pending_event.pk), {"action": "validate"}, format="json")
    response = supervisor_client.post(review_url(pending_event.pk), {"action": "validate"}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_already_rejected_event_cannot_be_reviewed_returns_400(supervisor_client, pending_event):
    """POST /review/ on an already REJECTED event returns 400."""
    supervisor_client.post(
        review_url(pending_event.pk),
        {"action": "reject", "comment": "First rejection."},
        format="json",
    )
    response = supervisor_client.post(
        review_url(pending_event.pk),
        {"action": "reject", "comment": "Second rejection attempt."},
        format="json",
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Permission guards
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_doctor_cannot_validate_event_returns_403(doctor_client, pending_event):
    """POST /review/ returns 403 for a doctor."""
    response = doctor_client.post(review_url(pending_event.pk), {"action": "validate"}, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_unauthenticated_cannot_access_queue_returns_403(api_client):
    """GET /api/validation-queue/ returns 403 for unauthenticated requests."""
    response = api_client.get(QUEUE_URL)
    assert response.status_code == 403
