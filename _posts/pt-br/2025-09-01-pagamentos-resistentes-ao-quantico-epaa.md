---
title: "Pagos resistentes a lo quântico: por que a industria deve actuar agora"
subtitle: "La criptografia pós-quântica é ya uma decisão de infraestrutura actual, e no futura. El libro blanco EPAA expone o riesgo estructural e a urgente necessidade de migración."
description: "La computação quântica amenaza a criptografia de os sistemas de pago. El libro blanco EPAA expone o riesgo estructural e aboga por uma migración urgente rumo a a criptografia pós-quântica."
date: "September 01, 2025"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Placa de circuito de computação quântica bañada em luz azul"
keywords: "pagos resistentes a lo quântico, criptografia pós-quântica, SEPA, SWIFT gpi, ISO 20022, segurança de os serviços financeiros, EPAA, harvest-now decrypt-later, agilidade criptográfica, Sebastien Rousseau"
---

## La ameaça quântica sobre os sistemas de pago

La infraestrutura de pagos moderna reposa em a criptografia de clave pública —RSA, ECC e Diffie-Hellman— para autenticar as transações, proteger os dados de os titulares de tarjetas e asegurar a mensajería entre instituições financeiras. Estos algoritmos sustentan SWIFT, SEPA, os sistemas de liquidação bruta em tempo real e práticamente cada esquema de tarjetas em atividade hoje em dia.

Los computadores quânticos que ejecuten o algoritmo de Shor serão capaces de romper estas primitivas criptográficas. Si bien as máquinas quânticas tolerantes a fallos ainda no existen a a escala requerida, a trayectoria do desenvolvimento de hardware —demostrada por IBM, Google e otros— convierte esto em uma questão de calendario de ingeniería mais que de teoría. El National Institute of Standards and Technology (NIST) ya tem finalizado seu primer juego de estándares de criptografia pós-quântica (FIPS 203, 204 e 205) em resposta.

## El riesgo «cosechar agora, descifrar mais tarde»

La amenaza no se confina a uma fecha futura em a que os computadores quânticos alcancen capacidade suficiente. Actores estatales e adversarios sofisticados interceptan e almacenan ya hoje dados cifrados, com a intención de descifrarlos uma vez que os recursos quânticos estén disponibles. Esta estrategia «harvest-now decrypt-later» (HNDL) significa que cualquier dado de pago com sensibilidad larga —registros normativos, arquivos de cumplimiento, obligaciones contractuales— está ya em riesgo.

Los reguladores financeiros têm comenzado a reaccionar. La Monetary Authority of Singapore (MAS) tem publicado orientações sobre a preparación quântica. La Australian Prudential Regulation Authority (APRA) tem señalado o riesgo criptográfico em seu marco de resiliencia tecnológica. El Digital Operational Resilience Act (DORA) de a Unión Europea impone uma gestión de os riesgos ICT que deve tener em cuenta as amenazas emergentes, incluída a computação quântica.

## Impacto em o conjunto de os rails de pago

Las implicaciones cubren tudo o conjunto de a infraestrutura de pagos:

**Mensajería SWIFT:** Los formatos de mensajes MT e MX se apoyan em TLS e as firmas digitais para a integridad e a autenticação. Una infraestrutura de claves comprometida socavaría o modelo de confiança que vincula a mais de 11.000 instituciones a escala global.

**SEPA e pagos instantáneos:** El esquema SEPA Instant Credit Transfer do European Payments Council trata transações irrevocables em menos de dez segundos. Una vulneración criptográfica a essa velocidade no deja ninguna ventana para uma intervención humana ou uma verificação manual.

**Sistemas de pago em tempo real:** Faster Payments (UK), FedNow (US) e NPP (Australia) comparten todos a mesma dependencia de as primitivas criptográficas clásicas para a autenticação de mensajes e a verificação de os participantes.

**Cumplimiento e dados de larga duración de vida:** Los registros de pago conservados com fines normativos —frequentemente impuestos durante cinco a dez anos ou mais— sobrevivirán a as garantías de segurança de a criptografia que os protegía em o momento de seu criação. Los programas de migración [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) devem tener em cuenta a duración de preservação criptográfica de os dados que producen.

**Blockchain e libros mayores distribuidos:** Las plataformas de activos digitais e os instrumentos de pago tokenizados que dependen de a criptografia de curva elíptica afrontan uma amenaza directa e bien comprendida de os algoritmos quânticos.

## Lo que as organizações devem fazer agora

La transición rumo a uma criptografia resistente a lo quântico no é uma actualización única mas sim um programa plurianual que exige uma preparación estructurada:

**Inventario criptográfico:** Las organizações devem catalogar cada sistema, protocolo e almacén de dados que dependa de a criptografia de clave pública clásica. Esto inclui os certificados TLS, a autenticação de API, as configuraciones HSM, os sistemas de gestión de claves e o criptografia de os dados em reposo.

**Adopción de algoritmos pós-quânticos:** El NIST tem estandarizado ML-KEM (FIPS 203) para a encapsulación de claves e ML-DSA (FIPS 204) para as firmas digitais. Las organizações deveriam comenzar a probar estes algoritmos em entornos fora de producción e desenvolver folhas de ruta de migración para os sistemas críticos.

**Agilidad criptográfica:** Los sistemas devem diseñarse —ou refactorizarse— de modo que os algoritmos criptográficos puedan reemplazarse sem necessidade de uma refactorización aplicativa completa. Este principio se aplica tanto a as pasarelas de pago, como a a mensajería intermediaria e a as API de cliente.

**Enfoques híbridos:** Durante o periodo de transición, os esquemas criptográficos híbridos que combinan algoritmos clásicos e pós-quânticos oferecem uma defensa em profundidad. Este enfoque preserva a retrocompatibilidad ao tempo que introduz a resistencia quântica.

## Grupo de trabalho EPAA e colaboração industrial

La Emerging Payments Association Asia (EPAA) tem establecido seu Grupo de trabalho Quantum Safe Cryptography para abordar estes desafíos mediante uma ação industrial coordinada. El grupo de trabalho reúne a participantes de tudo o ecosistema de pagos, incluídos IBM, HSBC, KPMG, JPMorgan Chase e PayPal, entre otros.

En talleres celebrados em Sídney, Hong Kong e Singapur, o grupo de trabalho desenvolveu um marco compartido para avaliar o riesgo quântico em os sistemas de pago e identificar vías de migración práticas. El libro blanco resultante —[Quantum-Safe Payments: Why the Payments Industry Must Act Now][epaa]— representa uma posição consensuada sobre a urgencia e a amplitud do desafío.

El análisis do grupo de trabalho concluye que a preparación resistente a lo quântico é uma decisão de infraestrutura actual, e no futura. Las organizações que demoren se exponen a no poder ya satisfacer as expectativas normativas, proteger os dados de larga duración ou manter a interoperabilidade com socios ya migrados.

## Sobre ou autor

Sebastien Rousseau é Senior Digital Product Manager em HSBC Bank plc, onde dirige os productos de API de pagos corporativos em a Commercial & Investment Bank de HSBC. Ha contribuido ao Grupo de trabalho EPAA Quantum Safe Cryptography e estuda a aplicação de a criptografia pós-quântica a os serviços financeiros. [Más informação sobre Sebastien ❯][00]

## Artículos relacionados

- [[Distribución quântica de claves](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html): revolucionar a segurança bancária][rel1]
- [[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html): o algoritmo de protección em a era quântica][rel2]

[00]: /about/index.html "Sobre Sebastien Rousseau"
[epaa]: https://emergingpaymentsasia.org/wp-content/uploads/2025/09/Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf "Libro blanco EPAA Quantum-Safe Payments"
[rel1]: /2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking"
[rel2]: /2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age"
