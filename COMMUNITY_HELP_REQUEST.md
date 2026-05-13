# Buscamos profesionales de la salud para co-redactar las historias de usuario clínicas
# Seeking Healthcare Professionals to Co-Author Clinical User Stories

---

> **Español** · [English below ↓](#english)

---

## Español

**Proyecto:** life_jorney — Plataforma open-source de historial médico unificado
**Repo:** https://github.com/EdyRoqueFdez/life_jorney
**Etiquetas:** `help wanted` · `clinical review` · `user stories`

### ¿Qué es life_jorney?

life_jorney es una plataforma libre, sin fines de lucro y de código abierto cuyo objetivo es que toda persona tenga la propiedad completa de su historial médico — desde el nacimiento hasta el final de la vida — en un único registro seguro e interoperable.

El proyecto se construye en abierto para que hospitales, clínicas, ONGs y profesionales independientes puedan integrarse con él sin depender de ningún proveedor comercial.

**Stack tecnológico:** Python / Django / DRF (backend) · Flutter (móvil) · Next.js (web)
**Estándares objetivo:** ICD-10/11, LOINC, SNOMED CT, HL7 FHIR R4, ATC (OMS)

### Por qué necesitamos tu ayuda

Somos ingenieros de software, no clínicos. Las primeras cuatro historias de usuario fueron escritas con la mejor intención y el conocimiento de flujos clínicos que tenemos los programadores — y funcionan como punto de partida. Pero sabemos que hay cosas que solo alguien que ha trabajado en un hospital o clínica real puede ver: una restricción de permisos que parece lógica en papel pero no en la práctica, un campo que falta, un flujo que en la realidad ocurre al revés.

Nos importa hacerlo bien desde el principio. Por eso estamos aquí, preguntando antes de construir algo difícil de corregir después.

El siguiente bloque de historias cubre territorio donde la precisión clínica es crítica:

| ID | Título | Por qué necesita ojos clínicos |
|----|--------|-------------------------------|
| HU-05 | Visualización de antecedentes familiares | ¿Qué condiciones hereditarias deben resaltarse? ¿Cómo se modela el parentesco clínicamente? |
| HU-06 | Gestión de usuarios y roles | ¿Son los roles definidos suficientes para un hospital real? ¿Faltan perfiles como residente, auxiliar de enfermería o farmacéutico? |
| HU-07 | Autenticación segura con 2FA | ¿Qué métodos de segundo factor son aceptados en entornos hospitalarios? ¿Cómo se gestiona el acceso urgente si el 2FA no está disponible? |
| HU-08 | Gestión de consentimientos | ¿Qué granularidad de consentimiento usan los sistemas reales? ¿Qué significa "revocación inmediata" en la práctica? |
| HU-09 | Registro de suministros de enfermería | ¿Qué campos son legalmente obligatorios en un registro de administración de medicamentos (MAR)? ¿Qué es un "suministro" vs un "procedimiento"? |
| HU-10 | Resultados de laboratorio | ¿Cómo se asignan los códigos LOINC en la práctica? ¿Qué aspecto tiene una "orden médica" en un flujo de laboratorio real? |
| HU-11 | Estudios de imaginología | ¿Qué metadatos son obligatorios en un estudio DICOM? ¿Debe el sistema almacenar los archivos DICOM o solo metadatos + referencia a un PACS? |
| HU-12 | Acceso de emergencia (break-glass) | ¿Cuál es el conjunto mínimo de información vital real? ¿Qué obligaciones legales existen según la jurisdicción? |
| HU-13 | Alergias y medicamentos activos | ¿Cómo funciona SNOMED CT / ATC en la práctica? ¿Cómo se detectan interacciones medicamentosas? |

### Qué pedimos

No pedimos código. Necesitamos profesionales de la salud cualificados — médicos, enfermeros/as, técnicos de laboratorio, informáticos clínicos, farmacéuticos — para:

1. **Revisar las historias de usuario existentes** (HU-01 a HU-04) y señalar lo que sea clínicamente incorrecto o incompleto. Los criterios de aceptación actuales están en [`INGENIERIA_SW.md § 2`](INGENIERIA_SW.md).

2. **Co-redactar o mejorar las historias pendientes** (HU-05 a HU-15). Incluso unas pocas frases de "en nuestro hospital lo hacemos así" tienen un valor enorme.

3. **Identificar brechas regulatorias.** Apuntamos al uso global pero sabemos que las regulaciones locales varían (HIPAA en EE.UU., GDPR en Europa, normativas latinoamericanas). Si ves un punto ciego de cumplimiento, dínoslo.

4. **Validar las decisiones de codificación clínica** (alcance ICD-10 vs ICD-11, LOINC para laboratorio, SNOMED CT para alergias, ATC para medicamentos). ¿Son los estándares correctos para cada dominio?

### ¿Cómo opera cada perfil en el sistema?

Esta es la sección donde más necesitamos tu experiencia real. El sistema define los siguientes perfiles de usuario y estamos seguros de que nos falta contexto sobre qué hace cada uno en el día a día. Responder aunque sea una de estas preguntas ya nos ayuda a construir algo que funcione de verdad.

**Médico / Doctor**
> En un turno típico, ¿qué acciones realiza el médico en el sistema para cada paciente que atiende? ¿Puede ver los registros de todos los pacientes del hospital o solo los que están bajo su cuidado directo? ¿Existe una distinción entre "consultar" y "registrar" según la relación médico-paciente?

**Médico Residente / Interno** *(¿debería ser un rol separado?)*
> En su institución, ¿existe diferencia entre lo que puede registrar o validar un residente frente a un médico de planta? ¿Un residente puede emitir un diagnóstico definitivo o solo uno preliminar que requiere confirmación de un médico de mayor jerarquía?

**Un/a enfermero/a jefe/a**
> ¿Qué acciones realiza un/a enfermero/a jefe/a en el sistema que un auxiliar de enfermería NO puede hacer? ¿Puede registrar la administración de medicamentos de forma autónoma o necesita que el médico haya generado una orden previa? ¿Puede modificar el plan de cuidados del paciente?

**Auxiliar de enfermería** *(¿debería ser un rol separado?)*
> ¿Qué registra el auxiliar en el sistema durante un turno típico? ¿Tiene acceso a la historia clínica completa del paciente o solo a lo necesario para su tarea (signos vitales, estado de higiene, movilidad)? ¿Sus registros requieren validación de un/a enfermero/a antes de quedar guardados?

**Técnico de laboratorio**
> ¿Puede el técnico validar sus propios resultados o siempre requiere la firma de un supervisor antes de que queden visibles para el médico? ¿Tiene acceso a la historia clínica del paciente o solo ve la orden y registra el resultado?

**Profesional de imaginología / Técnico radiológico**
> ¿El técnico solo realiza el estudio o también lo interpreta? ¿Existe un médico radiólogo que firma el informe de forma separada? ¿Qué información del paciente necesita el técnico antes de realizar el estudio (alergias a contraste, peso, condiciones previas)?

**Supervisor**
> En su institución, ¿el supervisor es un médico de mayor jerarquía, un/a enfermero/a jefe/a, o un perfil administrativo? ¿Qué tipo de acción en el sistema genera una notificación al supervisor? ¿Puede el supervisor modificar un registro ya guardado por otro profesional?

**Farmacéutico** *(¿debería ser un rol en el sistema?)*
> ¿Debería existir un perfil de farmacéutico en el sistema? Si es así, ¿sus funciones incluirían: validar prescripciones antes de la dispensación, registrar la entrega del medicamento, detectar interacciones fármaco-fármaco? ¿O esto queda fuera del alcance de un historial médico y pertenece a un sistema de farmacia separado?

### Cómo contribuir

- **Responde esta Discussion** con tu experiencia o correcciones — sin necesidad de tocar código ni archivos.
- **Abre un Issue** con la etiqueta `clinical review` para una brecha específica.
- **PR directo en `INGENIERIA_SW.md`** si te sientes cómodo con Markdown.
- **Email:** [edyrfdez89@gmail.com](mailto:edyrfdez89@gmail.com) con asunto `life_jorney – revisión clínica`.

### Qué ofrecemos a cambio

- **Crédito de autoría** en el README y en las notas de versión por cada contribución.
- Rol de **Clinical Advisor** en la gobernanza del proyecto (cuando el modelo de gobernanza esté formalizado).
- La satisfacción de saber que, si este proyecto alcanza su potencial, servirá a pacientes que hoy no tienen acceso a un historial médico unificado.

No podemos ofrecer remuneración económica — este es un proyecto open-source sin fines de lucro. Lo que sí podemos prometer es que cada aporte tuyo se verá reflejado directamente en el sistema, con tu nombre.

### Preguntas abiertas — donde más necesitamos ayuda

Si solo tienes 10 minutos, responder cualquiera de estas preguntas ya ayuda enormemente:

1. **HU-09 / Enfermería:** ¿Es correcto decir que un/a enfermero/a solo puede registrar suministros para pacientes "asignados a su área"? ¿Cómo se modela esa asignación en el software hospitalario real?

2. **HU-10 / Laboratorio:** ¿Puede un técnico modificar un resultado ya validado por un supervisor? Si es así, ¿debe el supervisor re-validar? ¿Qué distingue una "modificación de resultado" de un nuevo resultado?

3. **HU-11 / Imaginología:** ¿Debe el sistema almacenar archivos DICOM directamente o solo metadatos + referencia a un PACS externo? ¿Cuál es el conjunto mínimo de metadatos si el almacenamiento DICOM completo queda fuera del alcance de la v1?

4. **HU-12 / Break-glass:** Los criterios actuales dicen que el conjunto vital mínimo es "grupo sanguíneo, alergias activas, medicamentos actuales y condiciones crónicas". ¿Es correcto? ¿Falta algo crítico (p. ej., dispositivos implantables, directivas anticipadas)?

5. **HU-13 / Alergias:** Los criterios dicen que las alergias deben codificarse con SNOMED CT "cuando esté disponible". En la práctica, ¿es suficiente la adopción de SNOMED CT para exigirlo, o necesitamos un fallback de texto libre?

6. **HU-05 / Historia familiar:** ¿Qué condiciones hereditarias (o categorías de condiciones) son clínicamente significativas como para mostrarse siempre visualmente en el árbol familiar? ¿Existe una ontología estándar para el riesgo hereditario?

---

<a name="english"></a>

## English

**Project:** life_jorney — Open-source unified medical history platform
**Repo:** https://github.com/EdyRoqueFdez/life_jorney
**Labels:** `help wanted` · `clinical review` · `user stories`

### What is life_jorney?

life_jorney is a free, non-profit, open-source platform whose goal is to give every person full ownership of their medical history — from birth to the end of life — in a single, secure, interoperable record.

The project is being built in the open so that hospitals, clinics, NGOs, and individual practitioners can eventually integrate with it without depending on any commercial vendor.

**Tech stack:** Python / Django / DRF (backend) · Flutter (mobile) · Next.js (web)
**Standards targeted:** ICD-10/11, LOINC, SNOMED CT, HL7 FHIR R4, ATC (WHO)

### Why we need your help

We are software engineers, not clinicians. The first four user stories were written with the best intentions and a programmer's understanding of clinical workflows — and they work as a starting point. But we know there are things only someone who has worked in a real hospital or clinic can see: a permission restriction that seems logical on paper but not in practice, a missing field, a workflow that actually happens in the opposite order.

We want to get it right from the start. That's why we're here, asking questions before building something that would be hard to fix later.

The next batch of stories covers territory where clinical accuracy is critical:

| ID | Title | Why it needs clinical eyes |
|----|-------|---------------------------|
| HU-05 | Family medical history visualization | Which hereditary conditions should be flagged? How is family relatedness modelled clinically? |
| HU-06 | User and role management | Are the defined roles enough for a real hospital? Are profiles like resident, nursing assistant, or pharmacist missing? |
| HU-07 | Secure authentication with 2FA | Which second-factor methods are accepted in hospital environments? How is urgent access handled if 2FA is unavailable? |
| HU-08 | Patient consent management | What consent granularity do real systems use? What does "immediate revocation" mean in practice? |
| HU-09 | Nursing supply records | What fields are legally required in a medication administration record (MAR)? What counts as a "supply" vs a "procedure"? |
| HU-10 | Laboratory results | How are LOINC codes assigned in practice? What does a "medical order" look like in a real lab workflow? |
| HU-11 | Imaging studies | What metadata is mandatory in a DICOM study? Should the system store DICOM files or only metadata + a reference to a PACS? |
| HU-12 | Emergency (break-glass) access | What clinical information is the true minimum vital set? What legal obligations exist in different jurisdictions? |
| HU-13 | Allergies and active medications | How do ATC / SNOMED CT coding practices work in real settings? How are drug-drug and drug-allergy interactions detected? |

### What we are asking for

We are **not** asking for code. We need qualified healthcare professionals — doctors, nurses, lab technicians, clinical informaticists, pharmacists — to:

1. **Review the existing user stories** (HU-01 through HU-04) and point out anything that is clinically wrong or missing. The current acceptance criteria are in [`INGENIERIA_SW.md § 2`](INGENIERIA_SW.md).

2. **Co-author or improve the pending user stories** (HU-05 through HU-15). Even a few sentences of "in our hospital we do it like this" is enormously valuable.

3. **Identify regulatory gaps.** We are targeting global use, but we know local regulations vary (HIPAA in the US, GDPR in Europe, Latin American regulations). If you spot a compliance blind spot, please tell us.

4. **Validate the clinical coding choices** (ICD-10 vs ICD-11 scope, LOINC for lab, SNOMED CT for allergies, ATC for drugs). Are these the right standards for each domain?

### How does each profile operate in the system?

This is the section where we need your real-world experience the most. The system defines several user profiles, and we are confident we are missing context about what each one actually does day to day. Answering even one of these questions helps us build something that works in practice.

**Doctor / Physician**
> In a typical shift, what actions does the doctor take in the system for each patient they see? Can they view all patients' records in the hospital, or only those under their direct care? Is there a distinction between "reading" and "recording" based on the doctor-patient relationship?

**Medical Resident / Intern** *(should this be a separate role?)*
> In your institution, is there a difference between what a resident can record or validate compared to an attending physician? Can a resident issue a definitive diagnosis, or only a preliminary one that requires confirmation from a senior physician?

**Head Nurse / Charge Nurse**
> What actions does a head nurse or charge nurse take in the system that a nursing assistant cannot? Can they record medication administration independently, or does a physician order need to exist first? Can they modify a patient's care plan?

**Nursing Assistant** *(should this be a separate role?)*
> What does a nursing assistant record in the system during a typical shift? Do they have access to the patient's full clinical history, or only what is relevant to their task (vital signs, hygiene, mobility)? Do their records require validation from a nurse before being saved?

**Lab Technician**
> Can the technician validate their own results, or does a supervisor always need to sign off before results are visible to the physician? Do they have access to the patient's clinical history, or do they only see the order and record the result?

**Imaging Professional / Radiologic Technologist**
> Does the technician only perform the study, or do they also interpret it? Is there a radiologist who signs the report separately? What patient information does the technician need before performing the study (contrast allergies, weight, prior conditions)?

**Supervisor**
> In your institution, is the supervisor a senior physician, a head nurse, or an administrative role? What type of system action triggers a notification to the supervisor? Can the supervisor modify a record already saved by another professional?

**Pharmacist** *(should this be a role in the system?)*
> Should there be a pharmacist profile in the system? If so, would their functions include: validating prescriptions before dispensing, recording medication delivery, detecting drug-drug interactions? Or does this fall outside the scope of a medical history and belong in a separate pharmacy system?

### How to contribute

- **Reply to this Discussion** with your experience or corrections — no need to touch any code or file.
- **Open an Issue** with the label `clinical review` for a specific gap.
- **Direct PR on `INGENIERIA_SW.md`** if you are comfortable with Markdown.
- **Email:** [edyrfdez89@gmail.com](mailto:edyrfdez89@gmail.com) — subject: `life_jorney – clinical review`.

### What we can offer in return

- **Authorship credit** in the project README and release notes for every contribution.
- A **Clinical Advisor** role in the project governance (once the governance model is formalized).
- The satisfaction of knowing that, if this project reaches its potential, it will serve patients who currently have no access to a unified medical record.

We cannot offer payment — this is a non-profit open-source project. What we can promise is that every contribution you make will be reflected directly in the system, with your name on it.

### Open questions — where we need help most

If you only have 10 minutes, answering any one of these helps enormously:

1. **HU-09 / Nursing:** Is it accurate to say a nurse can only record supplies for patients "assigned to their area"? How is area assignment modelled in real hospital software?

2. **HU-10 / Lab:** Can a lab technician modify a result after it has been validated by a supervisor? If so, does the supervisor need to re-validate? What distinguishes a "result modification" from a new result?

3. **HU-11 / Imaging:** Should the system store DICOM files directly, or only metadata + a reference to a PACS? What is the minimum viable metadata set if full DICOM storage is out of scope for v1?

4. **HU-12 / Break-glass:** The current criteria say the minimum vital set is "blood type, active allergies, current medications, and chronic conditions." Is this correct? Is anything critical missing (e.g., implantable devices, advance directives)?

5. **HU-13 / Allergies:** The criteria say allergies should be coded with SNOMED CT "when available." In practice, is SNOMED CT adoption widespread enough to mandate it, or do we need a free-text fallback?

6. **HU-05 / Family history:** Which hereditary conditions (or condition categories) are clinically significant enough to always surface visually in a family tree? Is there a standard ontology for hereditary risk?

---

*Thank you for reading this far. Every sentence you write saves us from implementing something clinically wrong — and that matters deeply when the system will eventually touch real patient data. We'd love to have you as part of this.*

*Gracias por leer hasta aquí. Cada frase que escribas nos evita implementar algo clínicamente incorrecto — y eso importa profundamente cuando el sistema eventualmente tocará datos reales de pacientes. Nos encantaría tenerte como parte de esto.*
