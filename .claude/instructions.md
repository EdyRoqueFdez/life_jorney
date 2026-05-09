# life_jorney — AI Coding Instructions

This file is the authoritative style guide for all code generated in this repository,
whether written by a human developer or an AI agent (Claude Code, Copilot, Cursor, etc.).
Every contributor and every agent **must** follow the mandatory rules below.
Optional recommendations are clearly marked.

---

## Who this file is for

- **AI agents:** treat every rule in the "Mandatory" sections as a hard constraint.
  Do not generate code that violates them, even if the user does not ask explicitly.
- **Human developers:** use this as the reference when writing new code or reviewing AI output.
- **New contributors:** read this before writing your first line of code.

---

## 1. Docstrings — Mandatory

### 1.1 Coverage

Every **module**, **class**, **method**, and **function** must have a docstring.
No exceptions, including:

- Private helpers prefixed with `_`
- `__init__` methods that do non-trivial initialization
- Class-based views, serializers, signals, and Celery tasks (Django/DRF)
- Flutter/Dart: every `class`, `method`, and top-level function

### 1.2 Language

All docstrings must be written in **English**.
Code comments may be English or Spanish, but docstrings are always English.

### 1.3 Content requirements

A docstring must answer two questions:

1. **What does this component do?**
2. **What problem does it solve, or why does it exist?**

Restating the function signature in prose is not a docstring — it is noise.
Explain intent and behavior, not syntax.

### 1.4 Format — Google style (required)

Use **Google-style docstrings** for Python. Include the sections below when they apply:

| Section | When to include |
|---------|-----------------|
| One-line summary | Always — first line, ends with a period |
| Extended description | When the one-liner is not enough to convey intent |
| `Args` | When the function has parameters |
| `Returns` | When the function returns a meaningful value |
| `Raises` | When the function raises documented exceptions |
| `Example` | When usage is not obvious from the signature |

For Dart/Flutter, use `///` doc comments following the same structural intent
(summary line, blank line, then detail paragraphs or parameter descriptions).

---

## 2. Docstring examples

### Python — correct

```python
def compute_medication_overlap(
    active_medications: list[str],
    new_medication: str,
) -> list[str]:
    """Return the known interactions between a new medication and an active list.

    Queries the local ATC interaction matrix to identify drug pairs that carry
    a documented interaction risk. Returns an empty list when no interactions
    are found, never raises for missing entries.

    Args:
        active_medications: ATC codes currently prescribed to the patient.
        new_medication: ATC code of the medication being evaluated.

    Returns:
        A list of ATC codes from ``active_medications`` that interact with
        ``new_medication``. Empty if no interactions are found.

    Raises:
        ValueError: If ``new_medication`` is not a valid ATC code string.

    Example:
        >>> compute_medication_overlap(["N02BE01", "B01AC06"], "N02BE01")
        []
        >>> compute_medication_overlap(["B01AC06", "N02AA01"], "N02BE01")
        ["N02AA01"]
    """
```

### Python — incorrect

```python
def compute_medication_overlap(active_medications, new_medication):
    """Compute medication overlap."""  # ❌ restates the name, explains nothing
```

```python
def compute_medication_overlap(active_medications, new_medication):
    # Takes a list of meds and a new med and returns overlaps  # ❌ comment, not docstring
```

### Django model — correct

```python
class AuditEvent(models.Model):
    """Immutable record of every access or mutation of patient health data.

    Written on every read, write, or delete that touches a ``MedicalRecord``.
    Rows in this table must never be updated or deleted — integrity is enforced
    at the database level with a trigger. Used by the compliance module to
    produce GDPR and HIPAA audit reports.
    """
```

### DRF serializer — correct

```python
class MedicalRecordSerializer(serializers.ModelSerializer):
    """Serialize a patient's medical record for the REST API.

    Excludes fields the requesting user is not consented to see, based on
    the active ``ConsentGrant`` rows for the patient–provider pair. Callers
    should never bypass this serializer to access raw model data in a view.
    """
```

### Dart/Flutter — correct

```dart
/// Returns the offline-cached records for [patientId] stored in SQLCipher.
///
/// Reads from the local encrypted SQLite database. Falls back to an empty
/// list — never throws — when the patient has no cached records or when the
/// cache has been invalidated after a remote sync. Call [syncRecords] first
/// if up-to-date data is required.
Future<List<MedicalRecord>> getCachedRecords(String patientId) async { ... }
```

### Dart/Flutter — incorrect

```dart
// Gets cached records  // ❌ plain comment, not a doc comment
Future<List<MedicalRecord>> getCachedRecords(String patientId) async { ... }

/// Gets cached records for patientId.  // ❌ restates the signature
Future<List<MedicalRecord>> getCachedRecords(String patientId) async { ... }
```

---

## 3. Inline comments — Mandatory

Write inline comments **only** when the WHY is non-obvious:

- A hidden constraint or external requirement
- A workaround for a known library bug (include the issue URL)
- An invariant that would surprise a reader
- A regulatory or compliance reason for a specific choice

Do **not** write comments that describe what the code does — well-named identifiers
already do that.

```python
# HIPAA §164.312(b) requires every access to PHI to be logged, including reads.
audit_log.record(user=request.user, record=record, action="read")

# SQLCipher key derivation is intentionally slow (PBKDF2, 256k iterations).
# Do not replace with a faster KDF without a security review.
db_key = derive_key(passphrase, salt, iterations=256_000)
```

---

## 4. Naming conventions — Mandatory

| Context | Rule |
|---------|------|
| All identifiers (variables, functions, classes) | **English** |
| Python variables and functions | `snake_case` |
| Python classes | `PascalCase` |
| Python constants | `UPPER_SNAKE_CASE` |
| Dart/Flutter variables and functions | `camelCase` |
| Dart/Flutter classes | `PascalCase` |
| React/TypeScript components | `PascalCase` |
| React/TypeScript hooks | `useCamelCase` |
| TypeScript interfaces | `PascalCase`, no `I` prefix |
| Database columns and model fields | `snake_case` |
| URL path segments | `kebab-case` |

Avoid abbreviations unless the term is a well-known domain acronym
(e.g., `fhir`, `phi`, `atc`, `icd`).

---

## 5. Type annotations — Mandatory

### Python

All function signatures must include type hints for parameters and return values.
Use `from __future__ import annotations` at module level to enable forward references.

```python
# correct
def find_patient(patient_id: uuid.UUID, include_archived: bool = False) -> Patient | None:

# incorrect — no hints
def find_patient(patient_id, include_archived=False):
```

For complex types, define a `TypeAlias` or use `typing.TypedDict` rather than
inlining long unions.

### TypeScript

Explicit types are required on all function parameters and return values.
`any` is forbidden. Use `unknown` + narrowing when the type is genuinely unknown.

### Dart

All public API surfaces must have explicit types. Avoid `dynamic` except when
interacting with JSON decoding, and narrow the type immediately after.

---

## 6. Test-Driven Development (TDD) — Mandatory

All production code in this repository must be written following the **Red → Green → Refactor** cycle.
No production code may be written without a failing test that justifies it.

### 6.1 The cycle

1. **Red** — write a failing test that describes exactly the behavior you want. Run it and confirm it fails.
2. **Green** — write the minimum code needed to make the test pass. Nothing more.
3. **Refactor** — clean up duplication or design issues without changing behavior. Run tests again.

### 6.2 Test structure

```
backend/
└── tests/
    ├── __init__.py
    ├── conftest.py       ← pytest fixtures (users, clients, seed data)
    ├── test_models.py    ← unit tests for model methods and constraints
    ├── test_serializers.py ← serializer validation logic
    └── test_views.py     ← full API integration tests (request → response)
```

- Use **pytest** and **pytest-django**. Never Django's built-in `unittest` runner.
- Every test function must have a **one-line docstring** stating what it asserts and why.

### 6.3 Naming convention

```
test_<subject>_<condition>_<expected_result>

# examples
test_medical_event_matching_specialty_returns_201
test_medical_event_mismatched_specialty_without_request_returns_403
test_medical_event_is_validated_is_false_on_creation
```

### 6.4 Coverage rules

- 100 % of business-logic methods (model methods, validators, service functions) — unit tests.
- Every API endpoint — integration tests covering: happy path, permission denied, and at least one validation error.

### 6.5 Do not mock the database

Use a real test database. pytest-django creates and tears it down automatically.
Mocking the database has historically caused production regressions in this domain.

### 6.6 Fixture conventions

Define all reusable fixtures in `backend/tests/conftest.py`.
Never create test data inside a test function body — use fixtures so it is explicit and reusable.

### 6.7 For AI agents

When asked to implement any feature:

1. Write all tests **first** — confirm they fail before writing any implementation code.
2. Write the minimum implementation to make them pass.
3. Do not mark a task as done until `uv run pytest` exits with code 0.
4. After any `uv add` or `uv remove`, update `requirements.txt` in the same step.

---

## 7. Dependency management — Mandatory


### 6.1 Always update requirements.txt

Every time a package is installed or removed, `requirements.txt` must be updated
in the same commit. No exceptions — a package that is in the venv but not in
`requirements.txt` does not exist for other contributors.

**Workflow for adding a dependency:**

```bash
# 1. Install with uv
uv add <package>

# 2. Immediately update requirements.txt
uv pip freeze > requirements.txt   # then review the diff

# 3. Commit both changes together
git add requirements.txt pyproject.toml uv.lock
git commit -m "chore(deps): add <package>"
```

**For AI agents:** after any `uv add` or `uv remove` call, always update
`requirements.txt` before the task is considered done. Do not wait for the user
to ask.

### 6.2 requirements.txt conventions

- Group packages by role with a `# comment` header (Core framework, Database,
  Configuration, Dev/test, etc.).
- Pin exact versions (`package==x.y.z`) for all direct and indirect dependencies
  so installs are fully reproducible.
- Keep indirect Django dependencies (asgiref, sqlparse) at the bottom under
  `# Django internals`.

---

## 8. Commit messages — Recommended

Follow **Conventional Commits** (`https://www.conventionalcommits.org`).

```
<type>(<scope>): <short summary in imperative mood>

[optional body — explain why, not what]

[optional footer — breaking changes, issue refs]
```

| Type | Use for |
|------|---------|
| `feat` | New feature visible to users |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change with no behavior change |
| `test` | Adding or fixing tests |
| `chore` | Build, CI, dependency updates |
| `security` | Security-related change (use sparingly, be precise) |

Scopes for this project: `api`, `frontend`, `mobile`, `auth`, `audit`, `consent`,
`fhir`, `storage`, `infra`, `docs`.

```
# correct
feat(consent): add time-limited consent grants for research use

# incorrect
Fixed stuff
update
WIP
```

---

## 9. Security and privacy rules — Mandatory

These rules exist because life_jorney handles Protected Health Information (PHI).
Violating them is not a style issue — it is a data safety issue.

- **Never log PHI.** Patient names, diagnoses, medications, and identifiers must
  never appear in application logs, error messages, or Sentry/monitoring payloads.
- **Never hardcode secrets.** API keys, database URLs, encryption keys, and passwords
  must come from environment variables or a secrets manager — never from source code.
- **Never commit real patient data.** All test fixtures, seeds, and example data
  must be synthetic. If you accidentally include real data, treat it as a security
  incident and follow `SECURITY.md`.
- **Use parameterized queries.** Raw string interpolation into SQL is forbidden.
  Use the ORM or explicit parameterized queries.
- **Validate at boundaries.** Sanitize and validate all input at the API boundary
  (serializer layer for DRF). Do not re-validate inside service or model layers
  unless there is a documented reason.

---

## 10. Testing expectations — Recommended

- Unit tests cover the function contract described in the docstring.
- Integration tests cover the complete request/response cycle for API endpoints,
  including permission and consent checks.
- Do not mock the database in integration tests — use a real test database.
  (Mocks have caused prod regressions in this domain before.)
- Test file names mirror the module: `patients/services.py` → `tests/patients/test_services.py`.
- Every test function must have a one-line docstring stating what it asserts and why.

---

## 10. Clinical domain rules — Mandatory

These rules exist because life_jorney handles Protected Health Information (PHI) and
clinical decisions that directly affect patient safety. They apply to every model field,
serializer, viewset, and test that touches medical data.

### 10.1 Clinical code validation

Every field that stores a clinical code must have format validation — at the serializer
layer for API input, and at the model level via a validator for programmatic creation.
Never store a code without validating its format first.

| Standard | Format rule | Example |
|----------|-------------|---------|
| ICD-10/11 | `^[A-Z][0-9A-Z]{1,4}(\.[0-9A-Z]{1,4})?$` | `I49.9`, `A00`, `BA80` |
| LOINC | `^\d{1,5}-\d$` | `2160-0`, `14749-6` |
| SNOMED CT | Numeric SCTID, 6–18 digits | `73211009` |
| ATC | `^[A-Z][0-9]{2}[A-Z]{2}[0-9]{2}$` | `N02BE01` |

When a standard is ambiguous or the code cannot be validated automatically,
flag it with a comment and add it to the review backlog — never silently accept it.

### 10.2 The `is_validated` flag is inviolable

- `is_validated` (or `validate` in the data model) is **always `False` on creation**.
- No serializer may expose `is_validated` as a writable field.
- Only a supervisor action (US-03) may set it to `True` via its own dedicated endpoint.
- Any code that allows a client to set `is_validated=True` on creation is a patient
  safety defect, not just a bug.

### 10.3 PHI exposure check before every new endpoint

Before implementing any new API endpoint that returns patient data, verify:

1. Is there an active `ConsentGrant` for the requesting user → patient pair?
2. If not, is this a documented break-glass scenario (US-12) with a mandatory justification?
3. Does the response include only the minimum data necessary (data minimisation)?

If none of the above applies, the endpoint must not return patient data. Flag it.

### 10.4 Proactive patient safety checks

When implementing models or logic related to:
- Medications → always ask whether a drug-allergy interaction check is wired up (US-13).
- Supplies / vaccines → always verify the nurse's patient assignment scope (US-09 / FR-20).
- Laboratory results → always verify a prior medical order exists before accepting the result (US-10 / FR-25).
- Imaging studies → always verify a prior medical order exists (US-11 / FR-29).

If the check is not yet implemented, add a `# TODO(safety): ...` comment and open it
as a known gap — never silently omit it.

### 10.5 Specialty enforcement is not optional

Every endpoint that creates a clinical event must run the specialty check (FR-11 / FR-12).
Never bypass it with a boolean flag, an admin override, or a shortcut for testing.
Use an `APPROVED` `RegistrationRequest` as the only legitimate bypass (US-02).

### 10.6 Grounding new requirements in existing US/FR

When proposing or implementing a new feature:
- Link it explicitly to an existing US (US-01…US-15) or FR (FR-01…FR-51).
- If it does not fit any existing story, document the gap and propose a new US/FR
  in `software_engineering.md` before implementing.
- Never implement undocumented clinical behaviour — it cannot be clinically reviewed.

---

## 11. How AI agents should apply these rules

When generating code for this repository:

1. Always produce docstrings on every new class, method, and function — even when
   the user does not ask for documentation.
2. Apply type hints to every signature unless the language does not support them.
3. Refuse to generate code that logs PHI or interpolates variables into SQL strings.
4. If asked to write an example or seed file, use clearly synthetic data
   (e.g., `"John Doe"`, `"1970-01-01"`, fictional MRN values).
5. Flag any user request that would introduce a pattern prohibited in Section 7,
   explain the risk, and offer a compliant alternative.
6. When modifying an existing function that lacks a docstring, add one as part of
   the change — do not leave undocumented code behind.

---

*Last updated: 2026-05-09. Review before every major release.*
