# Política de Seguridad

life_jorney maneja algunos de los datos más sensibles que existen: historiales médicos personales, diagnósticos, medicamentos e historias clínicas familiares. Una vulnerabilidad de seguridad en este sistema no es solo un problema de software — puede tener consecuencias reales para personas reales. Tomamos cada reporte en serio y estamos profundamente agradecidos con los investigadores que nos ayudan a proteger a los pacientes y sus datos.

---

## Versiones con soporte

El proyecto está actualmente en fase previa al lanzamiento. Una vez que se publiquen versiones oficiales, esta tabla reflejará cuáles reciben parches de seguridad activos.

| Versión | Estado |
|---------|--------|
| Rama `main` | Desarrollo activo — recibe todos los parches de seguridad |
| MVP (v1.0, próximamente) | Recibirá parches de seguridad |
| Versiones de desarrollo / pre-lanzamiento | No para uso en producción; las vulnerabilidades en estas versiones son igualmente bienvenidas |

---

## Cómo reportar una vulnerabilidad

**No abras un issue público, un pull request ni un hilo de Discussion en GitHub para reportar una vulnerabilidad de seguridad.** La divulgación pública antes de que exista un parche pone en riesgo a los pacientes y sus datos.

### Canal preferido

Envía tu reporte por correo electrónico a:

```
[pendiente — el dominio del proyecto aún no está definido]
[se creará un correo de seguridad dedicado y se publicará aquí antes del primer lanzamiento público]
```

Si necesitas enviar detalles técnicos sensibles (credenciales encontradas, código de prueba de concepto o evidencia de exposición de datos), puedes solicitar nuestra clave PGP pública escribiendo a esa dirección una vez que esté publicada.

### Qué incluir en el reporte

Un buen reporte nos ayuda a reproducir y solucionar el problema más rápido. Incluye todo lo que puedas de lo siguiente:

1. **Resumen:** un párrafo que describa la vulnerabilidad y su impacto.
2. **Componente afectado:** API backend, frontend web, app móvil, base de datos, infraestructura, autenticación, log de auditoría, etc.
3. **Pasos para reproducir:** una secuencia numerada y clara que demuestre la vulnerabilidad. Incluye ejemplos de peticiones/respuestas, rutas de código relevantes o detalles de configuración.
4. **Prueba de concepto:** si tienes un script de PoC, adjúntalo. No penalizamos a los investigadores de buena fe por escribir un PoC.
5. **Evaluación de impacto:** ¿qué datos o funcionalidad están en riesgo? ¿En qué condiciones? ¿Cuántos usuarios podrían verse afectados?
6. **Corrección sugerida:** opcional, pero muy apreciada si tienes una propuesta.
7. **Tus datos de contacto:** nombre o alias, y cómo prefieres que te contactemos para el seguimiento.

**Importante:** si durante tu investigación encontraste datos reales de pacientes en algún despliegue, comunícanoslo de inmediato. No copies, almacenes ni compartas esos datos. Trataremos esto con la máxima urgencia independientemente de cómo los hayas encontrado.

---

## Plazos de respuesta

Nos comprometemos a los siguientes SLA una vez recibido el reporte:

| Hito | Plazo objetivo |
|------|----------------|
| Acuse de recibo inicial | Dentro de las 72 horas |
| Evaluación de la vulnerabilidad (confirmada / no confirmada) | Dentro de 7 días |
| Clasificación de severidad comunicada al investigador | Dentro de 10 días |
| Parche para severidad Crítica o Alta | Antes del siguiente lanzamiento, o antes si hay explotación activa |
| Parche para severidad Media | Dentro de 60 días |
| Parche para severidad Baja | Dentro de 90 días |
| Divulgación pública (coordinada con el investigador) | Después de que el parche esté desplegado |

Si las circunstancias nos impiden cumplir estos plazos, te lo comunicaremos de forma proactiva. Nunca dejaremos de responder ante una vulnerabilidad confirmada.

---

## Clasificación de severidad

Utilizamos la siguiente escala para clasificar las vulnerabilidades reportadas:

| Severidad | Descripción | Ejemplos en este proyecto |
|-----------|-------------|---------------------------|
| **Crítica** | Exposición directa de datos de salud de pacientes; bypass de autenticación; capacidad de modificar registros médicos sin autorización | Acceso no autenticado al historial de un paciente; alteración del log de auditoría; bypass de los controles de consentimiento |
| **Alta** | Exposición indirecta de datos de pacientes; escalada de privilegios; controles de acceso rotos; riesgo significativo de integridad de datos | Doctor que accede a registros de pacientes que nunca dieron consentimiento; escalada al rol de supervisor; acceso de emergencia sin registro en auditoría |
| **Media** | Exposición limitada de datos; fallos de lógica que no exponen PHI directamente; configuraciones de seguridad incorrectas | Fijación de sesión; CSRF en acciones no sensibles; filtración de información en mensajes de error |
| **Baja** | Problemas menores con impacto limitado; hallazgos informativos | Dependencia desactualizada sin exploit conocido; cabeceras HTTP verbosas |

---

## Alcance

Los siguientes componentes están dentro del alcance para la investigación de seguridad:

- API REST del backend (Django / Django Rest Framework)
- Frontend web (aplicación React)
- Aplicación móvil (Flutter — Android e iOS)
- Flujos de autenticación y segundo factor (2FA)
- Lógica de gestión de consentimientos y control de acceso
- Mecanismos de integridad del log de auditoría
- Flujo de acceso de emergencia (break-glass)
- Endpoint de exportación FHIR
- Carga y almacenamiento de archivos (MinIO)
- Mecanismo de sincronización offline (almacenamiento local SQLite)
- Archivos de configuración de infraestructura en el repositorio

Los siguientes están **fuera de alcance:**

- Ataques de ingeniería social contra contribuidores o mantenedores del proyecto
- Ataques físicos contra la infraestructura
- Ataques de denegación de servicio (DoS / DDoS)
- Vulnerabilidades en dependencias de terceros que ya han sido divulgadas públicamente (repórtalas al canal de seguridad de esa dependencia y abre un issue regular de actualización con nosotros)
- Resultados de escáneres automáticos enviados sin un impacto confirmado y reproducible
- Problemas que requieren una interacción de usuario improbable o impráctica (por ejemplo, un usuario que deliberadamente configura mal su propia cuenta)

---

## Divulgación responsable y protección al investigador

Apoyamos la divulgación coordinada y responsable. Si sigues las directrices de esta política, nos comprometemos a:

- No emprender acciones legales contra ti por tu investigación, siempre que se haya realizado de buena fe y dentro del alcance definido.
- No compartir tu identidad con terceros sin tu consentimiento.
- Trabajar contigo para entender y solucionar el problema antes de cualquier divulgación pública.
- Darte crédito por el hallazgo (si lo deseas) en nuestros reconocimientos de seguridad.

Definimos la investigación de "buena fe" como: acceder únicamente a cuentas y datos que controlas o para los que tienes permiso explícito de prueba; no modificar ni eliminar datos que no te pertenezcan; no explotar una vulnerabilidad más allá de lo necesario para demostrar el impacto; y reportarnos los hallazgos de forma oportuna.

Si en algún momento durante tu investigación accedes a datos que parecen pertenecer a pacientes reales, **detente inmediatamente** y contáctanos. No trataremos esto como una violación si actúas de manera responsable.

---

## Notificación regulatoria de brechas

life_jorney opera bajo múltiples regulaciones de protección de datos. Una brecha confirmada que involucre datos personales de salud activa obligaciones de notificación obligatoria:

| Regulación | Obligación de notificación |
|------------|---------------------------|
| **GDPR** | Autoridad supervisora dentro de las 72 horas de conocer la brecha; personas afectadas sin demora indebida si existe alto riesgo |
| **HIPAA** | Personas afectadas dentro de 60 días; HHS y medios de comunicación (si >500 afectados) anualmente o dentro de 60 días |
| **Colombia Ley 1581** | SIC (Superintendencia de Industria y Comercio) según lo requerido |
| **Brasil LGPD** | ANPD y personas afectadas en un plazo razonable |

Si tu reporte revela una brecha de esta naturaleza, indícalo explícitamente. Esto afecta nuestros plazos de respuesta y obligaciones legales.

---

## Reconocimiento

life_jorney no opera actualmente un programa de recompensas económicas (bug bounty) — somos un proyecto de código abierto sin ánimo de lucro. Sin embargo, creemos que los investigadores de seguridad que ayudan a proteger a los pacientes merecen reconocimiento.

Los investigadores que divulguen de forma responsable una vulnerabilidad confirmada serán:

- Listados en nuestro [Salón de la Fama de Seguridad](./SECURITY_HALL_OF_FAME.md) (creado cuando se confirme el primer hallazgo), con su nombre o alias preferido y una descripción de su contribución.
- Agradecidos públicamente en las notas de la versión que incluya el parche (si dan su consentimiento para el crédito público).
- Considerados con prioridad para roles remunerados si el proyecto alguna vez alcanza un estado financiado que lo haga posible.

También estamos abiertos a discutir otras formas de reconocimiento — oportunidades de ponencias en conferencias, coautoría en publicaciones sobre seguridad o cartas de agradecimiento para portfolios profesionales.

---

## Contacto

| Propósito | Contacto |
|-----------|----------|
| Reportes de vulnerabilidades de seguridad | **Pendiente** — dominio aún no definido. Se publicará el correo de seguridad aquí antes del primer lanzamiento público. |
| Preguntas generales sobre seguridad (no sensibles) | Abre una [GitHub Discussion](../../discussions) |
| Violaciones del Código de Conducta | **Pendiente** — dominio aún no definido. Se publicará el correo de conducta en [CODE_OF_CONDUCT_ES.md](./CODE_OF_CONDUCT_ES.md) antes del primer lanzamiento público. |
| Preguntas generales sobre el proyecto | Abre una [GitHub Discussion](../../discussions) |

---

*Esta política se revisa y actualiza antes de cada lanzamiento mayor.*
