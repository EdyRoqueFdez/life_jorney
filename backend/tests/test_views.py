"""Integration tests for the MedicalEvent API endpoint (US-01 / FR-11–FR-14).

Each test follows the Red-Green-Refactor cycle:  run this file before implementing
the viewset to confirm all tests fail, then implement until they all pass.
"""

from __future__ import annotations

import pytest
from django.urls import reverse

from backend.models import MedicalEvent


MEDICAL_EVENTS_URL = "/api/medical-events/"


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_doctor_matching_specialty_creates_event_returns_201(doctor_client, valid_event_payload):
    """POST with a doctor whose specialty matches the event specialty returns 201."""
    response = doctor_client.post(MEDICAL_EVENTS_URL, valid_event_payload, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_event_created_with_is_validated_false(doctor_client, valid_event_payload):
    """Events created via POST always have is_validated=False regardless of input — FR-13."""
    payload = {**valid_event_payload, "is_validated": True}  # attacker tries to set True
    response = doctor_client.post(MEDICAL_EVENTS_URL, payload, format="json")
    assert response.status_code == 201
    assert response.data["is_validated"] is False


@pytest.mark.django_db
def test_event_author_set_from_authenticated_user(doctor_client, doctor_user, valid_event_payload):
    """POST sets author from the authenticated user, not from the request body — FR-14."""
    response = doctor_client.post(MEDICAL_EVENTS_URL, valid_event_payload, format="json")
    assert response.status_code == 201
    event = MedicalEvent.objects.get(pk=response.data["id"])
    assert event.author == doctor_user.doctor_profile


@pytest.mark.django_db
def test_event_created_at_is_set_automatically(doctor_client, valid_event_payload):
    """POST response includes a non-null created_at timestamp — FR-14."""
    response = doctor_client.post(MEDICAL_EVENTS_URL, valid_event_payload, format="json")
    assert response.status_code == 201
    assert response.data["created_at"] is not None


# ---------------------------------------------------------------------------
# Specialty enforcement (FR-11, FR-12)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_doctor_mismatched_specialty_without_request_returns_403(
    doctor_client, valid_event_payload, neurology
):
    """POST returns 403 when doctor's specialty doesn't match and no approved request exists — FR-12."""
    payload = {**valid_event_payload, "specialty": neurology.pk}
    response = doctor_client.post(MEDICAL_EVENTS_URL, payload, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_doctor_mismatched_specialty_with_approved_request_returns_201(
    doctor_client, valid_event_payload, neurology, approved_cross_specialty_request
):
    """POST returns 201 when specialty mismatches but an APPROVED RegistrationRequest exists — FR-12."""
    payload = {**valid_event_payload, "specialty": neurology.pk}
    response = doctor_client.post(MEDICAL_EVENTS_URL, payload, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_doctor_mismatched_specialty_with_pending_request_returns_403(
    doctor_client, valid_event_payload, neurology, pending_cross_specialty_request
):
    """POST returns 403 when a request exists but is still PENDING — only APPROVED bypasses FR-12."""
    payload = {**valid_event_payload, "specialty": neurology.pk}
    response = doctor_client.post(MEDICAL_EVENTS_URL, payload, format="json")
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# Permission and authentication
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_non_doctor_cannot_create_event_returns_403(non_doctor_client, valid_event_payload):
    """POST returns 403 for authenticated users who are not doctors."""
    response = non_doctor_client.post(MEDICAL_EVENTS_URL, valid_event_payload, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_unauthenticated_cannot_create_event_returns_403(api_client, valid_event_payload):
    """POST returns 403 for unauthenticated requests under SessionAuthentication.

    DRF only returns 401 when the active authenticator sends a WWW-Authenticate
    header (e.g. BasicAuth, JWT). SessionAuthentication does not, so DRF falls
    through to 403. Update this assertion to 401 once JWT auth is wired up.
    """
    response = api_client.post(MEDICAL_EVENTS_URL, valid_event_payload, format="json")
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_missing_icd_code_returns_400(doctor_client, valid_event_payload):
    """POST returns 400 when icd_code is missing from the payload."""
    payload = {k: v for k, v in valid_event_payload.items() if k != "icd_code"}
    response = doctor_client.post(MEDICAL_EVENTS_URL, payload, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_invalid_icd_code_format_returns_400(doctor_client, valid_event_payload):
    """POST returns 400 when icd_code does not follow the ICD-10/11 format."""
    payload = {**valid_event_payload, "icd_code": "NOT-VALID"}
    response = doctor_client.post(MEDICAL_EVENTS_URL, payload, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_missing_description_returns_400(doctor_client, valid_event_payload):
    """POST returns 400 when description is missing."""
    payload = {k: v for k, v in valid_event_payload.items() if k != "description"}
    response = doctor_client.post(MEDICAL_EVENTS_URL, payload, format="json")
    assert response.status_code == 400
