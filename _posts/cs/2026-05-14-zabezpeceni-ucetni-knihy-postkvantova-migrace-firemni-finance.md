---
title: "Asegurar el libro contable: guía para consejos de administración sobre la migración postcuántica en banca corporativa"
subtitle: "El riesgo cuántico ha pasado de la curiosidad académica a un mandato normativo activo. La hoja de ruta del G7, BIS Project Leap y los calendarios UE/UK/Australia plantean ya la cuestión no del cuándo, sino del cómo."
description: "El riesgo cuántico ha pasado de la curiosidad académica al mandato normativo. Con la hoja de ruta del G7 de enero de 2026, calendarios UE, UK y australiano ahora aclarados, y BIS Project Leap que ha demostrado la viabilidad en un sistema de pago real, la cuestión para los consejos de administración ya no es la migración, sino los plazos."
date: "May 14, 2026"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Puerta de caja fuerte abierta bañada en luz dorada — metáfora visual de la protección criptográfica de los archivos financieros"
keywords: "criptografía postcuántica, ML-KEM, ML-DSA, FIPS 203, FIPS 204, BIS Project Leap, G7 CEG, NCSC, ANSSI, BSI, ASD, CNSA 2.0, agilidad criptográfica, banca corporativa, pagos wholesale"
---


> **TL;DR.** Tento článek je DRAFT překlad původně španělského zdroje, čekající na revizi rodilým mluvčím. Hlavní obsah, příklady a citace zůstávají ve španělštině; pouze záhlaví/frontmatter byly přepnuty na češtinu.

**Klíčové body**

El riesgo cuántico ha pasado de la curiosidad académica al mandato normativo activo. Con la hoja de ruta del G7 publicada en enero de 2026, los calendarios de la UE, el Reino Unido y Australia ahora aclarados, y BIS Project Leap que ha demostrado la viabilidad en un sistema de pago real, la cuestión para los consejos de administración ya no es si hay que migrar, sino si la migración puede completarse antes de que la vida útil criptográfica de los datos de hoy expire.

---

> **TL;DR.** La preparación postcuántica ha pasado en 2026 de hoja de ruta a obligación. Los consejos de administración deben tratar la migración como una decisión de gestión de riesgos sistémicos, anclada en ML-KEM y ML-DSA, desplegada de forma híbrida, y secuenciada con suficiente antelación para preceder a un CRQC plausible y a las exigencias normativas más estrictas aplicables.
>
> **Conclusiones clave**
>
> - **2026 es el año en que la postura normativa se ha endurecido.** La hoja de ruta de enero del Cyber Expert Group del G7, el calendario coordinado del Grupo de cooperación NIS de la UE y el plan en tres fases del NCSC británico han hecho pasar la conversación de la sensibilización a la ejecución. La Australian Signals Directorate va aún más lejos al fijar una fecha límite firme a 2030 para la criptografía asimétrica clásica.
> - **La exposición es asimétrica.** RSA, ECC y Diffie–Hellman constituyen el problema inmediato: los algoritmos asimétricos que sustentan los handshakes SWIFT, TLS, las PKI, la firma de código y la autenticación de las redes de compensación. El cifrado simétrico (AES-256) sigue siendo estable si se mantiene la longitud de las claves. La atención del consejo debe centrarse en la superficie asimétrica.
> - **«Cosechar ahora, descifrar más tarde» no es un escenario futuro.** Adversarios interceptan y almacenan ya hoy registros financieros cifrados, registros de liquidación, expedientes de M&A y datos de transferencias transfronterizas, con la intención explícita de descifrarlos una vez que exista un ordenador cuántico criptográficamente relevante (CRQC). Para datos sujetos a una exigencia de confidencialidad de 10 a 20 años, este riesgo ya se ha materializado.
> - **La industria dispone ahora de un punto de referencia operativo.** [BIS Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), publicado en diciembre de 2025, sustituyó con éxito las firmas digitales tradicionales por criptografía postcuántica en transferencias de liquidez en producción a través de TARGET2, y ha hecho aflorar los costes de ingeniería específicos (latencia de verificación, tamaño de paquetes) a los que se enfrentará cualquier programa de migración.
> - **La suite NIST es el ancla mundial.** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") y FIPS 204 (ML-DSA) son referenciados por todas las jurisdicciones principales, incluso cuando las posiciones nacionales divergen sobre los conjuntos de parámetros y las exigencias híbridas. Los consejos deberían considerar ML-KEM-768 / ML-DSA-65 como suelo y ML-KEM-1024 / ML-DSA-87 como referencia conservadora para los datos de larga vida útil.
> - **El híbrido es la única vía creíble.** Ninguna autoridad principal recomienda la bascula directa. Hacer funcionar clásico y resistente a lo cuántico en paralelo es el esquema de despliegue validado por el NCSC, el ANSSI, el BSI, y demostrado en Project Leap. Es más pesado que cualquiera de las alternativas, pero es la única que aborda a la vez la compatibilidad de hoy y la amenaza de mañana.

---

## El año en que la postura normativa se ha endurecido

Durante la mayor parte de la última década, la criptografía postcuántica vivía en una esquina cómoda de la hoja de ruta a largo plazo. Los ordenadores cuánticos eran impresionantes pero lejanos; la matemática criptográfica subyacente a RSA y a las curvas elípticas se trataba como sustrato estable; y la conversación sobre la migración se mantenía en gran medida confinada a grupos de trabajo especializados. Esa posición ya no es sostenible.

En enero de 2026, el [Cyber Expert Group del G7 publicó su declaración más consecuente hasta la fecha ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement on Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector"), copresidida por el Tesoro estadounidense y el Banco de Inglaterra. El documento no es una regulación, pero pesa más que una orientación clásica: representa la posición compartida de los ministerios de Finanzas, bancos centrales y autoridades de supervisión de las jurisdicciones del G7, según la cual la transición criptográfica es ahora una cuestión de gestión de riesgos sistémicos. La hoja de ruta alinea su horizonte de planificación con mediados de la década de 2030, animando a los sistemas financieros críticos a migrar antes, una formulación que, en el idioma prudente de los banqueros centrales, señala una expectativa más que una sugerencia.

Dos meses antes, el BIS Innovation Hub y el Eurosistema publicaron los resultados de [Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), una experimentación técnica que sustituyó las firmas digitales tradicionales por criptografía postcuántica en transferencias de liquidez en producción entre la Banca d'Italia, la Banque de France, la Deutsche Bundesbank, Nexi-Colt y Swift. La conclusión principal fue un éxito: transferencias firmadas resistentes a lo cuántico atravesaron de extremo a extremo un sistema de pago operativo. El detalle bajo el titular es más instructivo, y se examina más adelante en este artículo.

La combinación de estos dos eventos —un marco político coordinado del G7 y una prueba operativa en un sistema de pago real— ha producido lo que la comunidad técnica esperaba desde hace una década: una respuesta definitiva a la pregunta «¿es esto real?». La respuesta, en mayo de 2026, es sí. La cuestión que queda es la del ritmo.

## Tres vectores de amenaza que deben preocupar al consejo

Antes de discutir la mecánica de migración, conviene ser preciso sobre lo que está concretamente en juego. El riesgo cuántico en banca corporativa no es uniforme en todo el parque criptográfico, y la atención del consejo se dirige mejor a los tres vectores donde la exposición es más aguda.

### 1. Cosechar ahora, descifrar más tarde (HNDL)

La preocupación más inmediata no es futura. Es presente. Adversarios de nivel estatal y organizaciones criminales sofisticadas interceptan y almacenan sistemáticamente el tráfico financiero cifrado —transferencias, flujos de mensajes SWIFT, comunicaciones M&A, registros de liquidación transfronteriza, contratos de swap y archivos KYC— sin capacidad actual de leerlos. Su objetivo es simple: almacenar ahora, descifrar más tarde, una vez que exista un CRQC. Como [señaló explícitamente el Banco de Pagos Internacionales ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), esa recopilación ya está en curso.

Para los consejos, la implicación es incómoda pero precisa: cualquier dato sensible transmitido hoy bajo cifrado asimétrico clásico, cuya exigencia de confidencialidad se extienda más allá de la llegada de un CRQC, ya debe considerarse expuesto. No hay notificación de brecha cuando ocurre un HNDL. No hay alerta SIEM. El cifrado se sostiene —de momento— pero los datos ya han salido del perímetro.

### 2. Riesgo de sensibilidad a largo plazo

Los datos de banca corporativa tienen vidas útiles institucionales inusualmente largas. La documentación de M&A estratégica puede seguir siendo sensible al mercado durante una década. Las comunicaciones sobre secretos industriales y las valoraciones de propiedad intelectual pueden seguir siendo confidenciales durante quince a veinte años. Los registros de liquidación transfronteriza, las exposiciones de contrapartes centrales y las evaluaciones de crédito de contrapartes conservan una sensibilidad comercial mucho más allá de su vida transaccional inmediata.

La [ecuación de Mosca ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), formulada originalmente por Michele Mosca y ahora integrada en todo marco de migración serio, formaliza el problema. Si **S** es la vida útil de los datos, **M** es el tiempo necesario para migrar los sistemas que los protegen y **Q** es el tiempo antes de que un CRQC esté disponible, entonces:

```
Si S + M > Q, los datos ya están expuestos.
```

Para datos cuyo horizonte de confidencialidad es de veinte años y un programa de migración que requiere razonablemente cinco a siete años, el valor Q implícito sobre el que apuesta el consejo es de al menos 25 años. Un cuerpo creciente de evaluaciones de expertos —las [predicciones APAC 2026 de Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), las encuestas anuales del Global Risk Institute y un artículo de arquitectura de febrero de 2026 que propone un CRQC con unos 100.000 qubits físicos utilizando códigos QLDPC— sugiere que esa apuesta es imprudente.

### 3. La vulnerabilidad de los handshakes centrales

El tercer vector es el más significativo arquitectónicamente. Los cifrados simétricos (AES-256) siguen siendo comparativamente estables; el algoritmo de Grover divide a la mitad el nivel de seguridad efectivo, pero duplicar la longitud de clave restaura el margen. La exposición catastrófica concierne a los algoritmos asimétricos, y son precisamente los algoritmos que sustentan todo handshake autenticado en banca corporativa: RSA en la infraestructura de claves públicas SWIFT, ECDSA en la autenticación cliente/servidor TLS, ECDH en el establecimiento de claves de sesión, y las variantes ECC por todas partes en la autenticación móvil del cliente, las firmas de API y las cadenas de firma de código.

Un CRQC funcional que ejecute el algoritmo de Shor no debilita progresivamente esos sistemas. Los rompe. Una vez que un CRQC sea operativo, cualquier handshake protegido por RSA, cualquier firma ECDSA y cualquier intercambio de clave por curva elíptica se vuelven recuperables, no después de meses de esfuerzo, sino en cuestión de horas. La transición de «seguro» a «comprometido» es binaria, y se propaga simultáneamente a través de cada sistema que utilice el algoritmo afectado. Ese es el fundamento sobre el que descansa la urgencia normativa.

## Endurecimiento normativo: panorama por jurisdicción

El panorama normativo mundial en mayo de 2026 ya no es un mosaico de sugerencias. Es un conjunto coordinado de calendarios que varían en rigor pero convergen hacia el mismo destino. Un banco multinacional que opere en las principales plazas financieras está sometido ahora a la jurisdicción aplicable más estricta, no a la más permisiva.

### Estados Unidos

Estados Unidos tiene la posición más prescriptiva para cualquier institución que toque sistemas federales. La [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") de la NSA impone ML-KEM-1024 y ML-DSA-87 para los sistemas de seguridad nacional, debiendo los nuevos sistemas desplegar la PQC a partir de enero de 2027 y debiendo completarse la migración de la infraestructura para 2035. El Memorándum OMB M-23-02 vincula a las agencias federales a la misma trayectoria. Para los bancos comerciales, la exposición inmediata pasa por las cadenas de compras federales, los contratos adyacentes a los NSS, y la presión indirecta que las orientaciones de la NSA ejercen sobre el mercado más amplio.

### Unión Europea

La UE opera en tres capas. La [hoja de ruta coordinada de implementación de la Comisión Europea ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), elaborada por el Grupo de cooperación NIS en junio de 2025, fija hitos por fases en 2026 (estrategias nacionales), 2030 (sistemas de alto riesgo migrados) y 2035 (transición completa). El Cyber Resilience Act impondrá actualizaciones de seguridad al estado del arte para los productos digitales a partir de finales de 2027. NIS2 refuerza la gestión de riesgos ICT, aunque ninguna de las dos directivas contiene una exigencia PQC explícita. Los reguladores nacionales, por su parte, han adelantado a la Comisión. El BSI alemán impone el intercambio de claves híbrido y aprueba un panel conservador de ML-KEM, FrodoKEM y Classic McEliece. La ANSSI francesa exige el híbrido tanto para la encapsulación de claves como para las firmas. La NLNCSA neerlandesa y las autoridades noruegas se han alineado con ML-KEM-1024 como referencia conservadora para los datos de larga vida útil.

### Reino Unido

El NCSC británico publicó sus orientaciones definitivas en marzo de 2025 y las reafirmó mediante el Annual Review 2025. El calendario en tres fases es explícito:

- **Hasta 2028**: identificar los servicios criptográficos que requieren actualización, construir el plan de migración y producir un inventario criptográfico completo.
- **2028 a 2031**: ejecutar las actualizaciones prioritarias, en particular sobre los sistemas críticos y los protocolos de Internet expuestos.
- **2031 a 2035**: completar la migración en el conjunto de sistemas, servicios y productos.

Para las instituciones financieras británicas, las [orientaciones PQC del CMORG (Cross-Market Operational Resilience Group) ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") se inscriben junto al marco NCSC, tratan a los bancos como infraestructura nacional crítica y ponen el énfasis en la disponibilidad de proveedores y la alineación de la cadena de suministro.

### Asia-Pacífico

La postura APAC es más fragmentada pero evoluciona rápido. La ASD australiana tiene la posición más dura a nivel mundial: la criptografía de clave pública clásica ya no debe utilizarse más allá de finales de 2030, sin recomendación híbrida, y ML-KEM-1024 requerido (ML-KEM-768 aceptable solo hasta 2030). Las organizaciones deberían disponer de un plan de transición afinado para finales de 2026. La Monetary Authority de Singapur ha publicado orientaciones formales de preparación cuántica. Japón y Corea del Sur invierten sustancialmente, aunque los dos países disponen de filiales algorítmicas nacionales (Corea ha seleccionado NTRU+ y SMAUG-T como KEM, ALMer y HAETAE como firmas). La National Quantum Mission india, dotada de una asignación gubernamental de 6.003,65 crores de rupias, identifica explícitamente los servicios bancarios y financieros como prioridad estratégica. Las [predicciones APAC 2026 de Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") evalúan en más del 90 % el número de empresas regionales que deben invertir en tecnologías postcuánticas este año.

### La posición neta

Para un consejo de administración, la síntesis práctica de esas posiciones jurisdiccionales es directa. Un banco multinacional no puede gestionar el calendario de un solo regulador; debe gestionar el más estricto aplicable. Para la mayoría de las grandes instituciones, esto significa un horizonte de planificación de finales de 2030 para los sistemas de alto riesgo y finales de 2035 para la larga cola; las entidades expuestas a la ASD apuntando a la PQC pura para 2030 y las expuestas a la CNSA apuntando a la misma ventana con ML-KEM-1024 y ML-DSA-87 específicamente.

## BIS Project Leap: lo que la industria ha probado realmente

Project Leap merece la atención del consejo no porque sea un hito de marketing, sino porque se trata de la demostración de extremo a extremo más creíble hasta la fecha de la criptografía postcuántica en un sistema de pago financiero en producción. La conclusión principal es directa: funciona. El detalle subyacente es donde residen las implicaciones operativas.

La Fase 1, completada en 2023, estableció una VPN resistente a lo cuántico entre los sistemas IT de la Banque de France y la Deutsche Bundesbank, con mensajes de pago transmitidos entre París y Fráncfort bajo un esquema de cifrado híbrido. La Fase 2, completada a finales de 2025 y [publicada en diciembre ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), fue considerablemente más allá. El consorcio sustituyó las firmas digitales tradicionales basadas en RSA por firmas postcuánticas en la ejecución de transferencias de liquidez a través de TARGET2, el sistema de liquidación bruta en tiempo real del Eurosistema. Los participantes —el BIS Innovation Hub Eurosystem Centre, la Banca d'Italia, la Banque de France, la Deutsche Bundesbank, Nexi-Colt (que proporciona la conectividad TARGET2) y Swift— representan precisamente las instituciones cuya infraestructura tendrá que migrar eventualmente.

El informe hizo aflorar tres constataciones que todo programa de migración debería integrar:

- **La latencia de verificación es sensiblemente más elevada.** La verificación de firma postcuántica llevó materialmente más tiempo que la verificación basada en RSA en el mismo hardware. Para un sistema RTGS diseñado en torno a un tratamiento de mensajes por debajo del segundo, no es una observación marginal; es un dato de planificación de capacidad.
- **Los tamaños de paquete exigen una refactorización del sistema.** Las firmas PQC son un orden de magnitud mayores que los equivalentes ECDSA (véase más abajo). Los sistemas de pago cuyas colas internas, herramientas de supervisión y esquemas de base de datos se han dimensionado para mensajes de tamaño heredado no pueden acomodar la nueva carga útil sin refactorización. Project Leap constató explícitamente que TARGET2 no podía «acomodar fácilmente» el modelo híbrido sin reingeniería sustancial.
- **El híbrido es la respuesta correcta, pero más pesado.** Ejecutar clásico y postcuántico en paralelo preservó la retrocompatibilidad y proporcionó defensa en profundidad, pero duplicó el coste del tratamiento criptográfico. Es el coste operativo de hacer PQC correctamente durante la transición; no es evitable solo mediante ingeniería astuta.

Para un director financiero que examine un caso de inversión PQC, las constataciones de Project Leap son útiles precisamente porque son precisas. El coste de la migración postcuántica no es una sola línea capex. Es una latencia de verificación que se propaga en los contratos SLA, una expansión del tamaño de mensajes que afecta a los presupuestos de almacenamiento y ancho de banda, y un periodo transitorio de operaciones criptográficas duplicadas que afecta a la planificación de capacidad de cálculo. Ninguno de estos puntos es especulativo. Se han medido en un sistema de banco central en producción.

## La caja de herramientas NIST: ML-KEM y ML-DSA comparados

La pieza maestra técnica de todo marco nacional creíble es la suite NIST de estándares postcuánticos publicada en agosto de 2024. Dos de esos estándares están en el centro de atención para la banca corporativa: ML-KEM (FIPS 203) para la encapsulación de claves y ML-DSA (FIPS 204) para las firmas digitales. Comparten un fundamento matemático —ambos se apoyan en la dificultad de los problemas Module Learning With Errors (ML-LWE) y Module Short Integer Solution sobre retículos estructurados— pero desempeñan papeles muy distintos en el parque criptográfico, y sus perfiles de rendimiento y tamaño difieren materialmente.

### ML-KEM (FIPS 203) — encapsulación de claves

ML-KEM, derivado de [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html), es el reemplazo de ECDH y de RSA-KEM en los protocolos en los que dos partes deben establecer una clave simétrica compartida sobre un canal no seguro. Es, en la práctica, adonde van los handshakes TLS tras la retirada de RSA y de ECDH. NIST define tres conjuntos de parámetros con fuerza de seguridad creciente y rendimiento decreciente: ML-KEM-512 (NIST Categoría 1), ML-KEM-768 (Categoría 3) y ML-KEM-1024 (Categoría 5).

### ML-DSA (FIPS 204) — firmas digitales

ML-DSA, derivado de CRYSTALS-Dilithium, es el reemplazo de las firmas RSA y ECDSA. Soporta la firma de certificados, la firma de código, la firma de documentos y la autenticación. Los tres conjuntos de parámetros son ML-DSA-44, ML-DSA-65 y ML-DSA-87, correspondientes en líneas generales a las NIST Categorías 2, 3 y 5.

### Perfil de tamaño y rendimiento

Para un CIO que dimensione la capacidad de migración, las cifras más importantes son los tamaños de artefactos. Son las entradas para la planificación de capacidad de red, las proyecciones de almacenamiento y las pruebas a nivel de protocolo.

| Algoritmo | Clave pública | Criptograma / Firma | Equivalente clásico más cercano | Tamaño vs clásico |
|---|---|---|---|---|
| ML-KEM-512 | 800 bytes | 768 bytes (criptograma) | ECDH P-256 (~32 bytes clave pub) | ~25× mayor |
| ML-KEM-768 | 1.184 bytes | 1.088 bytes (criptograma) | ECDH P-384 | ~25× mayor |
| ML-KEM-1024 | 1.568 bytes | 1.568 bytes (criptograma) | ECDH P-521 | ~25× mayor |
| ML-DSA-44 | 1.312 bytes | ~2.420 bytes (firma) | ECDSA P-256 (firma 64 bytes) | ~38× mayor |
| ML-DSA-65 | 1.952 bytes | ~3.293 bytes (firma) | ECDSA P-384 | ~50× mayor |
| ML-DSA-87 | 2.592 bytes | ~4.595 bytes (firma) | ECDSA P-521 | ~70× mayor |

*Fuente: síntesis de las especificaciones [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") y FIPS 204, con datos comparativos procedentes de la literatura de benchmarking independiente.*

Tres implicaciones operativas se derivan directamente de ello. **Primero**, el tamaño de firma es la restricción limitante para la mayoría de despliegues empresariales. Una firma ML-DSA-65 es unas cincuenta veces el tamaño de una firma ECDSA P-256, y las cadenas de certificados TLS que llevan CA intermedias crecen proporcionalmente. El trabajo de capacidad sobre esa superficie no es opcional, es estructurador. **Segundo**, ML-KEM es competitivo en cálculo con ECDH y, en algunas implementaciones, materialmente más rápido, en particular en hardware que dispone de soporte vectorial para la aritmética de retículos subyacente. **Tercero**, la verificación ML-DSA es constantemente rápida (a menudo más rápida que la verificación ECDSA), pero la firma ML-DSA implica un bucle de rejection sampling que puede requerir varios intentos en hardware restringido. Para los servicios de firma de alto rendimiento, es un benchmark a verificar más que a presumir.

### Elegir los conjuntos de parámetros

Las posiciones jurisdiccionales sobre la elección de los parámetros no son idénticas, pero la convergencia es clara. ML-KEM-768 y ML-DSA-65 constituyen el suelo empresarial —validados por el NCSC británico como referencia para las organizaciones británicas y aceptables en la mayoría de marcos europeos—. ML-KEM-1024 y ML-DSA-87 son el techo conservador —impuestos por la CNSA 2.0 de la NSA para los sistemas de seguridad nacional estadounidenses y requeridos por la ASD para las entidades australianas reguladas para 2030—. Para los datos de sensibilidad extremadamente larga —registros de liquidación soberanos, propiedad intelectual con horizonte decenal, registros de custodia para instrumentos de largo vencimiento— los conjuntos de parámetros superiores son el valor por defecto defendible.

### Un fundamento matemático compartido, un riesgo compartido

Un punto digno de la atención del consejo: ML-KEM y ML-DSA extraen ambos su seguridad de la misma familia de problemas sobre retículos. Un avance criptoanalítico futuro contra Module-LWE afectaría a los dos estándares simultáneamente. Es precisamente por ello por lo que varias autoridades nacionales —notablemente el BSI alemán y la ANSSI francesa— recomiendan complementar la pila basada en retículos con firmas basadas en funciones de hash (SLH-DSA, FIPS 205) para los casos de uso de firma a largo plazo y firma de código. La agilidad criptográfica, en este sentido, no es solo la capacidad de reemplazar RSA por ML-KEM. Es la capacidad de reemplazar un algoritmo PQC por otro cuando el panorama criptoanalítico evolucione.

## Un camino de migración lógico: Descubrimiento → Triaje → Despliegue híbrido

Para un consejo que apruebe un programa PQC plurianual, la cuestión operativa es cómo escalonar el trabajo sin asumir un riesgo inaceptable de disponibilidad de servicio. El esquema que ha emergido a través de la hoja de ruta del G7, el marco NCSC, BIS Project Leap y los documentos de orientación nacionales principales converge en tres fases.

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│ 1. DESCUBRIMIENTO &  │ → │ 2. TRIAJE (MOSCA)    │ → │ 3. DESPLIEGUE        │
│    CBOM              │   │ Priorización por     │   │    HÍBRIDO           │
│ Inventario cripto    │   │ riesgo según vida    │   │ Doble sobre clásico  │
│ en todos los sistemas│   │ útil de los datos    │   │ + PQC, cripto-ágil   │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### Fase 1 — Descubrimiento y nomenclatura criptográfica (CBOM)

No se puede planificar la migración de un parque criptográfico que no ha sido cartografiado, y la mayoría de instituciones no disponen de un mapa exacto. La primera fase es por tanto la producción de una Cryptographic Bill of Materials —un inventario estructurado de cada instancia de criptografía asimétrica en la organización, etiquetada cada instancia por algoritmo, longitud de clave, contexto protocolar, sensibilidad de los datos y propietario del sistema—. El escaneo automatizado sobre las bases de código, aplicaciones web, imágenes de contenedores, configuraciones de bases de datos, almacenes de certificados, módulos HSM e interfaces de proveedor es el mecanismo práctico; el inventario manual de los sistemas heredados y los protocolos propietarios es el complemento inevitable.

La salida de la Fase 1 no es glamurosa, pero es el único fundamento sobre el que las Fases 2 y 3 pueden descansar. Es también el entregable que la mayoría de funciones de auditoría interna y reguladores externos buscarán primero cuando se empiecen a pedir las atestaciones de cumplimiento PQC.

### Fase 2 — Triaje de riesgos con la ecuación de Mosca

Una vez la CBOM en mano, la institución puede aplicar el marco de Mosca activo por activo. Para cada dependencia criptográfica, la cuestión es si **S + M > Q** —si la vida útil de los datos más el tiempo de migración supera el tiempo estimado hasta un CRQC—. Los activos donde la desigualdad es más aguda —datos sensibles de larga vida útil sobre una infraestructura que tarda años en migrar— pasan al frente de la fila. Los activos con vidas útiles de datos cortas o una infraestructura ya modernizada pueden secuenciarse más tarde en el programa.

Esta es la fase donde el apetito de riesgo del consejo es más visible. El valor Q que la institución elige como objetivo de planificación es, en efecto, una apuesta estratégica sobre el ritmo de los progresos del hardware cuántico. Una Q conservadora (mediados de la década de 2030) produce un plan de migración más agresivo y una línea capex a corto plazo más alta. Una Q optimista (post-2040) produce un plan más relajado y una exposición residual más alta a los datos ya cosechados. Ninguna está equivocada; ambas deberían ser decisiones explícitas del consejo, no defectos implícitos de la función tecnológica.

### Fase 3 — Despliegue híbrido

Una vez identificados los activos prioritarios, el despliegue debería seguir el esquema híbrido demostrado en Project Leap y validado por el NCSC, la ANSSI, el BSI y la hoja de ruta del G7. Un despliegue híbrido hace funcionar un algoritmo clásico y un algoritmo postcuántico en paralelo, combinando sus salidas en una sola envolvente. El compuesto es seguro contra los ataques clásicos (el algoritmo clásico se sostiene hoy) y contra los ataques cuánticos (el algoritmo PQC se sostiene mañana). Concretamente, el esquema habitual es X25519 combinado con ML-KEM-768 o ML-KEM-1024 para la encapsulación de claves, y ECDSA combinado con ML-DSA para las firmas cuando las dobles firmas son operacionalmente factibles.

La constatación de Project Leap según la cual el híbrido es «mucho, mucho más pesado» que cualquiera de los enfoques puros es el contrapeso honesto a esa recomendación. Los consejos deberían anticipar una subida de capacidad de cálculo y almacenamiento, handshakes más largos y complejidad adicional de cadenas de certificados durante la transición. La compensación: el híbrido elimina la mayor fuente única de riesgo de migración: la bascula abrupta de un fundamento criptográfico a otro en entorno de producción.

## Cuánto cuesta y por qué no hacer nada cuesta más

El análisis de Mastercard, [reportado a principios de 2026 ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs"), cifró el coste mundial de la migración PQC del sector financiero en 28-42 mil millones de dólares. Dentro de ese agregado, las [investigaciones de RedCompass Labs y CMORG ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") que siguen los gastos institucionales reales sugieren que los bancos de primer nivel comprometen entre 20 y 30 millones de dólares al año en programas de preparación, con calendarios de implementación que cubren varios ciclos de liderazgo. Son cantidades sustanciales. Sin embargo, no es la comparación pertinente.

La comparación pertinente es el coste de un solo evento de descifrado retroactivo. Para una institución cuyo tráfico de transferencias cosechado, correspondencia M&A o datos de exposición a contrapartes se vuelven legibles para un adversario en 2032, el coste operativo y reputacional no está acotado por la línea capex de migración. Está acotado por el valor de la década de información estratégica subyacente, que, para cualquier institución sistémica, es materialmente superior a cualquier presupuesto de migración plausible. El encuadre del G7 según el cual la transición criptográfica es una cuestión de gestión de riesgos sistémicos en lugar de una actualización tecnológica es correcto, y los consejos deberían abordarlo sobre esa base.

Hay una segunda línea de coste que merece separarse. La migración a la PQC es una función de forzamiento para la agilidad criptográfica: la capacidad arquitectónica para reemplazar los algoritmos criptográficos sin reconstruir los sistemas que dependen de ellos. La mayoría de instituciones no tienen hoy agilidad criptográfica; sus dependencias RSA y ECC están profundamente integradas en las PKI, las cadenas de firma de código, las integraciones de proveedores y los protocolos caseros acumulados a lo largo de las décadas. La inversión en agilidad, hecha bajo la presión de la transición PQC, es duradera. Se movilizará de nuevo cuando llegue la próxima transición criptográfica, ya se trate de un sucesor de la PQC basada en retículos, de una sobrecapa de QKD o de otra cosa que aún no esté en la hoja de ruta de los estándares. Tratado correctamente, el capex de migración PQC es una inversión puntual que reporta opcionalidad recurrente.

## Conclusión

El argumento a favor de tratar la migración postcuántica como una prioridad de consejo en 2026 no descansa en la inminencia de un CRQC. Las estimaciones al respecto siguen siendo realmente inciertas: la opinión científica creíble sitúa la probabilidad de un CRQC para 2028 muy por debajo del uno por ciento, ascendiendo a aproximadamente el cincuenta por ciento en el horizonte 2037-2040. El argumento descansa en tres observaciones más que no son inciertas.

Primero, el HNDL se produce hoy, y los datos con una exigencia de confidencialidad de al menos una década están expuestos independientemente de cuándo llegue el CRQC. Segundo, la migración del parque criptográfico de una gran institución financiera lleva de cinco a siete años incluso con financiación adecuada y atención de la dirección, lo que significa que el programa iniciado en 2026 termina hacia 2031, bien dentro del extremo conservador de la distribución de probabilidad del CRQC. Tercero, las expectativas normativas se han endurecido materialmente en los últimos doce meses, y las instituciones cuyas actas de consejo 2026 consignen un programa PQC claro estarán en una posición sensiblemente más fuerte que aquellas cuyas actas solo consignen una vigilancia atenta.

Las instituciones que arrancan ahora tienen la ventaja de la elección. Pueden secuenciar el trabajo a lo largo de varios ciclos de liderazgo, integrarlo con iniciativas de resiliencia más amplias y absorber los costes operativos del despliegue híbrido en una planificación capitalista normal. Las instituciones que esperan afrontarán el mismo trabajo bajo plazos más ajustados, con menos margen de secuenciación, y sobre un trasfondo de restricciones de suministro de hardware PQC, experiencia y capacidad de proveedores. El coste de actuar pronto es conocido; el coste de actuar tarde es asimétrico precisamente de la manera que la gestión de riesgos se diseña para evitar.

Para poner este artículo en perspectiva en este sitio, el [artículo de abril de 2026 sobre la compresión de los umbrales cuánticos](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") examinaba la trayectoria material subyacente, el [análisis de noviembre de 2023 sobre CRYSTALS-Kyber](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") cubría los fundamentos matemáticos ahora estandarizados bajo ML-KEM, el [artículo de diciembre de 2023 sobre la distribución cuántica de claves](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") trataba de la sobrecapa [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) complementaria, y la [implementación de referencia open source KyberLib](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") proporciona una implementación Rust operativa de las primitivas subyacentes para las instituciones que deseen inspeccionar directamente la superficie criptográfica. Implicarse en el detalle práctico y técnico —no solo en los titulares normativos— es la manera en que los consejos distinguen un programa de migración creíble de un teatro de cumplimiento.

## Preguntas frecuentes

**¿Cuándo existirá realmente un ordenador cuántico criptográficamente relevante?**

Las estimaciones creíbles varían ampliamente. A principios de 2026, las demostraciones cuánticas públicas han alcanzado entre 24 y 28 qubits lógicos, mientras que se estima que un CRQC requiere alrededor de 6.000 qubits lógicos sustentados por entre 100.000 y varios millones de qubits físicos, dependiendo del enfoque de corrección de errores. El consenso experto sitúa la probabilidad de un CRQC en menos del uno por ciento para 2028, en torno al cincuenta por ciento en el horizonte 2037-2040, con una variabilidad significativa entre previsiones. Las recientes reducciones de las estimaciones teóricas de recursos —de 20 millones de qubits hace unos años a menos de un millón en los trabajos de Gidney en 2025, y a aproximadamente 100.000 en el artículo QLDPC de febrero de 2026— han comprimido el horizonte de planificación. Para las necesidades de un consejo, la hipótesis de planificación apropiada es mediados de la década de 2030 para los sistemas de alto riesgo, finales de la década de 2030 como punto medio conservador, y antes si la exposición HNDL es la preocupación limitante.

**¿Por qué un despliegue híbrido en lugar de postcuántico puro?**

Tres razones. Primero, ML-KEM y ML-DSA, aunque seriamente validados, tienen historiales criptoanalíticos más cortos que RSA y ECC. Un esquema híbrido sigue siendo seguro si cualquiera de los componentes se sostiene; un esquema PQC puro queda expuesto si el problema sobre retículos se debilita inesperadamente. Segundo, el híbrido preserva la retrocompatibilidad con las contrapartes que aún no han migrado, crítico en una transición industrial plurianual. Tercero, toda autoridad principal fuera de la Australian Signals Directorate recomienda explícitamente el híbrido para el periodo de transición: NCSC, ANSSI, BSI, NLNCSA y el marco G7 validan todos el enfoque de doble envolvente. La compensación, como cuantificó Project Leap, es un sobrecoste materialmente más alto en cálculo y almacenamiento. Es el precio de la opcionalidad.

**¿Hace falta a la vez ML-KEM y ML-DSA, o se puede elegir?**

Ambos. ML-KEM y ML-DSA desempeñan roles criptográficos distintos. ML-KEM reemplaza las primitivas de establecimiento de clave en TLS, las VPN, la autenticación móvil y protocolos similares en los que dos partes deben convenir una clave simétrica compartida. ML-DSA reemplaza las primitivas de firma digital en los certificados PKI, la firma de código, la firma de documentos, la mensajería autenticada tipo SWIFT y las aserciones de identidad. El parque criptográfico de una institución utiliza los dos tipos de primitivas en distintos lugares; la migración debe cubrir ambos. El tamaño de firma significativamente mayor de ML-DSA (50-70× ECDSA) suele ser el más exigente de los dos a nivel operativo; el trabajo de planificación de red y almacenamiento para ML-DSA domina la mayoría de evaluaciones de capacidad de migración.

**¿Cómo medir el avance de un programa de este tamaño?**

Tres indicadores son prácticos y se alinean con los principales marcos normativos. **Cobertura de la CBOM**: qué porcentaje de las instancias criptográficas asimétricas de la institución se ha inventariado, clasificado y etiquetado para prioridad de migración. **Cobertura de migración de los activos de alto riesgo**: qué porcentaje de los activos donde la condición S + M > Q de Mosca es verdadera ha migrado a la PQC híbrida. **Cobertura de agilidad criptográfica**: qué porcentaje de los sistemas con dependencia criptográfica puede reemplazar los algoritmos sin cambio de código, solo por configuración. La hoja de ruta G7 CEG, el marco en tres fases del NCSC y la hoja de ruta coordinada UE se conectan todos a estas tres medidas, incluso cuando utilizan terminología diferente.

**¿Cuál es el coste de esperar un año más?**

No es nulo, y no es simétrico. Esperar un año renuncia a un año de protección HNDL sobre los datos de larga vida útil: los datos cuya exigencia de confidencialidad se extiende a 2040 quedan expuestos un año más de lo necesario. Comprime la ventana de migración frente a plazos normativos fijos (ASD 2030, hitos NSA CNSA 2.0, objetivo UE 2030 para los sistemas críticos), lo que se traduce en un riesgo de entrega más alto y una flexibilidad de secuenciación reducida. Expone a la institución a restricciones de suministro de proveedores y talento que ya son visibles en el mercado y que se agravarán cuando los mayores actores del sector pasen de la planificación a la ejecución. El coste no es catastrófico en un solo año, pero se compone, y el entorno normativo converge hacia una posición en la que los consejos tendrán que explicar el retraso en lugar del gasto.

## Referencias

- Sebastien Rousseau, (2026). [Quantum Thresholds Are Moving Again](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Sebastien Rousseau, (2023). [Quantum Key Distribution Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [KyberLib: A Rust-Powered Shield Against Quantum Threats](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats").
- G7 Cyber Expert Group, (2026). [Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement, January 2026"). GOV.UK.
- Bank for International Settlements, (2025). [Project Leap Phase 2: Quantum-Proofing Payment Systems ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"). BIS.
- Bank for International Settlements, (2025). [Project Leap: Quantum-Proofing the Financial System ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"). BIS.
- NIST, (2024). [FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard"). NIST.
- UK NCSC, (2025). [Timelines for Migration to Post-Quantum Cryptography ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines "Timelines for migration to post-quantum cryptography — NCSC"). UK National Cyber Security Centre.
- CMORG, (2025). [Guidance for Post-Quantum Cryptography ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"). Cross-Market Operational Resilience Group.
- Post-Quantum Cryptography Coalition, (2025). [International PQC Requirements ⧉](https://pqcc.org/international-pqc-requirements/ "International PQC Requirements — Post-Quantum Cryptography Coalition"). PQCC.
- PQShield, (2025). [PQC Roadmaps and Transition Guidance ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"). PQShield.
- Banking.Vision, (2026). [The Year of Quantum Computing: 2026 ⧉](https://banking.vision/en/the-year-of-quantum-computing/ "The Year of Quantum Computing 2026"). Banking.Vision / msg for banking.
- The Quantum Insider, (2026). [How to Prep For Post-Quantum Cryptography: G7 Releases Roadmap ⧉](https://thequantuminsider.com/2026/01/15/how-to-prep-for-post-quantum-crytography-g7-releases-roadmap-to-help-financial-sector-navigate-transition-to-quantum-era/ "How to Prep For Post-Quantum Cryptography — The Quantum Insider"). The Quantum Insider.
- Quantum Computing Report, (2026). [Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates ⧉](https://quantumcomputingreport.com/shor-qldpc-codes-and-the-compression-of-rsa-2048-resource-estimates-part-i/ "Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates"). Quantum Computing Report.
- Cryptomathic, (2025). [A Banker's Guide to Quantum Safe Cryptography — Roadmap to PQC Migration for Financial Institutions ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography"). Cryptomathic.
- Forrester, (2025). [2026 Asia Pacific Predictions: Quantum Security ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"). Forrester Research.
- The Asian Banker, (2025). [Building Resilience for a Quantum-Ready Financial System ⧉](https://www.theasianbanker.com/updates-and-articles/building-resilience-for-a-quantum-ready-financial-system "Building resilience for a quantum-ready financial system"). The Asian Banker.
