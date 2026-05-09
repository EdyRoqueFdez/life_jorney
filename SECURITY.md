# Security Policy

life_jorney handles some of the most sensitive data that exists: personal health records, diagnoses, medications, and family medical histories. A security vulnerability in this system is not just a software problem — it can have real consequences for real people. We take every report seriously and we are deeply grateful to researchers who help us protect patients and their data.

---

## Supported Versions

The project is currently in the pre-release phase. Once versions are published, this table will reflect which ones receive active security patches.

| Version | Status |
|---------|--------|
| `main` branch | Active development — receives all security fixes |
| MVP (v1.0, upcoming) | Will receive security patches |
| Pre-release / development builds | Not for production use; vulnerabilities in these builds are still welcome |

---

## How to Report a Vulnerability

**Do not open a public GitHub issue, pull request, or discussion thread for a security vulnerability.** Public disclosure before a fix is available puts patients and their data at risk.

### Preferred channel

Send your report by email to:

```
[pending — the project domain has not yet been defined]
[a dedicated security email will be set up and published here before the first public release]
```

If you need to send sensitive technical details (credentials found, proof-of-concept code, or data exposure evidence), you may request our PGP public key by writing to the same address once it is published.

### What to include in your report

A good report helps us reproduce and fix the issue faster. Please include as much of the following as you can:

1. **Summary:** a one-paragraph description of the vulnerability and its impact.
2. **Affected component:** backend API, web frontend, mobile app, database, infrastructure, authentication, audit log, etc.
3. **Steps to reproduce:** a clear, numbered sequence of steps that demonstrates the vulnerability. Include request/response samples, relevant code paths, or configuration details.
4. **Proof of concept:** if you have a PoC script, attach it. We will not penalize good-faith researchers for writing a PoC.
5. **Impact assessment:** what data or functionality is at risk? Under what conditions? How many users could be affected?
6. **Suggested fix:** optional, but appreciated if you have one in mind.
7. **Your contact information:** name or alias, and how you prefer to be contacted for follow-up.

**Important:** if during your research you encountered actual patient data from a live deployment, tell us immediately. Do not copy, store, or share that data. We will treat this with the highest urgency regardless of how you found it.

---

## Response Timeline

We commit to the following SLAs once a report is received:

| Milestone | Target time |
|-----------|-------------|
| Initial acknowledgement | Within 72 hours |
| Vulnerability assessment (confirmed / not confirmed) | Within 7 days |
| Severity classification shared with reporter | Within 10 days |
| Fix delivered for Critical or High severity | Before next release, or sooner if actively exploited |
| Fix delivered for Medium severity | Within 60 days |
| Fix delivered for Low severity | Within 90 days |
| Public disclosure (coordinated with reporter) | After fix is deployed |

If circumstances prevent us from meeting these timelines, we will communicate with you proactively. We will never go silent on a confirmed vulnerability.

---

## Severity Classification

We use the following scale to classify reported vulnerabilities:

| Severity | Description | Examples in this project |
|----------|-------------|--------------------------|
| **Critical** | Direct exposure of patient health data; authentication bypass; ability to modify medical records without authorization | Unauthenticated access to patient history; audit log tampering; bypass of consent controls |
| **High** | Indirect patient data exposure; privilege escalation; broken access controls; significant data integrity risk | Doctor accessing records of patients who never gave consent; supervisor role escalation; break-glass access without logging |
| **Medium** | Limited data exposure; logic flaws that do not directly expose PHI; security misconfigurations | Session fixation; CSRF on non-sensitive actions; information leakage in error messages |
| **Low** | Minor issues with limited impact; informational findings | Outdated dependency with no known exploit; verbose HTTP headers |

---

## Scope

The following are in scope for security research:

- Backend REST API (Django / Django Rest Framework)
- Web frontend (React application)
- Mobile application (Flutter — Android and iOS)
- Authentication and two-factor authentication flows
- Consent management and access control logic
- Audit log integrity mechanisms
- Break-glass emergency access flow
- FHIR export endpoint
- File upload and storage (MinIO)
- Offline sync mechanism (SQLite local storage)
- Infrastructure configuration files in the repository

The following are **out of scope:**

- Social engineering attacks against project contributors or maintainers
- Physical attacks against infrastructure
- Denial of Service (DoS / DDoS) attacks
- Vulnerabilities in third-party dependencies that have already been publicly disclosed (report these via the dependency's own security channel and open a regular dependency-update issue with us)
- Automated scanner results submitted without a confirmed, reproducible impact
- Issues requiring unlikely or impractical user interaction (e.g., a user deliberately misconfiguring their own account)

---

## Responsible Disclosure and Safe Harbor

We support coordinated responsible disclosure. If you follow the guidelines in this policy, we commit to:

- Not pursuing legal action against you for your research, provided it was conducted in good faith and within scope.
- Not sharing your identity with third parties without your consent.
- Working with you to understand and fix the issue before any public disclosure.
- Giving you credit for the finding (if you want it) in our security acknowledgements.

We define "good faith" research as: accessing only accounts and data you control or have explicit permission to test; not modifying or deleting data that does not belong to you; not exploiting a vulnerability beyond what is necessary to demonstrate impact; and reporting to us promptly.

If at any point during your research you access data that appears to belong to real patients, **stop immediately** and contact us. We will not treat this as a violation if you act responsibly.

---

## Regulatory Breach Notification

life_jorney operates under multiple data protection regulations. A confirmed breach involving personal health data triggers mandatory notification obligations:

| Regulation | Notification requirement |
|------------|--------------------------|
| **GDPR** | Supervisory authority within 72 hours of becoming aware; affected individuals without undue delay if high risk |
| **HIPAA** | Affected individuals within 60 days; HHS and media (if >500 affected) annually or within 60 days |
| **Colombia Ley 1581** | SIC (Superintendencia de Industria y Comercio) as required |
| **Brazil LGPD** | ANPD and affected individuals within a reasonable timeframe |

If your report reveals a breach of this nature, please flag it explicitly. This affects our response timeline and obligations.

---

## Recognition

life_jorney does not currently operate a paid bug bounty program — we are a non-profit open source project. However, we believe that security researchers who help protect patients deserve recognition.

Researchers who responsibly disclose a confirmed vulnerability will be:

- Listed in our [Security Hall of Fame](./SECURITY_HALL_OF_FAME.md) (created when the first finding is confirmed), with their preferred name or alias and a description of their contribution.
- Thanked publicly in the release notes of the version that includes the fix (if they consent to public credit).
- Given priority consideration for paid roles if the project ever reaches a funded state where that becomes possible.

We are also open to discussing other forms of recognition — conference speaking opportunities, co-authorship on security write-ups, or letters of acknowledgement for professional portfolios.

---

## Contact

| Purpose | Contact |
|---------|---------|
| Security vulnerability reports | **Pending** — domain not yet defined. A security email will be published here before the first public release. |
| General security questions (non-sensitive) | Open a [GitHub Discussion](../../discussions) |
| Code of Conduct violations | **Pending** — domain not yet defined. A conduct email will be published in [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) before the first public release. |
| General project questions | Open a [GitHub Discussion](../../discussions) |

---

*This policy is reviewed and updated before every major release.*
