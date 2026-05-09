# Contributing to life_jorney

Thank you for your interest in contributing to life_jorney. This project exists because a global, secure, and unified medical history platform should be a public good — not a product. Every contribution, whether a line of code, a clinical review, a translation, or a bug report, brings that vision one step closer to reality.

life_jorney is a non-profit, open-source project. There is no corporate agenda here. The people who build it are the people who believe that patients deserve ownership of their own health data, and that software can be a genuine act of care.

---

## Table of Contents

1. [Before You Start](#before-you-start)
2. [Types of Contributions](#types-of-contributions)
3. [How to Report a Bug](#how-to-report-a-bug)
4. [How to Request a Feature](#how-to-request-a-feature)
5. [Development Workflow](#development-workflow)
6. [Code Standards](#code-standards)
7. [Medical and Clinical Contributions](#medical-and-clinical-contributions)
8. [Security Vulnerabilities](#security-vulnerabilities)
9. [Recognition](#recognition)
10. [Questions](#questions)

---

## Before You Start

### Read the engineering document

life_jorney is built on a detailed software engineering specification. Before contributing anything beyond a small bug fix, read `software_engineering.md` in the repository root. It contains the product vision, user stories, functional and non-functional requirements, architecture decisions, clinical standards, and the privacy-by-design model.

Contributing without this context risks duplicating existing decisions or introducing changes that conflict with the architecture. The document is a living reference, not a finished artifact — reading it also gives you the opportunity to improve it.

### Open a Discussion before large changes

If you want to add a new feature, refactor a significant component, change a data model, or propose a new clinical standard integration, open a GitHub Discussion before writing any code. Large pull requests that arrive without prior discussion are very likely to be declined or delayed, not because the idea is bad, but because the project needs to evaluate scope, compliance implications, and architectural fit before implementation begins.

This is especially important for anything that touches:
- Patient data models or storage
- Authentication, authorization, or consent flows
- Clinical coding (ICD, LOINC, SNOMED CT, ATC)
- FHIR resource structures
- GDPR or HIPAA compliance mechanisms

Small bug fixes, documentation corrections, and test additions do not require prior discussion.

---

## Types of Contributions

| Area | What is needed | Technical requirement |
|---|---|---|
| Backend development | Django 5 / DRF API endpoints, Celery tasks, data models, FHIR integration | Python, Django, PostgreSQL, Redis |
| Frontend development | React 18 + TypeScript web application, UI components, state management | React, TypeScript, REST/FHIR APIs |
| Mobile development | Flutter 3 cross-platform app for Android and iOS | Dart, Flutter |
| UI/UX design | Wireframes, component design, accessibility review, design system | Figma or equivalent; no code required |
| Medical/clinical expertise | Clinical workflow review, terminology validation, ICD/LOINC/SNOMED mapping, patient safety | Medical or healthcare background; no code required |
| Security research | Vulnerability research, threat modeling, penetration testing, compliance review | Security; see the dedicated section below |
| Documentation | User guides, API documentation, architectural decision records, translations of technical docs | Clear writing; some technical context helpful |
| Translation | Localizing the UI and documentation into additional languages | Bilingual fluency; no code required |
| QA and testing | Writing test cases, exploratory testing, reporting bugs, reviewing test coverage | Varies; some areas require no coding |
| Community | Answering questions in Discussions, reviewing issues, mentoring new contributors | Patience and familiarity with the project |

---

## How to Report a Bug

Use the **Bug Report** issue template on GitHub. Do not open a blank issue for bugs — the template exists to ensure every report contains the information needed to reproduce and fix the problem.

A good bug report includes:

- **Environment:** operating system, browser or device, and the version of the application where you observed the issue.
- **Steps to reproduce:** a numbered list of exact steps, starting from a known state. Assume the reader has never seen this bug before.
- **Expected behavior:** what should have happened.
- **Actual behavior:** what actually happened, including any error messages, stack traces, or screenshots.
- **Severity assessment:** does this affect patient data integrity, security, or clinical accuracy? If yes, flag it clearly.

If the bug involves patient data exposure, authentication bypass, or any potential security implication, do not open a public issue. Follow the process described in the [Security Vulnerabilities](#security-vulnerabilities) section instead.

---

## How to Request a Feature

Feature requests start in **GitHub Discussions**, not in issues. Open a discussion in the "Ideas" category and describe:

- The problem you are trying to solve (not the solution you have in mind).
- Who benefits — which type of user (patient, healthcare professional, healthcare center) is affected.
- Whether this relates to an existing user story in `software_engineering.md`.
- Any clinical, regulatory, or privacy considerations you are aware of.

If the discussion reaches consensus and the feature aligns with the project roadmap, a maintainer will convert it into a tracked issue and it can enter the development workflow.

Skipping the discussion and opening a feature issue directly will result in the issue being closed with a redirect to Discussions.

---

## Development Workflow

### 1. Fork and clone

Fork the repository on GitHub, then clone your fork locally:

```
git clone https://github.com/your-github-username/life_jorney.git
cd life_jorney
```

Add the upstream remote so you can keep your fork synchronized:

```
git remote add upstream https://github.com/life-jorney/life_jorney.git
```

### 2. Create a branch

Always work on a dedicated branch. Never commit directly to `main`.

Branch names follow this convention:

```
<type>/<short-description-in-kebab-case>
```

Valid types:

| Type | Use for |
|---|---|
| `feat/` | New features |
| `fix/` | Bug fixes |
| `docs/` | Documentation only |
| `test/` | Adding or improving tests |
| `chore/` | Build tooling, dependencies, CI configuration |
| `refactor/` | Code restructuring without behavior change |
| `security/` | Security fixes or hardening (coordinate with maintainers first) |

Examples of well-formed branch names:

```
feat/fhir-patient-export
fix/allergy-duplicate-validation
docs/api-authentication-guide
test/medication-interaction-service
chore/upgrade-django-5-1
refactor/consent-model-normalization
```

### 3. Write commits using Conventional Commits

Every commit message must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<optional scope>): <short description in imperative mood>

<optional body — explain the why, not the what>

<optional footer — BREAKING CHANGE or issue reference>
```

The short description must be lowercase and must not end with a period. Keep it under 72 characters.

Valid commit types: `feat`, `fix`, `docs`, `test`, `chore`, `refactor`, `perf`, `ci`, `security`.

Examples:

```
feat(fhir): add HL7 FHIR R4 Patient resource serializer

fix(auth): prevent session fixation after password change

Regenerate session token on successful password update to prevent
session fixation attacks. Resolves #142.

docs(contributing): add medical contribution workflow section

test(medication): cover drug-allergy cross-check edge cases

chore(deps): upgrade celery to 5.4.0

refactor(consent): normalize audit log schema to third normal form

BREAKING CHANGE: AuditEntry.actor field is now a ForeignKey to User
instead of a plain text field. Run the migration before deploying.
```

Commits that do not follow this format will be asked to be amended before a PR can be merged.

### 4. Open a pull request

Before opening a PR, ensure:

- Your branch is up to date with `upstream/main`.
- All tests pass locally.
- Test coverage has not dropped below 80% for the files you modified.
- All new public functions, classes, and methods have docstrings.
- Code is formatted with the tools specified in the [Code Standards](#code-standards) section.

When opening the PR:

- Use the PR template provided.
- Link to the issue or discussion that motivated the change.
- If the PR touches clinical logic, request a review from a maintainer with clinical expertise in addition to the standard code review.
- Mark the PR as a draft if it is not yet ready for full review.

A PR requires at least one approving review from a maintainer before merging. PRs that affect patient data, consent mechanisms, or clinical coding require two reviews.

---

## Code Standards

### Python (backend)

- Style: **PEP 8**, enforced with **Black** (line length 88) and **isort**.
- Docstrings: **PEP 257**, using Google-style docstring format.
- Every public function, method, and class must have a docstring. This is not optional.
- Type hints are required for all function signatures.
- Do not suppress linter warnings without a comment explaining why.

Example of a correctly documented Python function:

```python
def resolve_icd10_code(code: str) -> dict[str, str]:
    """Resolve an ICD-10 code to its full description and category.

    Args:
        code: A valid ICD-10-CM or ICD-10-WHO code string, e.g. "J18.9".

    Returns:
        A dictionary with keys "code", "description", and "category".

    Raises:
        ValueError: If the code is not found in the local terminology index.
    """
```

### JavaScript and TypeScript (frontend)

- Style: **ESLint** with the project configuration + **Prettier**.
- All exported functions and React components must have **JSDoc** comments.
- Prefer explicit TypeScript types over `any`. Use `unknown` when the type is genuinely unknown.
- React components should be functional. Class components are not accepted for new code.

### Dart and Flutter (mobile)

- Style: **dart format** (the official formatter). Run it before committing.
- Follow the [Effective Dart](https://dart.dev/effective-dart) style guide for naming and documentation conventions.
- Widget tests are required for all new screens.

### Test coverage

The project enforces a minimum of **80% line coverage** across all packages. Coverage is measured in CI for every PR. A PR that reduces coverage below 80% for the files it touches will not be merged until tests are added.

Write tests that reflect real clinical scenarios. A test that validates a FHIR resource should use realistic synthetic data, not placeholder strings like `"string"` or `"test"`.

### General rules

- All code, comments, docstrings, and commit messages must be written in **English**.
- Do not commit commented-out code. Remove it or open an issue to track it.
- Do not commit secrets, credentials, or patient data of any kind — including synthetic data that resembles real data structurally.
- Keep pull requests focused. A PR that fixes a bug and adds a new feature is two PRs.

---

## Medical and Clinical Contributions

life_jorney is a platform for healthcare. The participation of doctors, nurses, specialists, pharmacists, and other clinical professionals is not a nice-to-have — it is essential to building something that is actually safe and useful in real medical contexts.

You do not need to write code to make a meaningful contribution to this project.

### How clinicians can contribute

**Clinical workflow review.** Read a proposed feature or user story in `software_engineering.md` or in a GitHub issue, and provide feedback on whether the workflow reflects how things actually work in clinical practice. Does the allergy recording flow match what a physician expects? Is the medication history display useful during an emergency consultation? Your field experience is irreplaceable here.

**Terminology and coding review.** The project uses ICD-10/11, LOINC, SNOMED CT, and ATC codes. Reviewing proposed data models, code mappings, or search implementations for clinical accuracy is a critical contribution. You can do this entirely through GitHub comments on issues and pull requests — no local development setup required.

**Patient safety review.** Before any feature that displays clinical information reaches release, it should be reviewed by someone who understands what a clinician or patient might do with that information. Identifying misleading labels, missing contraindication warnings, or confusing dose representations is exactly the kind of review that prevents harm.

**Writing clinical documentation.** User guides for healthcare professionals, explanations of how FHIR resources map to real clinical concepts, or glossaries of clinical terms used in the codebase — all of these require clinical knowledge, not programming skills.

### How to get started as a clinical contributor

1. Read the Product Vision and User Stories in `software_engineering.md` (sections 1 and 2).
2. Open a GitHub Discussion in the "Clinical Review" category and introduce yourself and your area of expertise.
3. A maintainer will tag you on relevant open issues and upcoming PRs where your input would be valuable.

### ICD, LOINC, and SNOMED guidance

When proposing a mapping between a clinical concept and a terminology code, include:

- The full code and its official description from the authoritative source.
- The version of the terminology (e.g., ICD-10-CM 2024, SNOMED CT International Edition January 2025).
- Whether the mapping is exact, approximate, or the best available option when no exact match exists.
- Any known ambiguity or regional variation in how the code is applied.

Do not propose mappings based on memory alone. Verify against the official terminology browsers: [ICD-10 Browser](https://icd.who.int/browse10), [LOINC Search](https://loinc.org/search/), [SNOMED CT Browser](https://browser.ihtsdotools.org/).

### Patient safety review process

Any pull request that modifies how clinical information is displayed to patients or healthcare professionals, or that changes drug interaction logic, allergy cross-check behavior, or emergency access workflows, is marked with the `patient-safety-review` label.

These PRs require sign-off from at least one contributor with a verified clinical background before they can be merged, in addition to standard code review. If you have a clinical background and want to participate in these reviews, indicate this in your introduction discussion so maintainers can add you to the review rotation.

---

## Security Vulnerabilities

**Do not open a public GitHub issue to report a security vulnerability.**

If you discover a vulnerability — including authentication flaws, authorization bypasses, data exposure risks, injection vulnerabilities, or issues with the consent and audit mechanisms — report it privately by email.

> **Note:** the project domain has not yet been defined. A dedicated security email will be created once the domain is established and will be published in [SECURITY.md](./SECURITY.md) before the first public release. Check that file for the most up-to-date contact address.

Include in your email:

- A description of the vulnerability and the component affected.
- Steps to reproduce or a proof of concept (if safe to provide).
- The potential impact, including whether patient data could be exposed.
- Your contact information so we can follow up.

**Responsible disclosure process:**

1. You submit the report to the security email address published in [SECURITY.md](./SECURITY.md).
2. A maintainer acknowledges receipt within 72 hours.
3. The maintainer investigates and provides an initial assessment within 7 days.
4. If the vulnerability is confirmed, we work on a fix privately. We will keep you informed of progress.
5. A security release is prepared and coordinated.
6. After the fix is deployed, we publish a security advisory crediting you (unless you prefer to remain anonymous).

We ask that you do not disclose the vulnerability publicly until the fix is available, and we commit to moving as quickly as possible to minimize that window. We do not pursue legal action against good-faith security researchers who follow this process.

---

## Recognition

Every person who contributes to life_jorney is listed in `CONTRIBUTORS.md` in the repository. This includes code contributors, clinical reviewers, translators, designers, documentation writers, and security researchers.

Contributions are recognized in the following ways:

- **CONTRIBUTORS.md listing:** your name, GitHub handle, and the areas you contributed to are recorded permanently in the repository.
- **Release notes:** significant contributions are acknowledged in the release notes for the version they appear in.
- **Clinical reviewer badge:** contributors who participate in patient-safety reviews are listed separately as clinical reviewers to reflect the specialized nature of that work.
- **Security hall of fame:** security researchers who responsibly disclose vulnerabilities are credited in a dedicated security acknowledgment section.

life_jorney has no budget for monetary compensation. What it can offer is transparent credit, a meaningful project, and the knowledge that the work directly benefits patients.

---

## Questions

If something in this guide is unclear, or if you have a question that is not answered here, open a thread in **GitHub Discussions**. Discussions are the right place for:

- Questions about how to approach a contribution
- Requests for clarification on the engineering document
- Proposals for changes to this contributing guide itself
- General conversation about the project's direction

Do not use GitHub issues for questions. Issues are for tracked work: bugs and accepted features.

We look forward to building this with you.
