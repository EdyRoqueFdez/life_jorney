"""Shared pytest fixtures for the backend test suite.

All reusable test data lives here so test functions stay focused on assertions,
not on setup boilerplate. Fixtures are scoped to 'function' by default so each
test starts with a clean slate.
"""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from backend.models import DoctorProfile, PatientProfile, RegistrationRequest, Specialty

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    """Return an unauthenticated DRF test client."""
    return APIClient()


# ---------------------------------------------------------------------------
# Specialties
# ---------------------------------------------------------------------------

@pytest.fixture
def cardiology() -> Specialty:
    """Return a Cardiology specialty instance."""
    return Specialty.objects.create(name="Cardiology", description="Heart and circulatory system.")


@pytest.fixture
def neurology(db) -> Specialty:
    """Return a Neurology specialty instance."""
    return Specialty.objects.create(name="Neurology", description="Nervous system disorders.")


# ---------------------------------------------------------------------------
# Users and profiles
# ---------------------------------------------------------------------------

@pytest.fixture
def doctor_user(db, cardiology) -> User:
    """Return a User with role=doctor and a DoctorProfile in Cardiology."""
    user = User.objects.create_user(
        email="doctor@example.com",
        password="Str0ng!Pass",
        role=User.Role.DOCTOR,
        first_name="Ana",
        last_name="García",
    )
    DoctorProfile.objects.create(user=user, specialty=cardiology, license_number="MED-0001")
    return user


@pytest.fixture
def neurology_doctor(db, neurology) -> User:
    """Return a User with role=doctor and a DoctorProfile in Neurology."""
    user = User.objects.create_user(
        email="neuro@example.com",
        password="Str0ng!Pass",
        role=User.Role.DOCTOR,
        first_name="Carlos",
        last_name="López",
    )
    DoctorProfile.objects.create(user=user, specialty=neurology, license_number="MED-0002")
    return user


@pytest.fixture
def patient_user(db) -> User:
    """Return a User with role=patient and a PatientProfile."""
    user = User.objects.create_user(
        email="patient@example.com",
        password="Str0ng!Pass",
        role=User.Role.PATIENT,
        first_name="John",
        last_name="Doe",
    )
    PatientProfile.objects.create(user=user, date_of_birth="1985-06-15")
    return user


@pytest.fixture
def non_doctor_user(db) -> User:
    """Return a nurse User (no doctor profile) to test permission rejection."""
    return User.objects.create_user(
        email="nurse@example.com",
        password="Str0ng!Pass",
        role=User.Role.NURSE,
    )


# ---------------------------------------------------------------------------
# Authenticated clients
# ---------------------------------------------------------------------------

@pytest.fixture
def doctor_client(api_client, doctor_user) -> APIClient:
    """Return an API client authenticated as the cardiology doctor."""
    api_client.force_authenticate(user=doctor_user)
    return api_client


@pytest.fixture
def neurology_doctor_client(api_client, neurology_doctor) -> APIClient:
    """Return an API client authenticated as the neurology doctor."""
    api_client.force_authenticate(user=neurology_doctor)
    return api_client


@pytest.fixture
def non_doctor_client(api_client, non_doctor_user) -> APIClient:
    """Return an API client authenticated as a non-doctor user."""
    api_client.force_authenticate(user=non_doctor_user)
    return api_client


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@pytest.fixture
def valid_event_payload(patient_user, cardiology) -> dict:
    """Return a valid payload for creating a MedicalEvent via the API."""
    return {
        "patient": patient_user.patient_profile.pk,
        "event_type": "consultation",
        "description": "Routine cardiac check-up. Patient reports occasional palpitations.",
        "icd_code": "I49.9",
        "event_date": "2026-05-09T10:00:00Z",
        "specialty": cardiology.pk,
    }


@pytest.fixture
def approved_cross_specialty_request(db, doctor_user, patient_user, neurology) -> RegistrationRequest:
    """Return an APPROVED RegistrationRequest allowing the cardiology doctor to record a neurology event."""
    return RegistrationRequest.objects.create(
        requesting_doctor=doctor_user.doctor_profile,
        patient=patient_user.patient_profile,
        event_type="consultation",
        required_specialty=neurology,
        status=RegistrationRequest.Status.APPROVED,
    )


@pytest.fixture
def pending_cross_specialty_request(db, doctor_user, patient_user, neurology) -> RegistrationRequest:
    """Return a PENDING RegistrationRequest (not yet approved — must not bypass specialty check)."""
    return RegistrationRequest.objects.create(
        requesting_doctor=doctor_user.doctor_profile,
        patient=patient_user.patient_profile,
        event_type="consultation",
        required_specialty=neurology,
        status=RegistrationRequest.Status.PENDING,
    )


# ---------------------------------------------------------------------------
# US-02 fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def pending_request(db, doctor_user, neurology_doctor, patient_user, neurology) -> RegistrationRequest:
    """Return a PENDING RegistrationRequest addressed to the neurology doctor — US-02 base case."""
    return RegistrationRequest.objects.create(
        requesting_doctor=doctor_user.doctor_profile,
        executing_doctor=neurology_doctor.doctor_profile,
        patient=patient_user.patient_profile,
        event_type="consultation",
        required_specialty=neurology,
        status=RegistrationRequest.Status.PENDING,
    )


@pytest.fixture
def valid_request_payload(patient_user, neurology_doctor, neurology) -> dict:
    """Return a valid payload for POST /api/registration-requests/."""
    return {
        "patient": patient_user.patient_profile.pk,
        "executing_doctor": neurology_doctor.doctor_profile.pk,
        "event_type": "consultation",
        "required_specialty": neurology.pk,
    }
