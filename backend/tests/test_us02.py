"""Integration tests for US-02: cross-specialty registration requests (FR-15, FR-16, FR-17).

Run before implementing the viewset to confirm all tests fail (Red),
then implement until all pass (Green).
"""

from __future__ import annotations

import pytest

from backend.models import RegistrationRequest

REQUESTS_URL = "/api/registration-requests/"


def respond_url(pk: int) -> str:
    """Return the respond action URL for a given request pk."""
    return f"/api/registration-requests/{pk}/respond/"


# ---------------------------------------------------------------------------
# FR-15: Create a cross-specialty registration request
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_requesting_doctor_can_create_request_returns_201(doctor_client, valid_request_payload):
    """POST /api/registration-requests/ by a doctor with a valid payload returns 201."""
    response = doctor_client.post(REQUESTS_URL, valid_request_payload, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_new_request_status_is_pending(doctor_client, valid_request_payload):
    """A newly created RegistrationRequest must have status=PENDING — FR-15."""
    response = doctor_client.post(REQUESTS_URL, valid_request_payload, format="json")
    assert response.status_code == 201
    assert response.data["status"] == RegistrationRequest.Status.PENDING


@pytest.mark.django_db
def test_requesting_doctor_set_from_authenticated_user(doctor_client, doctor_user, valid_request_payload):
    """requesting_doctor is always taken from the authenticated user, never from the payload."""
    response = doctor_client.post(REQUESTS_URL, valid_request_payload, format="json")
    assert response.status_code == 201
    request_obj = RegistrationRequest.objects.get(pk=response.data["id"])
    assert request_obj.requesting_doctor == doctor_user.doctor_profile


@pytest.mark.django_db
def test_doctor_cannot_request_own_specialty_returns_400(doctor_client, patient_user, cardiology, doctor_user):
    """POST returns 400 when the required_specialty matches the requesting doctor's specialty.

    If the specialty already matches, the doctor should create the event directly (US-01),
    not create a cross-specialty request.
    """
    payload = {
        "patient": patient_user.patient_profile.pk,
        "executing_doctor": doctor_user.doctor_profile.pk,
        "event_type": "consultation",
        "required_specialty": cardiology.pk,  # same as doctor_user's specialty
    }
    response = doctor_client.post(REQUESTS_URL, payload, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_executing_doctor_must_have_required_specialty_returns_400(
    doctor_client, patient_user, neurology, doctor_user
):
    """POST returns 400 when the executing_doctor's specialty does not match required_specialty."""
    payload = {
        "patient": patient_user.patient_profile.pk,
        "executing_doctor": doctor_user.doctor_profile.pk,  # cardiology doctor, not neurology
        "event_type": "consultation",
        "required_specialty": neurology.pk,
    }
    response = doctor_client.post(REQUESTS_URL, payload, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_non_doctor_cannot_create_request_returns_403(non_doctor_client, valid_request_payload):
    """POST returns 403 for authenticated non-doctor users."""
    response = non_doctor_client.post(REQUESTS_URL, valid_request_payload, format="json")
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# FR-17: Accept or reject a registration request
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_executing_doctor_can_accept_request_returns_200(neurology_doctor_client, pending_request):
    """POST /respond/ with action=accept by the executing doctor returns 200."""
    response = neurology_doctor_client.post(respond_url(pending_request.pk), {"action": "accept"}, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_accepted_request_status_becomes_approved(neurology_doctor_client, pending_request):
    """Accepting a request sets status=APPROVED on the RegistrationRequest — FR-17."""
    neurology_doctor_client.post(respond_url(pending_request.pk), {"action": "accept"}, format="json")
    pending_request.refresh_from_db()
    assert pending_request.status == RegistrationRequest.Status.APPROVED


@pytest.mark.django_db
def test_executing_doctor_can_reject_request_returns_200(neurology_doctor_client, pending_request):
    """POST /respond/ with action=reject by the executing doctor returns 200."""
    response = neurology_doctor_client.post(respond_url(pending_request.pk), {"action": "reject"}, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_rejected_request_status_becomes_rejected(neurology_doctor_client, pending_request):
    """Rejecting a request sets status=REJECTED on the RegistrationRequest — FR-17."""
    neurology_doctor_client.post(respond_url(pending_request.pk), {"action": "reject"}, format="json")
    pending_request.refresh_from_db()
    assert pending_request.status == RegistrationRequest.Status.REJECTED


@pytest.mark.django_db
def test_requesting_doctor_cannot_respond_to_own_request_returns_403(doctor_client, pending_request):
    """The requesting doctor cannot accept or reject their own request."""
    response = doctor_client.post(respond_url(pending_request.pk), {"action": "accept"}, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_unrelated_doctor_cannot_respond_returns_404(api_client, pending_request, db, neurology):
    """A doctor unrelated to the request receives 404, not 403.

    The queryset already hides requests the doctor has no relation to, so the
    resource does not exist from their perspective. 404 is more secure than 403
    because it does not reveal that the request exists at all.
    """
    from django.contrib.auth import get_user_model
    from backend.models import DoctorProfile
    User = get_user_model()
    other = User.objects.create_user(email="other@example.com", password="Str0ng!Pass", role=User.Role.DOCTOR)
    DoctorProfile.objects.create(user=other, specialty=neurology, license_number="MED-0099")
    api_client.force_authenticate(user=other)
    response = api_client.post(respond_url(pending_request.pk), {"action": "accept"}, format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_invalid_action_returns_400(neurology_doctor_client, pending_request):
    """POST /respond/ with an unknown action value returns 400."""
    response = neurology_doctor_client.post(respond_url(pending_request.pk), {"action": "maybe"}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_already_resolved_request_cannot_be_responded_again_returns_400(
    neurology_doctor_client, pending_request
):
    """POST /respond/ on an already APPROVED or REJECTED request returns 400."""
    neurology_doctor_client.post(respond_url(pending_request.pk), {"action": "accept"}, format="json")
    response = neurology_doctor_client.post(respond_url(pending_request.pk), {"action": "reject"}, format="json")
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# FR-16: Notification created on request creation
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_notification_created_for_executing_doctor_on_request_creation(
    doctor_client, valid_request_payload, neurology_doctor
):
    """Creating a request generates a Notification record for the executing doctor — FR-16."""
    from backend.models import Notification
    doctor_client.post(REQUESTS_URL, valid_request_payload, format="json")
    assert Notification.objects.filter(recipient=neurology_doctor).exists()


# ---------------------------------------------------------------------------
# Queryset visibility
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_requesting_doctor_can_list_their_sent_requests(doctor_client, pending_request):
    """GET /api/registration-requests/ returns requests sent by the authenticated doctor."""
    response = doctor_client.get(REQUESTS_URL)
    assert response.status_code == 200
    assert any(r["id"] == pending_request.pk for r in response.data)


@pytest.mark.django_db
def test_executing_doctor_can_list_their_received_requests(neurology_doctor_client, pending_request):
    """GET /api/registration-requests/ returns requests directed to the authenticated doctor."""
    response = neurology_doctor_client.get(REQUESTS_URL)
    assert response.status_code == 200
    assert any(r["id"] == pending_request.pk for r in response.data)
