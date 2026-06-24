---
title: "El reinicio de la criptografía cuántica en 2026: estándares PQC, garantía de QKD y el trabajo de migración que los bancos no pueden aplazar"
subtitle: "La criptografía cuántica ha pasado de la prospectiva a la disciplina de implementación: los estándares NIST PQC están listos, la guía del NCSC británico ha estrechado las opciones de algoritmos, el trabajo protocolar del IETF todavía madura, y la garantía de QKD pasa de la confianza de laboratorio al lenguaje de certificación."
description: "La criptografía cuántica en 2026 ya no es un debate sobre la inminencia de los ordenadores cuánticos. Es un programa de migración que atraviesa la criptografía postcuántica, la cripto-agilidad, la garantía de la distribución cuántica de claves, los estándares de protocolo, la preparación de proveedores y los datos financieros de larga duración ya expuestos al riesgo «harvest-now-decrypt-later»."
date: "May 18, 2026"
language: "es-ES"
locale: "es_ES"
banner: "https://cloudcdn.pro/stocks/images/alex-shuper-YYZnrK8NrSw-unsplash.webp"
banner_alt: "Mapa de migración hacia una criptografía resistente a lo cuántico para 2026 — estándares NIST PQC, trabajo sobre protocolos híbridos, garantía de QKD, cripto-agilidad y niveles de riesgo de datos bancarios"
keywords: "criptografía cuántica 2026, criptografía postcuántica, NIST FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC PQC, IETF TLS, IPsec, RFC 9794, intercambio de claves híbrido, QKD, ETSI QKD, ISO IEC 23837, cripto-agilidad, harvest now decrypt later, HNDL, criptografía para servicios financieros, seguridad bancaria"
tags: "criptografía cuántica, criptografía postcuántica, PQC, NIST, FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC, IETF, TLS, IPsec, QKD, ETSI, cripto-agilidad, HNDL, seguridad bancaria"
item_title: "El reinicio de la criptografía cuántica en 2026: estándares PQC, garantía de QKD y el trabajo de migración que los bancos no pueden aplazar"
item_description: "El reinicio de la criptografía cuántica 2026: estándares NIST PQC, recomendaciones de migración del NCSC, preparación protocolar del IETF, garantía de QKD, cripto-agilidad y lo que los bancos deberían priorizar esta semana."
twitter_title: "Criptografía cuántica 2026: estándares PQC y migración bancaria"
twitter_description: "El reinicio de la criptografía cuántica 2026: estándares NIST PQC, recomendaciones de migración del NCSC, preparación protocolar del IETF, garantía de QKD, cripto-agilidad y lo que los bancos deberían priorizar esta semana."
---

# El reinicio de la criptografía cuántica en 2026: estándares PQC, garantía de QKD y el trabajo de migración que los bancos no pueden aplazar

La criptografía cuántica en 2026 se ha dividido en dos vías prácticas. La criptografía postcuántica es ahora un programa de implementación, porque el NIST afirma que tres estándares postcuánticos están listos para su uso y los sistemas federales deben tratarlos como estándares FIPS ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")); la distribución cuántica de claves se está convirtiendo en un problema de garantía y certificación, porque los despliegues de QKD necesitan lenguaje de evaluación, perfiles de protección y estándares operativos en lugar de demostraciones de laboratorio aisladas ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publica un perfil de protección QKD")).

---

> **Resumen ejecutivo / Conclusiones clave**
>
> - **El NIST ha pasado la PQC a fase de implementación.** Los estándares actuales son FIPS 203 para el establecimiento de claves ML-KEM, FIPS 204 para firmas ML-DSA y FIPS 205 para firmas SLH-DSA; el NIST insta a las organizaciones a identificar la criptografía vulnerable y comenzar la migración ya ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")).
> - **El NCSC británico ha estrechado las opciones prácticas.** Recomienda ML-KEM-768 y ML-DSA-65 para la mayoría de los casos de uso, advirtiendo que los sistemas deben apoyarse en implementaciones robustas de los estándares finales y no en experimentos compatibles con borradores ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos pasos para preparar la PQC")).
> - **La preparación protocolar es desigual.** El IETF está actualizando TLS e IPsec para PQC e intercambio de claves híbrido, pero el NCSC advierte que los sistemas operativos deben preferir RFC publicados antes que Internet Drafts cambiantes ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos pasos para preparar la PQC")).
> - **El esquema híbrido es un mecanismo de transición, no un estado final.** Los esquemas híbridos de clave pública más postcuántico ayudan a escalonar la migración y a cubrir el riesgo de implementación, pero añaden complejidad y pueden requerir una segunda migración hacia un esquema solo-PQC más tarde ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos pasos para preparar la PQC")).
> - **QKD no es un sustituto de la PQC.** QKD puede servir para enlaces especializados de alta garantía, pero su relevancia bancaria depende de la certificación, la interoperabilidad, el coste operativo y la integración con sistemas existentes de gestión de claves, no solo de la física ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publica un perfil de protección QKD")).
> - **La pregunta a nivel banco es el inventario.** Una institución financiera que no puede localizar RSA, ECDH, ECDSA, EdDSA, criptografía propietaria de VPN, plantillas HSM, vidas útiles de certificados y criptografía gestionada por proveedores no puede migrar, sean cuales sean los estándares disponibles.
> - **El riesgo ya está activo.** Los ataques harvest-now-decrypt-later hacen que los datos financieros de larga duración sean vulnerables antes de que existan ordenadores cuánticos criptográficamente relevantes, porque al adversario le basta con recopilar el texto cifrado hoy.
> - **La cripto-agilidad es el control duradero.** La arquitectura ganadora no es un cambio puntual de RSA a ML-KEM; es la capacidad de la plataforma de rotar algoritmos, parámetros, bibliotecas, certificados, políticas de hardware y modos de protocolo sin reconstruir el banco.
>
---

## Por qué importa esta semana

La conversación sobre estándares ha superado el punto de la abstracción. La guía pública del NIST dice que las organizaciones deben empezar a aplicar los nuevos estándares ya, identificar dónde se usan algoritmos vulnerables y planificar las actualizaciones de productos, servicios y protocolos ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Ese lenguaje importa porque convierte la PQC de un tema de investigación en una dependencia de renovación tecnológica.

El calendario también importa porque los datos financieros tienen una vida media de confidencialidad larga. Los materiales de M&A, los flujos de tesorería, las investigaciones de sanciones, los documentos de identidad de clientes, los metadatos de enrutamiento de pagos y los registros de liquidación wholesale pueden permanecer sensibles durante años. El ordenador cuántico que rompe la criptografía clásica de clave pública no necesita existir hoy para que la exposición sea racional hoy.

## La base criptográfica 2026: cuatro frentes de trabajo

### 1. Los estándares PQC están suficientemente listos para planificar

La primera base es algorítmica. El programa PQC del NIST ofrece ahora a los responsables tecnológicos objetivos con nombre: ML-KEM para establecimiento de claves, ML-DSA para firmas digitales generales y SLH-DSA para firmas basadas en hash ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos pasos para preparar la PQC")). El impacto práctico es que los equipos de compras, arquitectura y gestión de proveedores pueden dejar de preguntar si existirán estándares PQC y empezar a preguntar cuándo los soportará cada sistema.

El punto más delicado es la compatibilidad. El NCSC advierte que las implementaciones basadas en borradores pueden no ser compatibles con los estándares finales, exactamente el tipo de detalle que descarrila migraciones de grandes bancos si se ignora ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos pasos para preparar la PQC")). Los bancos deben, por tanto, separar pilotos experimentales de trayectorias de migración en producción.

### 2. Los protocolos son el cuello de botella

Los algoritmos no aseguran por sí mismos el tráfico bancario. TLS, IPsec, SSH, S/MIME, API de pagos, integraciones HSM y pilas de gestión de certificados necesitan soporte a nivel de protocolo. El NCSC indica que el IETF está actualizando protocolos ampliamente usados como TLS e IPsec para que los algoritmos PQC puedan incorporarse a los mecanismos de intercambio de claves y firma ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos pasos para preparar la PQC")).

Eso crea un problema de implementación por fases. Un banco puede inventariar la criptografía de inmediato, exigir hojas de ruta a sus proveedores de inmediato y diseñar la cripto-agilidad de inmediato, pero puede aún tener que esperar a implementaciones protocolares estables antes de mover canales de producción de alta criticidad.

### 3. QKD se convierte en disciplina de garantía

La distribución cuántica de claves sigue siendo relevante para enlaces muy especializados, en particular cuando la institución controla los extremos y las rutas de red. El desarrollo importante de 2026 no es una nueva caja QKD; es la aparición de un lenguaje de certificación, con ETSI GS QKD 016 descrito como un hito de perfil de protección para la evaluación de productos QKD ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publica un perfil de protección QKD")).

Para los bancos, esto desplaza la conversación de compra. La pregunta correcta ya no es si QKD es cuánticamente seguro en principio. La pregunta correcta es si el dispositivo, la integración, el proceso de gestión de claves, el entorno operativo y la evidencia de certificación cumplen el modelo de amenaza del banco.

### 4. La cripto-agilidad es la arquitectura

La cripto-agilidad es la capacidad de cambiar de algoritmos sin cambiar todo el sistema. Cubre bibliotecas de software, negociación de protocolo, política HSM, perfiles de certificados, vidas útiles de claves, servicios de firma, evidencia de auditoría y rutas de rollback. Sin ella, cada migración criptográfica se convierte en un proyecto a medida.

Esta es la lección arquitectónica central. La transición postcuántica no será la última transición criptográfica que afrontará el sistema financiero. Los bancos que construyan cripto-agilidad ahora obtienen un plano de control reutilizable para actualizaciones de algoritmos, riesgo de proveedor, revocación de emergencia y evidencia para el regulador.

## Qué deben hacer los bancos ahora

### Construir el inventario de activos criptográficos

El primer entregable es una lista de materiales criptográfica. Debe incluir algoritmos de clave pública, longitudes de clave, autoridades de certificación, plantillas HSM, versiones TLS, productos VPN, pasarelas de pago, API de terceros, SDK móviles, envoltorios de cifrado de datos en reposo, claves de firma, procesos de firma de firmware y criptografía gestionada por proveedores.

El inventario debe distinguir entre confidencialidad y autenticidad. Los datos cifrados de larga duración están expuestos al riesgo harvest-now-decrypt-later, mientras que las claves de firma de larga duración crean un riesgo futuro de falsificación si siguen ancladas en algoritmos de clave pública vulnerables.

### Segmentar por vida media de los datos

No todos los datos requieren el mismo orden de migración. Un mensaje de autorización de tarjeta en tiempo real puede tener una vida media de confidencialidad distinta de la de una investigación de sanciones, un archivo de adquisición corporativa, un paquete de identidad de banca privada o un documento de emisión de deuda soberana. Por eso la migración cuántica pertenece a la clasificación de datos tanto como a la seguridad de red.

La prioridad debe ser los sistemas que protegen datos de larga duración con un establecimiento de claves vulnerable. Esos son los sistemas en los que la recopilación de hoy crea la exposición de mañana.

### Forzar las hojas de ruta de proveedores en los contratos

El NIST afirma que los productos, servicios y protocolos necesitan actualizaciones para la transición ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Eso significa que el lenguaje de compras debe cambiar. Los proveedores deben revelar plazos de soporte PQC, compatibilidad con estándares finales, comportamiento en modo híbrido, restricciones de módulos hardware, impactos de rendimiento, soporte de perfiles de certificados y controles de fallback.

Un proveedor que solo dice «hoja de ruta cuántica segura» no ha respondido a la pregunta. El banco necesita fechas, algoritmos, fronteras de integración y evidencia.

## PQC, QKD e híbrido: una tabla de decisión práctica

| Control | Mejor uso | Estado 2026 | Salvedad bancaria |
|---|---|---|---|
| **ML-KEM / FIPS 203** | Establecimiento de claves para confidencialidad duradera | Estandarizado y listo para planificación de implementación ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")) | Necesita soporte de protocolos y bibliotecas antes del despliegue crítico en producción |
| **ML-DSA / FIPS 204** | Firmas digitales generales | Recomendado por el NCSC para la mayoría de los casos generales de firma ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos pasos para preparar la PQC")) | Las cadenas de certificados y la migración de PKI son operativamente difíciles |
| **SLH-DSA / FIPS 205** | Firmas basadas en hash para firmado de firmware y software | Estándar NIST final referenciado por el NCSC ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos pasos para preparar la PQC")) | Las firmas mayores pueden afectar a entornos limitados |
| **Esquemas híbridos PQ/T** | Migración intermedia e interoperabilidad | Útil como medida de transición ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos pasos para preparar la PQC")) | Añade complejidad y puede requerir una segunda migración |
| **QKD** | Enlaces especializados de alta garantía | El trabajo de garantía madura mediante la actividad de perfil de protección de ETSI ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publica un perfil de protección QKD")) | No resuelve la autenticación a escala de internet ni el inventario criptográfico de empresa |

## Qué significa por tipo de institución

### Bancos universales de primer nivel

Los bancos de primer nivel necesitan una oficina de programa, no una prueba de concepto. El modelo operativo objetivo debe combinar inventario criptográfico, exigencia a proveedores, gestión de la hoja de ruta HSM, entornos de prueba para TLS/IPsec híbridos y evidencia lista para el regulador. El trabajo temprano de mayor valor no es cambiar inmediatamente todos los cifradores; es construir el plano de control que hace seguro el cambio.

### Bancos medianos y regionales

Los bancos medianos deben tratar la PQC como un ejercicio de gestión de proveedores y estandarización de plataforma. Pueden evitar trabajo a medida costoso concentrando sistemas en torno a bibliotecas soportadas, pilas TLS estándar, servicios gestionados de certificados y plazos claros para proveedores. El riesgo clave es la criptografía oculta dentro de appliances, pasarelas de pago y middleware heredado.

### Fintechs, PSP e instituciones cripto-adyacentes

Las fintechs pueden moverse más rápido porque suelen tener menos anclajes de confianza heredados. El riesgo es la complacencia en API de terceros, valores por defecto de KMS en la nube, infraestructura de wallets e integraciones de custodia. Las firmas cripto-adyacentes deben tener especial cuidado de no confundir relatos de seguridad nativos de blockchain con preparación postcuántica.

### Ingenieros y arquitectos de seguridad

La disciplina de ingeniería es concreta: añadir metadatos de algoritmo a los inventarios de servicios, registrar los modos de protocolo negociados, crear feature flags seguros para pruebas híbridas, acortar vidas útiles de certificados cuando sea posible, eliminar suposiciones de algoritmo codificadas y hacer que la política criptográfica sea desplegable por configuración en lugar de por bifurcaciones de código.

## Conclusión

El reinicio de la criptografía cuántica no es una compra tecnológica única. Es un modelo operativo criptográfico. El NIST ha dado a la industria una base de estándares, el NCSC ha estrechado la guía práctica, los organismos de protocolos siguen moviéndose y la garantía de QKD se está formalizando. Las instituciones bancarias que ganarán esta transición no serán las que anuncien el mayor piloto. Serán las que sepan dónde vive su criptografía, qué datos necesitan protección primero y puedan cambiar las primitivas criptográficas sin reconstruir el banco.

## Preguntas frecuentes

**¿Está lista la criptografía postcuántica para que la usen los bancos?**

Está lista para planificación, compromiso con proveedores, pilotos y trabajo de implementación seleccionado. El NIST afirma que tres estándares están listos para ser implementados, mientras que el NCSC advierte que el uso operativo debe basarse en implementaciones robustas de los estándares finales y en protocolos estables ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography"), [NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos pasos para preparar la PQC")).

**¿Elimina QKD la necesidad de PQC?**

No. QKD puede ser útil para enlaces controlados especializados, pero la PQC es la trayectoria de migración escalable para software general, protocolos de Internet, API, certificados y sistemas empresariales. QKD también depende de marcos de garantía y certificación antes de poder tratarse como infraestructura de calidad bancaria ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publica un perfil de protección QKD")).

**¿Qué debe migrarse primero?**

Los sistemas que protegen datos sensibles de larga duración deben priorizarse. Eso incluye cifrado de archivos, investigaciones de pagos, documentos de tesorería y mercados de capitales, registros de identidad de banca privada, archivos de operaciones estratégicas, autoridades de certificación raíz, firmado de firmware y canales interbancarios.

**¿Cuál es la mayor trampa de implementación?**

La mayor trampa es tratar la PQC como un simple intercambio de algoritmos. La migración afecta a protocolos, certificados, HSM, proveedores, pruebas de rendimiento, respuesta a incidentes, monitorización y gobernanza. Sin cripto-agilidad, la institución simplemente recrea el mismo problema de migración para el siguiente cambio de algoritmo.

## Referencias

- NIST, (2025). [Criptografía postcuántica ⧉](https://www.nist.gov/pqc "Post-quantum cryptography").
- NCSC, (2024). [Próximos pasos para preparar la criptografía postcuántica ⧉](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC PQC guidance").
- NIST CSRC, (2026). [The NIST Post-Quantum Cryptography Project ⧉](https://csrc.nist.gov/presentations/2026/mpts2026-3b1 "The NIST PQC Project").
- ID Quantique, (2024). [ETSI publica el primer perfil de protección mundial para QKD ⧉](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD 016").
<!-- enrich-start -->
<aside class="author-card" aria-label="Acerca del autor"><img alt="Retrato de Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastienrousseau.webp" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Tecnólogo bancario sénior, escribe sobre IA aplicada, migración a ISO 20022, criptografía postcuántica para servicios financieros y la transformación estructural de los pagos wholesale.</span><span class="author-credentials">Más de 20 años en HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Perfil completo</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Última revisión <time datetime="2026-05-18">2026-05-18</time>.</p>
<!-- enrich-end -->
