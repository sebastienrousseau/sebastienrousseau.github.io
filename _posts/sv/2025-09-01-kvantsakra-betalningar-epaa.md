---
title: "Pagos resistentes a lo cuántico: por qué la industria debe actuar ahora"
subtitle: "La criptografía postcuántica es ya una decisión de infraestructura actual, y no futura. El libro blanco EPAA expone el riesgo estructural y la urgente necesidad de migración."
description: "La computación cuántica amenaza la criptografía de los sistemas de pago. El libro blanco EPAA expone el riesgo estructural y aboga por una migración urgente hacia la criptografía postcuántica."
date: "September 01, 2025"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Placa de circuito de computación cuántica bañada en luz azul"
keywords: "pagos resistentes a lo cuántico, criptografía postcuántica, SEPA, SWIFT gpi, ISO 20022, seguridad de los servicios financieros, EPAA, harvest-now decrypt-later, agilidad criptográfica, Sebastien Rousseau"
---

## La amenaza cuántica sobre los sistemas de pago

La infraestructura de pagos moderna reposa en la criptografía de clave pública —RSA, ECC y Diffie-Hellman— para autenticar las transacciones, proteger los datos de los titulares de tarjetas y asegurar la mensajería entre instituciones financieras. Estos algoritmos sustentan SWIFT, SEPA, los sistemas de liquidación bruta en tiempo real y prácticamente cada esquema de tarjetas en actividad hoy en día.

Los ordenadores cuánticos que ejecuten el algoritmo de Shor serán capaces de romper estas primitivas criptográficas. Si bien las máquinas cuánticas tolerantes a fallos aún no existen a la escala requerida, la trayectoria del desarrollo de hardware —demostrada por IBM, Google y otros— convierte esto en una cuestión de calendario de ingeniería más que de teoría. El National Institute of Standards and Technology (NIST) ya ha finalizado su primer juego de estándares de criptografía postcuántica (FIPS 203, 204 y 205) en respuesta.

## El riesgo «cosechar ahora, descifrar más tarde»

La amenaza no se confina a una fecha futura en la que los ordenadores cuánticos alcancen capacidad suficiente. Actores estatales y adversarios sofisticados interceptan y almacenan ya hoy datos cifrados, con la intención de descifrarlos una vez que los recursos cuánticos estén disponibles. Esta estrategia «harvest-now decrypt-later» (HNDL) significa que cualquier dato de pago con sensibilidad larga —registros normativos, archivos de cumplimiento, obligaciones contractuales— está ya en riesgo.

Los reguladores financieros han comenzado a reaccionar. La Monetary Authority of Singapore (MAS) ha publicado orientaciones sobre la preparación cuántica. La Australian Prudential Regulation Authority (APRA) ha señalado el riesgo criptográfico en su marco de resiliencia tecnológica. El Digital Operational Resilience Act (DORA) de la Unión Europea impone una gestión de los riesgos ICT que debe tener en cuenta las amenazas emergentes, incluida la computación cuántica.

## Impacto en el conjunto de los rails de pago

Las implicaciones cubren todo el conjunto de la infraestructura de pagos:

**Mensajería SWIFT:** Los formatos de mensajes MT y MX se apoyan en TLS y las firmas digitales para la integridad y la autenticación. Una infraestructura de claves comprometida socavaría el modelo de confianza que vincula a más de 11.000 instituciones a escala global.

**SEPA y pagos instantáneos:** El esquema SEPA Instant Credit Transfer del European Payments Council trata transacciones irrevocables en menos de diez segundos. Una vulneración criptográfica a esa velocidad no deja ninguna ventana para una intervención humana o una verificación manual.

**Sistemas de pago en tiempo real:** Faster Payments (UK), FedNow (US) y NPP (Australia) comparten todos la misma dependencia de las primitivas criptográficas clásicas para la autenticación de mensajes y la verificación de los participantes.

**Cumplimiento y datos de larga duración de vida:** Los registros de pago conservados con fines normativos —a menudo impuestos durante cinco a diez años o más— sobrevivirán a las garantías de seguridad de la criptografía que los protegía en el momento de su creación. Los programas de migración [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) deben tener en cuenta la duración de conservación criptográfica de los datos que producen.

**Blockchain y libros mayores distribuidos:** Las plataformas de activos digitales y los instrumentos de pago tokenizados que dependen de la criptografía de curva elíptica afrontan una amenaza directa y bien comprendida de los algoritmos cuánticos.

## Lo que las organizaciones deben hacer ahora

La transición hacia una criptografía resistente a lo cuántico no es una actualización única sino un programa plurianual que exige una preparación estructurada:

**Inventario criptográfico:** Las organizaciones deben catalogar cada sistema, protocolo y almacén de datos que dependa de la criptografía de clave pública clásica. Esto incluye los certificados TLS, la autenticación de API, las configuraciones HSM, los sistemas de gestión de claves y el cifrado de los datos en reposo.

**Adopción de algoritmos postcuánticos:** El NIST ha estandarizado ML-KEM (FIPS 203) para la encapsulación de claves y ML-DSA (FIPS 204) para las firmas digitales. Las organizaciones deberían comenzar a probar estos algoritmos en entornos fuera de producción y desarrollar hojas de ruta de migración para los sistemas críticos.

**Agilidad criptográfica:** Los sistemas deben diseñarse —o refactorizarse— de modo que los algoritmos criptográficos puedan reemplazarse sin necesidad de una refactorización aplicativa completa. Este principio se aplica tanto a las pasarelas de pago, como a la mensajería intermediaria y a las API de cliente.

**Enfoques híbridos:** Durante el periodo de transición, los esquemas criptográficos híbridos que combinan algoritmos clásicos y postcuánticos ofrecen una defensa en profundidad. Este enfoque preserva la retrocompatibilidad al tiempo que introduce la resistencia cuántica.

## Grupo de trabajo EPAA y colaboración industrial

La Emerging Payments Association Asia (EPAA) ha establecido su Grupo de trabajo Quantum Safe Cryptography para abordar estos desafíos mediante una acción industrial coordinada. El grupo de trabajo reúne a participantes de todo el ecosistema de pagos, incluidos IBM, HSBC, KPMG, JPMorgan Chase y PayPal, entre otros.

En talleres celebrados en Sídney, Hong Kong y Singapur, el grupo de trabajo ha desarrollado un marco compartido para evaluar el riesgo cuántico en los sistemas de pago e identificar vías de migración prácticas. El libro blanco resultante —[Quantum-Safe Payments: Why the Payments Industry Must Act Now][epaa]— representa una posición consensuada sobre la urgencia y la amplitud del desafío.

El análisis del grupo de trabajo concluye que la preparación resistente a lo cuántico es una decisión de infraestructura actual, y no futura. Las organizaciones que demoren se exponen a no poder ya satisfacer las expectativas normativas, proteger los datos de larga duración o mantener la interoperabilidad con socios ya migrados.

## Sobre el autor

Sebastien Rousseau es Senior Digital Product Manager en HSBC Bank plc, donde dirige los productos de API de pagos corporativos en la Commercial & Investment Bank de HSBC. Ha contribuido al Grupo de trabajo EPAA Quantum Safe Cryptography y estudia la aplicación de la criptografía postcuántica a los servicios financieros. [Más información sobre Sebastien ❯][00]

## Artículos relacionados

- [[Distribución cuántica de claves](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html): revolucionar la seguridad bancaria][rel1]
- [[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html): el algoritmo de protección en la era cuántica][rel2]

[00]: /about/index.html "Sobre Sebastien Rousseau"
[epaa]: https://emergingpaymentsasia.org/wp-content/uploads/2025/09/Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf "Libro blanco EPAA Quantum-Safe Payments"
[rel1]: /2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking"
[rel2]: /2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age"
