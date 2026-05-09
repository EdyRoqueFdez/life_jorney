# life_jorney

[Read in English](./README.md)

> *Una vida. Un historial. Abierto al mundo.*

![Estado](https://img.shields.io/badge/estado-pre--alpha%20%7C%20definiendo%20arquitectura-blue)
![Licencia](https://img.shields.io/badge/licencia-MIT-green)
![Contribuciones Bienvenidas](https://img.shields.io/badge/contribuciones-bienvenidas-brightgreen)
![PRs Bienvenidos](https://img.shields.io/badge/PRs-bienvenidos-brightgreen)
![Construido con](https://img.shields.io/badge/construido%20con-Django%20%7C%20React%20%7C%20Flutter-blueviolet)

---

## ¿Qué es life_jorney?

**life_jorney** es una plataforma gratuita y de código abierto que reúne el historial médico completo de una persona en un solo lugar — desde antes de nacer hasta el final de la vida. Le devuelve al paciente la propiedad de sus datos de salud y le da al personal de salud una vista unificada y segura del recorrido clínico de cada paciente.

En fases futuras, life_jorney utilizará datos anonimizados y análisis de Big Data para ayudar a predecir enfermedades hereditarias — como el cáncer — antes de que se manifiesten.

> El nombre es intencional. "Jorney" en lugar de "journey" — porque cada historial médico es también una historia profundamente personal, y esta es la tuya.

---

## El problema

El historial médico de una persona hoy está disperso en decenas de hospitales, clínicas y formatos. No existe un lugar único, seguro y universal donde consultar el cuadro clínico completo de un individuo — incluyendo los antecedentes familiares que podrían revelar patrones de riesgo hereditario.

**Las consecuencias son reales:**
- Los médicos repiten exámenes porque no pueden acceder a resultados previos.
- Los pacientes llegan a urgencias sin que nadie sepa sus alergias o sus medicamentos actuales.
- Los patrones de enfermedades hereditarias pasan desapercibidos porque nadie conecta los puntos a lo largo de las generaciones.
- Los historiales médicos están atrapados dentro de sistemas privados, inaccesibles para las personas a quienes pertenecen.

life_jorney existe para cambiar eso.

---

## ¿Por qué código abierto?

Como humanidad, invertimos y desarrollamos mucho más para la guerra que para la salud. Creemos que una herramienta tan esencial como el historial médico unificado debe ser un **bien común, no un privilegio comercial**.

- **Gratuito para siempre.** Sin barreras de pago para pacientes ni clínicas pequeñas.
- **Construido por la comunidad.** Médicos, desarrolladores, diseñadores y pacientes lo construyen juntos.
- **Auditable.** Cualquiera puede inspeccionar el código, el modelo de datos y las decisiones de privacidad.
- **Global por diseño.** Construido para funcionar en múltiples idiomas, países y regulaciones (GDPR, HIPAA y más).

---

## Qué estamos construyendo (MVP)

La primera versión se centra en recolectar y gestionar el historial médico de forma segura. Sin inteligencia artificial ni predicciones todavía — solo una base sólida construida correctamente.

| Funcionalidad | Descripción |
|---------------|-------------|
| Línea de tiempo médica unificada | Todos los eventos en orden cronológico: consultas, vacunas, diagnósticos, resultados de laboratorio, estudios de imagen |
| Alertas de alergias y medicamentos | Lista de alergias y medicamentos activos con avisos automáticos de interacciones |
| Antecedentes familiares | Vincula a familiares y visualiza patrones hereditarios con un árbol genealógico |
| Control de acceso por roles | Pacientes, médicos, enfermeros, técnicos de laboratorio, profesionales de imaginología, supervisores y administradores — cada uno con el nivel de acceso correcto |
| Consentimiento explícito del paciente | El paciente otorga y revoca el acceso médico por médico, en cualquier momento |
| Acceso de emergencia (break-glass) | Las situaciones de riesgo vital requieren un acceso justificado; cada acceso queda registrado y el paciente es notificado |
| Log de auditoría inmutable | Toda operación de escritura queda permanentemente registrada. Nadie — ni siquiera los administradores — puede modificar la bitácora |
| Exportación HL7 FHIR R4 | Los pacientes pueden descargar su historial completo en el estándar global de interoperabilidad |
| Derecho al olvido | Eliminación completa de cuenta y datos personales, conforme al GDPR |
| App móvil offline-first | Funciona en zonas con conectividad deficiente; sincroniza automáticamente al recuperar la conexión |

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend API | Python 3.12 + Django 5.0 + Django Rest Framework |
| Frontend Web | React 18 + TypeScript |
| App Móvil | Flutter 3 + Dart (Android e iOS) |
| Base de datos | PostgreSQL 16 |
| Almacenamiento local móvil | SQLite + SQLCipher (cifrado AES-256) |
| Almacenamiento de archivos (DICOM, etc.) | MinIO (autoalojado, compatible con S3) |
| Caché y cola de tareas | Redis 7 + Celery |
| Proxy inverso | Nginx + Gunicorn |
| Contenedores | Docker + Docker Compose |
| Codificación clínica | ICD-10/11, LOINC, SNOMED CT, ATC, DICOM, HL7 FHIR R4 |

---

## Seguridad y privacidad — No negociables

Los datos de salud son de los más sensibles que existen. La privacidad y la seguridad están integradas en la arquitectura desde el primer día, no añadidas como capa posterior.

- **Cifrado en tránsito:** solo TLS 1.3 (sin versiones anteriores del protocolo).
- **Cifrado en reposo:** AES-256 para todos los datos de salud; cifrado a nivel de columna para los campos más sensibles.
- **Almacenamiento local cifrado:** SQLCipher en dispositivos móviles.
- **Privacidad por diseño:** los 7 principios de Privacy by Design guían cada decisión arquitectónica.
- **Cumplimiento normativo:** GDPR, HIPAA, Ley 1581 de Colombia, LGPD de Brasil — y más regulaciones a medida que la comunidad crece.
- **Auditorías de seguridad:** se requiere un pentest profesional externo antes de cada lanzamiento mayor.
- **EIPD:** se mantiene y revisa una Evaluación de Impacto sobre la Protección de Datos ante cada cambio arquitectónico significativo.

Para un análisis en profundidad de nuestro modelo de seguridad y privacidad, consulta el [documento de Ingeniería de Software](./INGENIERIA_SW.md).

---

## Estado del proyecto

Actualmente estamos en la **fase de arquitectura y definición**. Aún no se ha escrito código de producción.

**Este es el mejor momento para involucrarse** — las decisiones fundamentales todavía se están tomando, y cada voz importa.

| Fase | Estado |
|------|--------|
| Definición de arquitectura e ingeniería | En progreso |
| Backend core + autenticación | Próximamente |
| Frontend web React | Próximamente |
| App móvil Flutter | Próximamente |
| Auditoría externa de seguridad | Antes del lanzamiento MVP |
| Lanzamiento MVP | Objetivo: octubre de 2026 |

---

## Hoja de ruta

**Fase 1 — MVP (2026):** Todas las funcionalidades listadas arriba. Seguro, privado, funcional.

**Fase 2 — Institucional (2027):** Integración HL7 FHIR con hospitales y clínicas; despliegues gestionados para instituciones de salud; app iOS completa.

**Fase 3 — Motor de predicción (2027–2028):** Análisis de Big Data sobre historiales familiares anonimizados y con consentimiento para detectar patrones de riesgo de enfermedades hereditarias.

Hoja de ruta técnica completa: [INGENIERIA_SW.md — Sección 11.3](./INGENIERIA_SW.md#113-hoja-de-ruta-de-alto-nivel)

---

## Cómo contribuir

**No necesitas ser desarrollador para contribuir.** life_jorney necesita personas de múltiples disciplinas.

### Formas de contribuir

| Tipo de contribución | Qué necesitamos |
|----------------------|-----------------|
| **Desarrollo backend** | Django, DRF, PostgreSQL, Celery, Redis |
| **Desarrollo frontend** | React + TypeScript, accesibilidad (WCAG 2.1) |
| **Desarrollo móvil** | Flutter + Dart, arquitectura offline-first |
| **Diseño UI/UX** | Wireframes, sistema de diseño, auditorías de accesibilidad |
| **Conocimiento médico** | Revisión clínica de flujos de trabajo, guía de codificación ICD/LOINC/SNOMED, revisión de seguridad del paciente |
| **Investigación en seguridad** | Revisión de arquitectura, modelado de amenazas, pruebas de penetración |
| **Documentación** | Redacción técnica, guías de usuario, documentación de API |
| **Traducción** | Queremos soportar el mayor número de idiomas posible |
| **Testing** | Pruebas manuales, redacción de casos de prueba, QA |
| **Comunidad** | Difusión, artículos de blog, ayuda a nuevos contribuidores |

### Buenas primeras contribuciones

¿No sabes por dónde empezar? Busca issues etiquetados como:

- `good first issue` — tareas pequeñas y bien definidas, ideales para quienes comienzan
- `help wanted` — tareas donde necesitamos apoyo activamente
- `documentation` — mejora la documentación sin tocar código de producción
- `medical review needed` — se necesitan expertos clínicos para validar flujos de trabajo

### Para desarrolladores: cómo empezar

> La guía de configuración del entorno de desarrollo se publicará aquí en cuanto el código inicial esté disponible. Sigue el repositorio para recibir notificaciones.

Mientras tanto, lee el [documento de Ingeniería de Software](./INGENIERIA_SW.md) para entender la arquitectura y contribuir con criterio desde el primer día.

### Guía de contribución

Por favor, lee [CONTRIBUTING.md](./CONTRIBUTING.md) antes de enviar tu primer pull request. Cubre:

- Nomenclatura de ramas y convenciones de commits (Conventional Commits)
- Proceso de pull request y expectativas de revisión
- Estilo de código y requisitos de documentación
- Cómo reportar errores y proponer funcionalidades

### Reportar vulnerabilidades de seguridad

**No abras un issue público para reportar vulnerabilidades de seguridad.**
El dominio del proyecto aún no está definido. Se creará un correo de seguridad dedicado y se publicará en [SECURITY_ES.md](./SECURITY_ES.md) antes del primer lanzamiento público. Consulta siempre ese archivo para obtener la dirección de contacto actualizada.

---

## Comunidad

Este proyecto vive gracias a su comunidad. Aquí es donde ocurren las conversaciones:

- **GitHub Discussions** — preguntas, ideas, conversación general → [pestaña Discussions](../../discussions)
- **GitHub Issues** — reportes de errores y solicitudes de funcionalidades → [pestaña Issues](../../issues)

Estamos explorando la creación de un espacio de comunidad dedicado (Discord o Matrix). Mantente atento.

### Código de conducta

Estamos comprometidos con una comunidad acogedora y respetuosa. Se espera que todos los contribuidores sigan nuestro [Código de Conducta](./CODE_OF_CONDUCT.md).

Valoramos las contribuciones de personas de todos los ámbitos, incluyendo pacientes, personal de salud y tecnólogos. El conocimiento clínico es tan valioso aquí como el conocimiento técnico.

---

## Gobernanza

life_jorney es gobernado por tres comités:

- **Comité Técnico** — arquitectura, estándares y hoja de ruta tecnológica
- **Comité Médico-Ético** — asegura que las funcionalidades respeten los principios clínicos y éticos
- **Comité de Privacidad** — cumplimiento normativo, supervisión de la EIPD, respuesta a incidentes de seguridad

Las decisiones importantes siguen un proceso público de RFC (Request for Comments / Solicitud de Comentarios) en GitHub Discussions. Cada contribuidor tiene voz.

---

## Licencia

life_jorney se publica bajo la [Licencia MIT](./LICENSE).

Eres libre de usar, copiar, modificar, distribuir y desplegar este software — incluyendo uso institucional — siempre que se preserve el aviso de licencia original. El uso comercial está permitido; vender el software sin modificación significativa no está en el espíritu de este proyecto.

---

## Reconocimientos

life_jorney es construido por una comunidad global de desarrolladores, profesionales de la salud, diseñadores y pacientes que creen que la tecnología sanitaria debe servir a la humanidad — no al revés.

Cada contribuidor está listado en [CONTRIBUTORS.md](./CONTRIBUTORS.md).

---

*Si crees que la tecnología puede transformar la salud cuando se construye en abierto, este proyecto es para ti.*
