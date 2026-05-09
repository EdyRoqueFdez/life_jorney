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

## 6. Commit messages — Recommended

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

## 7. Security and privacy rules — Mandatory

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

## 8. Testing expectations — Recommended

- Unit tests cover the function contract described in the docstring.
- Integration tests cover the complete request/response cycle for API endpoints,
  including permission and consent checks.
- Do not mock the database in integration tests — use a real test database.
  (Mocks have caused prod regressions in this domain before.)
- Test file names mirror the module: `patients/services.py` → `tests/patients/test_services.py`.
- Every test function must have a one-line docstring stating what it asserts and why.

---

## 9. How AI agents should apply these rules

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
