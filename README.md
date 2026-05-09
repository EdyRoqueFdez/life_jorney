# life_jorney

[Leer en Español](./README_ES.md)

> *One lifetime. One record. Open to the world.*

![Status](https://img.shields.io/badge/status-pre--alpha%20%7C%20defining%20architecture-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)
![Built With](https://img.shields.io/badge/built%20with-Django%20%7C%20React%20%7C%20Flutter-blueviolet)

---

## What is life_jorney?

**life_jorney** is a free, open-source platform that brings together a person's complete medical history in one place — from before birth to the end of life. It gives patients full ownership of their health data and gives healthcare professionals a secure, unified view of a patient's clinical journey.

In future phases, life_jorney will use anonymized data and Big Data analysis to help predict hereditary diseases — like cancer — before they manifest.

> The name is intentional. "Jorney" instead of "journey" — because every medical record is also a deeply personal story, and this one is yours.

---

## The Problem

A person's medical history today is scattered across dozens of hospitals, clinics, and formats. There is no single, secure, and universal place to consult the complete clinical picture of a person — including family history that could reveal hereditary risk patterns.

**The consequences are real:**
- Doctors repeat tests because they cannot access prior results.
- Patients arrive at emergencies without their allergy or medication history.
- Hereditary disease patterns go undetected because no one connects the dots across generations.
- Medical records are locked inside private systems, inaccessible to the people they belong to.

life_jorney exists to change that.

---

## Why Open Source?

As humanity, we invest and develop far more for war than for health. We believe that a tool as essential as a unified medical history should be a **common good, not a commercial privilege**.

- **Free to use, forever.** No paywalls for patients or small clinics.
- **Community-driven.** Doctors, developers, designers, and patients build it together.
- **Auditable.** Anyone can inspect the code, the data model, and the privacy decisions.
- **Global by default.** Built to work across languages, borders, and regulations (GDPR, HIPAA, and more).

---

## What We Are Building (MVP)

The first version focuses on securely collecting and managing medical history. No AI, no predictions yet — just a solid foundation built right.

| Feature | Description |
|---------|-------------|
| Unified medical timeline | All events in chronological order: consultations, vaccines, diagnoses, lab results, imaging studies |
| Allergy and medication alerts | Active allergy and medication lists with automatic interaction warnings |
| Family medical history | Link family members and visualize hereditary patterns with a family tree |
| Role-based access control | Patients, doctors, nurses, lab technicians, imaging professionals, supervisors, and admins — each with the right level of access |
| Explicit patient consent | Patients grant and revoke access doctor by doctor, at any time |
| Emergency access (break-glass) | Life-threatening situations require a justified override; every access is logged and the patient is notified |
| Immutable audit log | Every write action is permanently recorded. No one — not even admins — can modify the audit trail |
| HL7 FHIR R4 export | Patients can download their full history in the global interoperability standard |
| Right to erasure | Full GDPR-compliant account and data deletion |
| Offline-first mobile app | Works in areas with poor connectivity; syncs automatically when back online |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | Python 3.12 + Django 5.0 + Django Rest Framework |
| Web Frontend | React 18 + TypeScript |
| Mobile App | Flutter 3 + Dart (Android and iOS) |
| Database | PostgreSQL 16 |
| Local mobile storage | SQLite + SQLCipher (AES-256 encrypted) |
| File storage (DICOM, etc.) | MinIO (self-hosted, S3-compatible) |
| Cache and task queue | Redis 7 + Celery |
| Reverse proxy | Nginx + Gunicorn |
| Containers | Docker + Docker Compose |
| Clinical coding | ICD-10/11, LOINC, SNOMED CT, ATC, DICOM, HL7 FHIR R4 |

---

## Security and Privacy — Non-Negotiable

Health data is among the most sensitive data that exists. Privacy and security are baked into the architecture, not bolted on afterward.

- **Encryption in transit:** TLS 1.3 only (no older versions).
- **Encryption at rest:** AES-256 for all health data; column-level encryption for the most sensitive fields.
- **Encrypted local storage:** SQLCipher on mobile devices.
- **Privacy by Design:** the 7 principles of Privacy by Design guide every architectural decision.
- **Compliance:** GDPR, HIPAA, Colombia Ley 1581, Brazil LGPD — and extending to more regions as the community grows.
- **Security audits:** a professional penetration test is required before every major release.
- **DPIA:** a Data Protection Impact Assessment is maintained and reviewed at every architectural change.

For a deep dive into our security and privacy model, see the [Software Engineering document](./software_engineering.md).

---

## Project Status

We are currently in the **architecture and planning phase**. No production code has been written yet.

**This is the best moment to get involved** — foundational decisions are still being made, and every voice matters.

| Phase | Status |
|-------|--------|
| Architecture and engineering definition | In progress |
| Backend core + authentication | Starting soon |
| React web frontend | Upcoming |
| Flutter mobile app | Upcoming |
| External security audit | Before MVP launch |
| MVP launch | Target: October 2026 |

---

## Roadmap

**Phase 1 — MVP (2026):** All the features listed above. Secure, private, functional.

**Phase 2 — Institutional (2027):** HL7 FHIR integration with hospitals and clinics; managed deployments for healthcare institutions; full iOS app.

**Phase 3 — Prediction Engine (2027–2028):** Big Data analysis of anonymized, consented family histories to detect hereditary disease risk patterns.

Full technical roadmap: [software_engineering.md — Section 11.3](./software_engineering.md#113-high-level-roadmap)

---

## How to Contribute

**You do not need to be a developer to contribute.** life_jorney needs people across many disciplines.

### Ways to contribute

| Contribution type | What we need |
|-------------------|-------------|
| **Backend development** | Django, DRF, PostgreSQL, Celery, Redis |
| **Frontend development** | React + TypeScript, accessibility (WCAG 2.1) |
| **Mobile development** | Flutter + Dart, offline-first architecture |
| **UI/UX design** | Wireframes, design system, accessibility audits |
| **Medical expertise** | Clinical review of workflows, ICD/LOINC/SNOMED coding guidance, patient safety review |
| **Security research** | Architecture review, threat modeling, penetration testing |
| **Documentation** | Technical writing, user guides, API documentation |
| **Translation** | We want to support as many languages as possible |
| **Testing** | Manual testing, test case writing, QA |
| **Community** | Spreading the word, writing blog posts, helping newcomers |

### Good first contributions

Not sure where to start? Look for issues labeled:

- `good first issue` — small, well-defined tasks ideal for newcomers
- `help wanted` — tasks where we actively need support
- `documentation` — improve docs without touching production code
- `medical review needed` — clinical experts needed to validate workflows

### For developers: getting started

> The development environment setup guide will be published here once the initial codebase is committed. Follow this repository to be notified.

In the meantime, read the [Software Engineering document](./software_engineering.md) to understand the architecture and make informed contributions from day one.

### Contribution guidelines

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before submitting your first pull request. It covers:

- Branch naming and commit message conventions (Conventional Commits)
- Pull request process and review expectations
- Code style and documentation requirements
- How to report bugs and propose features

### Reporting security vulnerabilities

**Do not open a public issue for security vulnerabilities.**
The project domain has not yet been defined. A dedicated security email will be created and published in [SECURITY.md](./SECURITY.md) before the first public release. Always check that file for the current contact address.

---

## Community

This project lives by its community. Here is where conversations happen:

- **GitHub Discussions** — questions, ideas, general conversation → [Discussions tab](../../discussions)
- **GitHub Issues** — bug reports and feature requests → [Issues tab](../../issues)

We are exploring setting up a dedicated community space (Discord or Matrix). Watch this space.

### Code of Conduct

We are committed to a welcoming and respectful community. All contributors are expected to follow our [Code of Conduct](./CODE_OF_CONDUCT.md).

We value contributions from people of all backgrounds, including patients, healthcare workers, and technologists. Clinical expertise is as valuable as coding expertise here.

---

## Governance

life_jorney is governed by three committees:

- **Technical Committee** — architecture, standards, technology roadmap
- **Medical-Ethical Committee** — ensures features respect clinical and ethical principles
- **Privacy Committee** — regulatory compliance, DPIA oversight, security incident response

Major decisions follow a public RFC (Request for Comments) process in GitHub Discussions. Every contributor has a voice.

---

## License

life_jorney is released under the [MIT License](./LICENSE).

You are free to use, copy, modify, distribute, and deploy this software — including for institutional use — as long as the original license notice is preserved. Commercial use is permitted; selling the software without significant modification is not in the spirit of this project.

---

## Acknowledgements

life_jorney is built by a global community of developers, healthcare professionals, designers, and patients who believe healthcare technology should serve humanity — not the other way around.

Every contributor is listed in [CONTRIBUTORS.md](./CONTRIBUTORS.md).

---

*If you believe that technology can change healthcare when it is built in the open, this project is for you.*
