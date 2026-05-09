# Guía de Contribución a life_jorney

> Nota: este documento es la versión en español de la guía de contribución del proyecto.
> GitHub detecta automáticamente el archivo `CONTRIBUTING.md` como guía principal;
> si buscas esa versión en inglés, la encontraras en `CONTRIBUTING.md` en la raíz del repositorio.

---

Gracias por tomarte el tiempo de leer esta guia. life_jorney es una plataforma de historial medico unificado, de codigo abierto y sin animo de lucro. Su razon de ser es que ninguna persona pierda una oportunidad de atencion medica por culpa de informacion fragmentada, inaccesible o perdida.

Cada linea de codigo, cada termino clinico revisado, cada pagina traducida y cada reporte de error es un paso hacia un sistema de salud mas justo y humano. Tu contribucion importa, independientemente de tu perfil o nivel de experiencia.

---

## Índice

1. [Introducción](#1-introducción)
2. [Antes de empezar](#2-antes-de-empezar)
3. [Tipos de contribuciones](#3-tipos-de-contribuciones)
4. [Cómo reportar un bug](#4-cómo-reportar-un-bug)
5. [Cómo solicitar una funcionalidad](#5-cómo-solicitar-una-funcionalidad)
6. [Flujo de trabajo de desarrollo](#6-flujo-de-trabajo-de-desarrollo)
7. [Estándares de código](#7-estándares-de-código)
8. [Contribuciones médicas y clínicas](#8-contribuciones-médicas-y-clínicas)
9. [Vulnerabilidades de seguridad](#9-vulnerabilidades-de-seguridad)
10. [Reconocimiento](#10-reconocimiento)
11. [Preguntas](#11-preguntas)

---

## 1. Introducción

life_jorney concentra en un unico repositorio todos los eventos medicos de una persona, desde antes de nacer hasta el final de su vida, con el objetivo de predecir enfermedades y mejorar la atencion sanitaria global. Los datos son sensibles, la privacidad es un pilar —no un complemento— y la interoperabilidad clinica (HL7 FHIR R4, ICD-10/11, LOINC, SNOMED CT, ATC) es obligatoria desde el primer dia.

Construir esto correctamente requiere colaboracion entre disciplinas que rara vez trabajan juntas: desarrolladores de software, medicos, enfermeros, diseñadores, investigadores en seguridad, traductores y personas de la comunidad que simplemente quieren que el proyecto mejore. Todas esas miradas son bienvenidas y necesarias.

Este documento explica como colaborar de forma efectiva, independientemente de tu perfil.

---

## 2. Antes de empezar

### 2.1 Lee el documento de ingenieria

El documento central del proyecto es `INGENIERIA_SW.md`. Contiene la vision del producto, las Historias de Usuario (HU), los Requisitos Funcionales (RF) y No Funcionales (RNF), la arquitectura, los patrones de diseño y los estandares clinicos adoptados. Antes de abrir un Pull Request o una propuesta de funcionalidad, dedica tiempo a leerlo. Muchas preguntas sobre el alcance del proyecto tienen respuesta ahi.

### 2.2 Abre una Discussion antes de cambios grandes

Si tu idea implica modificar la arquitectura, añadir una dependencia significativa, cambiar un flujo clinico, introducir un nuevo estandar o cualquier decision que afecte al proyecto de forma transversal, **abre primero una Discussion en GitHub** (pestana Discussions) antes de escribir una sola linea de codigo. Esto evita trabajo duplicado y permite que la comunidad aporte perspectivas desde el principio.

Los cambios pequeños —correcciones de errores, mejoras de documentacion, ajustes de estilo— pueden ir directamente como Pull Request.

### 2.3 Acepta el Codigo de Conducta

Al participar en este proyecto aceptas el Codigo de Conducta (`CODE_OF_CONDUCT.md`). Este es un espacio respetuoso y colaborativo. Las discusiones tecnicas pueden ser intensas; las descalificaciones personales no tienen lugar aqui.

### 2.4 Configura tu entorno local

Antes de comenzar a desarrollar, asegurate de tener instaladas las herramientas necesarias segun el area en la que vayas a trabajar:

- **Backend:** Python 3.12+, Django 5, Django REST Framework, PostgreSQL 16, Redis, Celery, MinIO
- **Web:** Node.js 20+, React 18, TypeScript 5
- **Movil:** Flutter 3 y Dart 3
- **Calidad:** Black, isort, ESLint, Prettier, dart format

Las instrucciones detalladas de instalacion y configuracion del entorno de desarrollo se encuentran en la seccion correspondiente del repositorio (cuando este disponible). Si aun no existe esa documentacion, es una excelente area en la que puedes contribuir.

---

## 3. Tipos de contribuciones

Todas las contribuciones son valiosas. La siguiente tabla describe las areas principales y el perfil de personas que pueden contribuir en cada una.

| Area | Descripcion | Perfil ideal |
|---|---|---|
| Desarrollo backend | Django 5, DRF, PostgreSQL, Redis, Celery, MinIO, APIs FHIR | Desarrolladores Python con experiencia en APIs REST y sistemas de datos sensibles |
| Desarrollo frontend web | React 18, TypeScript, accesibilidad, internacionalizacion | Desarrolladores web con interes en UX y aplicaciones criticas |
| Desarrollo movil | Flutter 3, Dart, apps iOS y Android | Desarrolladores moviles con experiencia en Flutter |
| Diseno UI/UX | Flujos de usuario, prototipos, sistemas de diseno, accesibilidad (WCAG) | Disenadores con experiencia en aplicaciones medicas o de alta responsabilidad |
| Conocimiento medico y clinico | Revision de flujos clinicos, codificacion ICD/LOINC/SNOMED, validacion de terminologia | Medicos, enfermeros, especialistas, tecnicos de laboratorio o cualquier profesional de la salud |
| Investigacion en seguridad | Revision de modelos de amenaza, auditorias, divulgacion responsable de vulnerabilidades | Investigadores en ciberseguridad, especialmente con experiencia en sistemas de salud o datos personales |
| Documentacion | Guias, tutoriales, referencias de API, documentacion de arquitectura | Cualquier persona con capacidad de comunicacion tecnica clara |
| Traduccion | Internacionalizacion de la interfaz y documentacion a otros idiomas | Personas bilingues o multilingues con atencion al detalle en terminologia medica |
| QA y pruebas | Casos de prueba manuales y automatizados, pruebas de regresion, pruebas de accesibilidad | Profesionales de QA, desarrolladores con experiencia en testing |
| Comunidad | Moderacion de foros, respuesta a preguntas, mentoria, organizacion de eventos | Cualquier persona con disposicion a ayudar y conocimiento del proyecto |

Si tu area no aparece en la tabla y crees que puedes aportar algo valioso, abre una Discussion. El proyecto esta en fase temprana y las necesidades evolucionan.

---

## 4. Como reportar un bug

### 4.1 Busca primero

Antes de abrir un issue, busca en los issues existentes. Es posible que el error ya haya sido reportado o que incluso tenga una solucion en curso.

### 4.2 Usa la plantilla de issue

Al abrir un nuevo issue de tipo "Bug report", GitHub mostrara una plantilla. Completala en su totalidad. Los reports incompletos tardan mas en resolverse o quedan sin atencion.

### 4.3 Que debe incluir un buen reporte de bug

Un reporte util incluye:

- **Descripcion clara:** que esperabas que ocurriera y que ocurrio en su lugar.
- **Pasos para reproducir:** una secuencia numerada y concreta de acciones que lleven al error. Si no se puede reproducir, es muy dificil arreglarlo.
- **Entorno:** sistema operativo, navegador o version de la app movil, version del servidor si aplica.
- **Logs relevantes:** mensajes de error, trazas de pila (stack traces), respuestas de la API. Elimina cualquier dato personal o sensible antes de pegar logs.
- **Capturas de pantalla o videos:** si el problema es visual, una imagen vale mas que mil palabras.
- **Impacto clinico potencial:** si el bug podria afectar la integridad de datos medicos o la seguridad del paciente, indicalo explicitamente. Estos issues reciben prioridad alta.

> Si el bug involucra una vulnerabilidad de seguridad, **no lo reportes como issue publico**. Lee la seccion 9 de esta guia.

---

## 5. Como solicitar una funcionalidad

### 5.1 Empieza por una Discussion

Las nuevas funcionalidades, especialmente aquellas que afectan flujos clinicos o la arquitectura, deben debatirse antes de ser comprometidas. Abre una Discussion en GitHub explicando:

- El problema que resuelve la funcionalidad (no la solucion tecnica todavia).
- A quien beneficia: pacientes, medicos, centros de salud, investigadores.
- Si existe algun estandar clinico relevante (FHIR, ICD, LOINC, SNOMED) que deba tenerse en cuenta.
- Cualquier alternativa que hayas considerado.

### 5.2 Del debate al issue formal

Una vez que haya consenso en la Discussion, se puede abrir un issue formal usando la plantilla de "Feature request". El issue debe referenciar la Discussion original y recoger los puntos acordados.

### 5.3 Ten en cuenta el alcance del MVP

life_jorney tiene un alcance inicial definido en `INGENIERIA_SW.md § 1.4`. Las propuestas que queden fuera de ese alcance no son rechazadas; se etiquetan para fases futuras. El proyecto es de largo plazo y todas las ideas bien argumentadas quedan registradas.

---

## 6. Flujo de trabajo de desarrollo

### 6.1 Fork y clonado

1. Haz fork del repositorio en tu cuenta de GitHub.
2. Clona tu fork localmente.
3. Añade el repositorio original como remote `upstream`:
   ```
   git remote add upstream https://github.com/life-jorney/life_jorney.git
   ```
4. Antes de comenzar cualquier trabajo, sincroniza con `upstream`:
   ```
   git fetch upstream
   git rebase upstream/main
   ```

### 6.2 Convencion de nombres de ramas

Usa el prefijo que corresponda al tipo de cambio, seguido de una descripcion breve en minusculas separada por guiones:

| Prefijo | Tipo de cambio | Ejemplo |
|---|---|---|
| `feat/` | Nueva funcionalidad | `feat/registro-eventos-vacunacion` |
| `fix/` | Correccion de un bug | `fix/error-validacion-fecha-nacimiento` |
| `docs/` | Documentacion | `docs/guia-contribucion-clinica` |
| `test/` | Pruebas | `test/cobertura-api-fhir-patient` |
| `chore/` | Mantenimiento, dependencias, configuracion | `chore/actualizacion-django-5-1` |
| `refactor/` | Refactorizacion sin cambio funcional | `refactor/modelo-alergias` |

Algunos ejemplos reales del proyecto:

```
feat/exportacion-fhir-r4
fix/alerta-interaccion-medicamentos
docs/integracion-loinc-laboratorio
test/consentimiento-break-glass
chore/configuracion-celery-beat
```

### 6.3 Conventional Commits

Todos los commits deben seguir el estandar [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/). El formato es:

```
<tipo>(<ambito opcional>): <descripcion en ingles>

[cuerpo opcional]

[pie opcional]
```

El tipo debe ser uno de: `feat`, `fix`, `docs`, `test`, `chore`, `refactor`, `perf`, `style`, `ci`.

La descripcion va en ingles y en imperativo presente. El cuerpo y el pie son opcionales pero recomendados cuando el cambio necesita contexto adicional.

Ejemplos correctos:

```
feat(patient): add FHIR R4 export endpoint for complete medical history

Implements GET /api/v1/patients/{id}/export/fhir that returns a FHIR
Bundle with all clinical events. Requires patient consent scope.

Closes #42
```

```
fix(medications): correct ATC code validation for combination drugs

The previous regex rejected valid ATC codes for combination products
(e.g., A10BD07). Updated validation to allow alphanumeric suffixes.
```

```
docs(contributing): add clinical contribution guide in Spanish
```

```
test(fhir): add unit tests for ImmunizationRecord serializer

Coverage for edge cases: missing lot number, partial dates (YYYY-MM
format per FHIR spec), and future administration dates.
```

```
chore(deps): upgrade Django to 5.1.4 and DRF to 3.15.2
```

Evita commits como `fix stuff`, `cambios`, `wip` o `arreglado`. Los commits son parte permanente de la historia del proyecto.

### 6.4 Proceso de Pull Request

1. Asegurate de que tu rama esta al dia con `upstream/main` antes de abrir el PR.
2. Ejecuta todas las pruebas localmente y confirma que pasan.
3. Verifica que la cobertura de pruebas no baje del 80% en el codigo que tocas.
4. Abre el Pull Request usando la plantilla proporcionada. Incluye:
   - Una descripcion clara de que cambia y por que.
   - El issue o Discussion relacionados (usa `Closes #NNN` si el PR cierra un issue).
   - Capturas de pantalla si hay cambios visuales.
   - Notas sobre posibles impactos en datos clinicos o privacidad, si aplica.
5. Los PRs requieren al menos una revision aprobatoria antes de hacer merge. Los cambios que afectan flujos clinicos requieren adicionalmente la revision de un colaborador con perfil medico o clinico.
6. Responde a los comentarios de revision con cordialidad. El objetivo es mejorar el codigo, no ganar una discusion.
7. Una vez aprobado, el merge lo hace un mantenedor del proyecto.

> Los PRs que incluyen cambios clinicos sin revision medica o que bajan la cobertura de pruebas por debajo del 80% no seran mergeados hasta que se corrijan esas situaciones.

---

## 7. Estandares de codigo

### 7.1 Python (backend Django)

- **Estilo:** PEP 8, aplicado automaticamente con `black` (linea maxima: 88 caracteres) e `isort` para ordenar imports.
- **Docstrings:** PEP 257. Todas las clases, metodos y funciones publicas deben tener docstring en **ingles**. Los docstrings explican el proposito, los parametros y el valor de retorno; no describen implementacion obvia.
- **Type hints:** obligatorios en firmas de funciones publicas.
- **Pruebas:** usa `pytest` con `pytest-django`. La cobertura minima es del 80% por modulo. Los endpoints de la API deben tener pruebas de integracion ademas de unitarias.

Ejemplo de docstring correcto:

```python
def get_patient_fhir_bundle(patient_id: int, include_family: bool = False) -> dict:
    """
    Build a FHIR R4 Bundle containing all clinical events for a patient.

    Args:
        patient_id: The internal database ID of the patient.
        include_family: If True, includes linked family medical history resources.

    Returns:
        A dict representing a valid FHIR Bundle (type=collection).

    Raises:
        Patient.DoesNotExist: If no patient with the given ID exists.
        PermissionDenied: If the requesting user lacks read consent for this patient.
    """
```

### 7.2 JavaScript y TypeScript (frontend React)

- **Estilo:** ESLint con la configuracion del proyecto + Prettier para formateo.
- **Tipado:** TypeScript estricto (`strict: true`). Evita `any`; si es inevitable, comenta el motivo.
- **Documentacion:** JSDoc para todas las funciones exportadas y componentes React publicos.
- **Pruebas:** Jest + React Testing Library. Cobertura minima del 80%.

### 7.3 Dart y Flutter (app movil)

- **Formato:** `dart format` con las opciones por defecto del proyecto.
- **Linting:** `flutter analyze` sin warnings antes de abrir un PR.
- **Documentacion:** comentarios `///` (DartDoc) en clases y metodos publicos, en ingles.
- **Pruebas:** `flutter test`. Cobertura minima del 80%.

### 7.4 Reglas generales

- **Idioma del codigo:** ingles. Nombres de variables, funciones, clases, comentarios en el codigo y docstrings van en ingles.
- **Idioma de los commits y PRs:** el titulo del commit en ingles (Conventional Commits). La descripcion del PR puede ir en espanol si el autor lo prefiere.
- **Sin datos reales de pacientes:** jamas incluyas datos medicos reales en tests, fixtures o ejemplos. Usa datos ficticios o anonimizados.
- **Privacidad en los logs:** asegurate de que ningun log, excepcion o traza de pila registre datos personales o clinicos del paciente.
- **Accesibilidad:** los componentes web y moviles deben cumplir WCAG 2.1 nivel AA como minimo.

---

## 8. Contribuciones medicas y clinicas

Esta seccion esta dirigida especialmente a profesionales de la salud: medicos, medicas, enfermeros, enfermeras, especialistas, tecnicos de laboratorio, farmaceuticos y cualquier persona con formacion o experiencia clinica. Tu aporte es tan importante como el de cualquier programador, y no necesitas saber programar para contribuir de forma significativa.

### 8.1 Por que necesitamos tu conocimiento

life_jorney modela eventos clinicos reales: consultas, diagnosticos, prescripciones, resultados de laboratorio, vacunaciones, alergias, antecedentes familiares. Si los flujos de datos, los formularios y las terminologias no reflejan la realidad de la practica clinica, el sistema sera util en teoria pero fallara en la practica.

Un medico que revisa un flujo de registro de diagnostico y señala que "en la realidad el medico necesita este campo antes que ese otro" esta aportando conocimiento que ninguna especificacion tecnica puede sustituir.

### 8.2 Como contribuir sin programar

Existen varias formas de contribuir si no tienes experiencia en desarrollo de software:

**Revision de flujos clinicos.** Abre la Discussion correspondiente o comenta en un issue donde se modele un proceso clinico (por ejemplo, el flujo de prescripcion de un medicamento o el registro de una vacuna). Describe si el flujo refleja la practica real, que pasos faltan o sobran, y que informacion es imprescindible frente a la que es opcional.

**Validacion de terminologia.** Cuando el proyecto defina que campo se codifica con que estandar (por ejemplo, usar SNOMED CT para hallazgos clinicos y LOINC para resultados de laboratorio), los profesionales de la salud pueden revisar que los codigos propuestos sean los correctos y que las descripciones sean clinicamente precisas.

**Revision de seguridad del paciente.** Señala situaciones donde el diseno actual del sistema podria conducir a errores clinicos: campos ambiguos, alertas que podrian ignorarse facilmente, ausencia de validacion critica (por ejemplo, alerta de alergia antes de prescribir).

**Documentacion clinica.** Redactar o revisar la documentacion dirigida a profesionales de la salud: manuales de uso, glosarios de terminos, explicaciones de como interpretar los datos exportados en formato FHIR.

Para cualquiera de estas contribuciones, el canal de entrada es GitHub Discussions (etiqueta `clinical-review`) o, si ya existe un issue especifico, los comentarios en ese issue.

### 8.3 Guia de codificacion clinica

El proyecto adopta los siguientes estandares de codificacion. Si propones añadir o modificar codigos clinicos, sigue estas directrices:

**ICD-10 e ICD-11 (diagnosticos)**

- Usa siempre la version mas especifica disponible. Prefiere `J45.0` (asma predominantemente alergica) a `J45` (asma) si el contexto clinico lo permite.
- Documenta la fuente: ICD-10-CM (version americana), ICD-10 de la OMS, o ICD-11 (indicar si es una migracion desde ICD-10).
- Si un codigo ICD-10 no tiene equivalente directo en ICD-11, documentalo en el issue o PR y propone el codigo ICD-11 mas apropiado con una breve justificacion.

**LOINC (observaciones y resultados de laboratorio)**

- Consulta la base de datos oficial de LOINC (loinc.org) para verificar que el codigo y el nombre largo (Long Common Name) son correctos.
- Especifica las seis partes del codigo LOINC cuando propongas uno nuevo: componente, propiedad, tiempo, sistema, escala y metodo.
- Si el resultado tiene unidades, indica las unidades UCUM correspondientes.

**SNOMED CT (hallazgos clinicos, procedimientos, morfologia)**

- Usa el codigo de concepto (Concept ID) y el termino preferido en el idioma correspondiente.
- Indica la jerarquia del concepto (hallazgo clinico, procedimiento, estructura corporal, etc.).
- Si existe un subconjunto nacional (por ejemplo, SNOMED CT en Espanol), menciona si el termino preferido difiere del termino internacional.

**ATC (medicamentos)**

- Usa el codigo ATC completo de cinco niveles (por ejemplo, `C10AA01` para simvastatina).
- La fuente de referencia es la base de datos de la OMS (whocc.no/atc_ddd).

Para proponer la adopcion de un nuevo codigo o corregir uno existente, abre un issue con la etiqueta `clinical-terminology` e incluye: el codigo actual (si existe), el codigo propuesto, la justificacion clinica y la fuente de referencia.

### 8.4 Proceso de revision clinica

Cualquier cambio que afecte un flujo clinico, un modelo de datos clinicos o la codificacion de terminos medicos debe pasar por una revision clinica antes del merge. Esto significa:

1. El PR debe etiquetarse con `needs-clinical-review`.
2. Al menos un colaborador con perfil clinico verificado debe aprobar el cambio o dar el visto bueno mediante comentario.
3. Si no hay disponibilidad de revisores clinicos en un plazo razonable, el mantenedor puede pedir ayuda en la Discussion correspondiente para convocar voluntarios.

El objetivo no es crear burocracia sino garantizar que los datos medicos del sistema sean clinicamente correctos y seguros para los pacientes.

---

## 9. Vulnerabilidades de seguridad

life_jorney maneja datos de salud altamente sensibles. La seguridad no es negociable.

**Si encuentras una vulnerabilidad de seguridad, NO abras un issue publico en GitHub.** Un issue publico expone la vulnerabilidad antes de que pueda ser corregida, poniendo en riesgo a los usuarios del proyecto.

### 9.1 Como reportar una vulnerabilidad

Envía un correo electrónico a la dirección publicada en [SECURITY_ES.md](./SECURITY_ES.md).

> **Nota:** el dominio del proyecto aún no está definido. Se creará un correo de seguridad dedicado una vez que se establezca el dominio, y se publicará en [SECURITY_ES.md](./SECURITY_ES.md) antes del primer lanzamiento público. Consulta ese archivo para obtener la dirección de contacto más actualizada.

El correo debe incluir:

- Una descripcion clara de la vulnerabilidad.
- Los pasos para reproducirla (tan detallados como sea posible).
- El impacto potencial: que datos podrian verse afectados, que usuarios, que tipo de ataque es posible.
- Si tienes una propuesta de correccion o mitigacion, incluyela.
- Tu informacion de contacto para que el equipo pueda responderte.

Si prefieres cifrar tu comunicacion, indica en el correo que deseas recibir una clave PGP publica para el intercambio.

### 9.2 Proceso de divulgacion responsable

El proyecto sigue un proceso de divulgacion responsable (responsible disclosure):

1. Acuse de recibo: el equipo respondera en un plazo maximo de 72 horas desde la recepcion del reporte.
2. Evaluacion: se evaluara la severidad y el impacto de la vulnerabilidad. El investigador sera informado del resultado.
3. Correccion: el equipo trabajara en una correccion con la maxima prioridad segun la severidad.
4. Coordinacion: se coordinara con el investigador la fecha de divulgacion publica, normalmente una vez que la correccion este disponible.
5. Reconocimiento publico: salvo que el investigador prefiera el anonimato, su nombre aparecera en el aviso de seguridad publico y en `CONTRIBUTORS.md`.

Comprometemos a no emprender acciones legales contra investigadores que reporten vulnerabilidades de buena fe siguiendo este proceso.

---

## 10. Reconocimiento

Toda persona que contribuya al proyecto, en cualquiera de sus formas, queda registrada en `CONTRIBUTORS.md` en la raíz del repositorio.

### 10.1 Como se reconoce cada tipo de contribucion

El proyecto sigue el estandar [All Contributors](https://allcontributors.org/) para reconocer tipos de contribucion diversos mas alla del codigo:

| Tipo de contribucion | Simbolo en CONTRIBUTORS.md |
|---|---|
| Codigo (backend, frontend, movil) | code |
| Diseno UI/UX | design |
| Documentacion | doc |
| Traduccion | translation |
| Revision clinica y conocimiento medico | medical |
| Investigacion en seguridad | security |
| Reporte de bugs | bug |
| Respuesta a preguntas en la comunidad | question |
| Pruebas y QA | test |
| Ideas y propuestas | ideas |

### 10.2 Creditos en releases

Las notas de cada release mencionan a los contribuidores cuyo trabajo esta incluido en esa version.

### 10.3 Una nota sobre la gratitud

life_jorney no tiene financiacion comercial. Quienes contribuyen lo hacen porque creen que los datos medicos pertenecen a las personas y que la tecnologia puede mejorar la atencion sanitaria global. Ese compromiso merece reconocimiento explicito y permanente.

---

## 11. Preguntas

Si tienes cualquier duda sobre el proyecto, el proceso de contribucion, los estandares clinicos o cualquier otro aspecto, el canal principal es **GitHub Discussions**:

- Para dudas tecnicas de desarrollo: etiqueta `development`
- Para preguntas sobre flujos o terminologia clinica: etiqueta `clinical-review`
- Para propuestas de nuevas funcionalidades: etiqueta `feature-idea`
- Para dudas generales sobre el proyecto: etiqueta `general`

Intenta buscar si tu pregunta ya tiene respuesta antes de abrir una nueva discusion. Las preguntas bien formuladas ayudan a toda la comunidad, porque quedan indexadas y disponibles para quien llegue despues con la misma duda.

Bienvenido o bienvenida a life_jorney. Nos alegra tenerte aqui.

---

*Este documento es mantenido por la comunidad de life_jorney. Si encuentras algo incorrecto, desactualizado o que podria explicarse mejor, abre un PR con la etiqueta `docs`.*
