"""Domain models for life_jorney.

Covers the core entities required by US-01 through US-03:
User (with roles), Specialty, DoctorProfile, PatientProfile,
SupervisorProfile, MedicalEvent, RegistrationRequest, and Notification.
"""

from __future__ import annotations

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Manager that uses email as the unique identifier instead of username."""

    def create_user(self, email: str, password: str | None = None, **extra_fields) -> "User":
        """Create and return a regular user with hashed password.

        Args:
            email: Unique email address used for authentication.
            password: Plain-text password (will be hashed).
            **extra_fields: Additional fields forwarded to the User model.

        Returns:
            The newly created User instance.

        Raises:
            ValueError: If email is empty.
        """
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields) -> "User":
        """Create and return a superuser (admin role, staff and superuser flags set).

        Args:
            email: Unique email address.
            password: Plain-text password.
            **extra_fields: Additional fields merged with superuser defaults.

        Returns:
            The newly created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """System user with role-based access control.

    Replaces Django's default username-based auth with email-based auth.
    Role determines which parts of the clinical system the user can access.
    """

    class Role(models.TextChoices):
        PATIENT = "patient", "Patient"
        DOCTOR = "doctor", "Doctor"
        NURSE = "nurse", "Nurse"
        LAB_TECHNICIAN = "lab_technician", "Laboratory Technician"
        IMAGING_PROFESSIONAL = "imaging_professional", "Imaging Professional"
        SUPERVISOR = "supervisor", "Supervisor"
        ADMIN = "admin", "Administrator"

    username = None  # type: ignore[assignment]  # replaced by email
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=Role.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role"]

    objects = UserManager()  # type: ignore[assignment]

    def __str__(self) -> str:
        """Return full name if set, otherwise email, followed by role."""
        return f"{self.get_full_name() or self.email} ({self.role})"


class Specialty(models.Model):
    """Medical specialty assigned to doctors and required by event types.

    Acts as the gate between a doctor's credentials and the events they are
    permitted to record (FR-11).
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "specialties"

    def __str__(self) -> str:
        """Return the specialty name."""
        return self.name


class DoctorProfile(models.Model):
    """Extended profile for users with the Doctor role.

    Separates clinical credentials from the core authentication record
    so audit queries on User remain clean.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, related_name="doctors")
    license_number = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        """Return doctor name and specialty."""
        return f"Dr. {self.user.get_full_name() or self.user.email} ({self.specialty})"


class PatientProfile(models.Model):
    """Extended profile for users with the Patient role."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=5, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        """Return patient's full name or email."""
        return f"Patient: {self.user.get_full_name() or self.user.email}"


class SupervisorProfile(models.Model):
    """Extended profile for users with the Supervisor role.

    Supervisors validate medical events recorded by doctors (US-03 / FR-32–FR-36).
    """

    class Shift(models.TextChoices):
        MORNING = "morning", "Morning"
        AFTERNOON = "afternoon", "Afternoon"
        NIGHT = "night", "Night"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="supervisor_profile")
    supervised_area = models.CharField(max_length=100, blank=True)
    shift = models.CharField(max_length=20, choices=Shift.choices, blank=True)

    def __str__(self) -> str:
        """Return supervisor name and area."""
        return f"Supervisor: {self.user.get_full_name() or self.user.email} ({self.supervised_area})"


class MedicalEvent(models.Model):
    """A clinical event recorded in a patient's history.

    Implements US-01 / FR-11–FR-14. Created with is_validated=False;
    a supervisor must explicitly approve it (US-03) before it appears
    in the patient's validated history.
    """

    class EventType(models.TextChoices):
        CONSULTATION = "consultation", "Consultation"
        DIAGNOSIS = "diagnosis", "Diagnosis"
        VACCINE = "vaccine", "Vaccine"
        PROCEDURE = "procedure", "Procedure"
        FOLLOW_UP = "follow_up", "Follow-up"

    class ValidationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        VALIDATED = "validated", "Validated"
        REJECTED = "rejected", "Rejected"

    patient = models.ForeignKey(PatientProfile, on_delete=models.PROTECT, related_name="medical_events")
    event_type = models.CharField(max_length=30, choices=EventType.choices)
    description = models.TextField()
    icd_code = models.CharField(max_length=10, help_text="ICD-10/11 code for the diagnosis.")
    event_date = models.DateTimeField(help_text="Date and time the clinical event occurred.")
    author = models.ForeignKey(DoctorProfile, on_delete=models.PROTECT, related_name="authored_events")
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        help_text="Specialty required to record this event type.",
    )
    # FR-13: always False on creation; set True only by supervisor action (US-03)
    is_validated = models.BooleanField(default=False)
    # US-03: tracks the full review lifecycle (PENDING → VALIDATED or REJECTED)
    validation_status = models.CharField(
        max_length=20,
        choices=ValidationStatus.choices,
        default=ValidationStatus.PENDING,
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="validated_events",
    )
    validated_at = models.DateTimeField(null=True, blank=True)
    rejection_comment = models.TextField(blank=True)
    # FR-14: author and timestamp recorded automatically
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return event type, patient, and date."""
        return f"{self.get_event_type_display()} — {self.patient} ({self.event_date:%Y-%m-%d})"


class RegistrationRequest(models.Model):
    """Cross-specialty registration request from one doctor to another.

    When a doctor's specialty does not match the required specialty for an event,
    they must create a RegistrationRequest addressed to a doctor of the correct
    specialty (US-02 / FR-12). An event can only bypass the specialty check if
    a matching request with status=APPROVED exists.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    requesting_doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.PROTECT, related_name="sent_requests"
    )
    executing_doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="received_requests",
    )
    patient = models.ForeignKey(PatientProfile, on_delete=models.PROTECT, related_name="registration_requests")
    event_type = models.CharField(max_length=30, choices=MedicalEvent.EventType.choices)
    required_specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return request summary with doctors, specialty, and status."""
        return (
            f"Request {self.pk}: {self.requesting_doctor} → "
            f"{self.required_specialty.name} ({self.status})"
        )


class Notification(models.Model):
    """In-app notification record created when a clinical action requires a user's attention.

    Satisfies FR-16 at the data layer. Actual delivery (email, push) is delegated
    to Celery tasks and will be wired up when the task queue is configured.
    """

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    # TODO(delivery): wire up Celery task here to send email/push when created
    registration_request = models.ForeignKey(
        RegistrationRequest,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return recipient email and read status."""
        return f"Notification → {self.recipient.email} ({'read' if self.is_read else 'unread'})"
