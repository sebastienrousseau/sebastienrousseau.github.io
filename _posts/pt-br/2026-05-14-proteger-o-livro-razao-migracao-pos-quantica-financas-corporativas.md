---
title: "Asegurar o libro contable: guía para consejos de administración sobre a migración pós-quântica em banca corporativa"
subtitle: "El riesgo quântico tem passado de a curiosidad acadêmica a um mandato normativo activo. La folha de ruta do G7, BIS Project Leap e os calendarios UE/UK/Australia plantean ya a questão no do cuándo, mas sim do cómo."
description: "El riesgo quântico tem passado de a curiosidad acadêmica ao mandato normativo. Con a folha de ruta do G7 de enero de 2026, calendarios UE, UK e australiano agora aclarados, e BIS Project Leap que demonstrou a viabilidad em um sistema de pago real, a questão para os consejos de administración ya no é a migración, mas sim os prazos."
date: "May 14, 2026"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Puerta de caja fuerte abierta bañada em luz dorada — metáfora visual de a protección criptográfica de os arquivos financeiros"
keywords: "criptografia pós-quântica, ML-KEM, ML-DSA, FIPS 203, FIPS 204, BIS Project Leap, G7 CEG, NCSC, ANSSI, BSI, ASD, CNSA 2.0, agilidade criptográfica, banca corporativa, pagos wholesale"
---

El riesgo quântico tem passado de a curiosidad acadêmica ao mandato normativo activo. Con a folha de ruta do G7 publicada em enero de 2026, os calendarios de a UE, o Reino Unido e Australia agora aclarados, e BIS Project Leap que demonstrou a viabilidad em um sistema de pago real, a questão para os consejos de administración ya no é si há que migrar, mas sim si a migración pode completarse antes de que a vida útil criptográfica de os dados de hoje expire.

---

> **TL;DR.** La preparación pós-quântica tem passado em 2026 de folha de ruta a obligación. Los consejos de administración devem tratar a migración como uma decisão de gestión de riesgos sistémicos, anclada em ML-KEM e ML-DSA, desplegada de forma híbrida, e secuenciada com suficiente antelación para preceder a um CRQC plausible e a as exigencias normativas mais estrictas aplicables.
>
> **Principais Conclusões**
>
> - **2026 é o ano em que a postura normativa tem-se endurecido.** La folha de ruta de enero do Cyber Expert Group do G7, o calendario coordinado do Grupo de cooperación NIS de a UE e o plan em três fases do NCSC británico fizeram passar a conversación de a sensibilización a a execução. La Australian Signals Directorate va ainda mais longe ao fijar uma fecha límite firme a 2030 para a criptografia asimétrica clásica.
> - **La exposición é asimétrica.** RSA, ECC e Diffie–Hellman constituyen o problema inmediato: os algoritmos asimétricos que sustentan os handshakes SWIFT, TLS, as PKI, a firma de código e a autenticação de as redes de compensación. El criptografia simétrico (AES-256) segue siendo estable si se mantém a longitud de as claves. La atención do consejo deve centrarse em a superficie asimétrica.
> - **«Cosechar agora, descifrar mais tarde» no é um escenario futuro.** Adversarios interceptan e almacenan ya hoje registros financeiros cifrados, registros de liquidação, expedientes de M&A e dados de transferências transfronteiriças, com a intención explícita de descifrarlos uma vez que exista um computador quântico criptográficamente relevante (CRQC). Para dados sujetos a uma exigencia de confidencialidad de 10 a 20 anos, este riesgo ya tem-se materializado.
> - **La industria dispone agora de um ponto de referencia operativo.** [BIS Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), publicado em diciembre de 2025, sustituyó com éxito as firmas digitais tradicionais por criptografia pós-quântica em transferencias de liquidez em producción através de TARGET2, e fez aflorar os costes de ingeniería específicos (latencia de verificação, tamaño de paquetes) a os que se enfrentará cualquier programa de migración.
> - **La suite NIST é o ancla mundial.** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") e FIPS 204 (ML-DSA) são referenciados por todas as jurisdicciones principales, incluso quando as posições nacionales divergen sobre os conjuntos de parámetros e as exigencias híbridas. Los consejos deveriam considerar ML-KEM-768 / ML-DSA-65 como suelo e ML-KEM-1024 / ML-DSA-87 como referencia conservadora para os dados de larga vida útil.
> - **El híbrido é a única vía creíble.** Ninguna autoridade principal recomienda a bascula directa. Hacer funcionar clásico e resistente a lo quântico em paralelo é o esquema de despliegue validado por o NCSC, o ANSSI, o BSI, e demostrado em Project Leap. Es mais pesado que cualquiera de as alternativas, mas é a única que aborda a a vez a compatibilidade de hoje e a amenaza de amanhã.

---

## El ano em que a postura normativa tem-se endurecido

Durante a maior parte de a última década, a criptografia pós-quântica vivía em uma esquina cómoda de a folha de ruta a longo prazo. Los computadores quânticos eram impresionantes mas lejanos; a matemática criptográfica subyacente a RSA e a as curvas elípticas se trataba como sustrato estable; e a conversación sobre a migración se mantenía em gran medida confinada a grupos de trabalho especializados. Esa posição ya no é sostenible.

En enero de 2026, o [Cyber Expert Group do G7 publicó seu declaración mais consecuente até a fecha ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement on Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector"), copresidida por o Tesoro estadounidense e o Banco de Inglaterra. El documento no é uma regulação, mas pesa mais que uma orientação clásica: representa a posição compartida de os ministerios de Finanzas, bancos centrales e autoridades de supervisión de as jurisdicciones do G7, conforme a cual a transición criptográfica é agora uma questão de gestión de riesgos sistémicos. La folha de ruta alinea seu horizonte de planificación com mediados de a década de 2030, animando a os sistemas financeiros críticos a migrar antes, uma formulación que, em o idioma prudente de os banqueros centrales, señala uma expectativa mais que uma sugerencia.

Dos meses antes, o BIS Innovation Hub e o Eurosistema publicaron os resultados de [Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), uma experimentación técnica que sustituyó as firmas digitais tradicionais por criptografia pós-quântica em transferencias de liquidez em producción entre a Banca d'Italia, a Banque de France, a Deutsche Bundesbank, Nexi-Colt e Swift. La conclusão principal foi um éxito: transferencias firmadas resistentes a lo quântico atravesaron de extremo a extremo um sistema de pago operativo. El detalle sob o titular é mais instructivo, e se examina mais adelante em este artigo.

La combinación de estes dois eventos —um marco político coordinado do G7 e uma prueba operativa em um sistema de pago real— tem producido lo que a comunidade técnica esperaba desde faz uma década: uma resposta definitiva a a pergunta «é esto real?». La resposta, em mayo de 2026, é sim. La questão que queda é a do ritmo.

## Tres vectores de amenaza que devem preocupar ao consejo

Antes de discutir a mecánica de migración, conviene ser preciso sobre lo que está concretamente em juego. El riesgo quântico em banca corporativa no é uniforme em tudo o parque criptográfico, e a atención do consejo se dirige melhor a os três vectores onde a exposición é mais aguda.

### 1. Cosechar agora, descifrar mais tarde (HNDL)

La preocupação mais inmediata no é futura. Es presente. Adversarios de nivel estatal e organizações criminales sofisticadas interceptan e almacenan sistemáticamente o tráfico financeiro criptografia —transferencias, flujos de mensajes SWIFT, comunicações M&A, registros de liquidação transfronteiriça, contratos de swap e arquivos KYC— sem capacidade actual de leerlos. Su objetivo é simple: almacenar agora, descifrar mais tarde, uma vez que exista um CRQC. Como [señaló explícitamente o Banco de Pagos Internacionales ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), essa coleta ya está em curso.

Para os consejos, a implicación é incómoda mas precisa: cualquier dado sensible transmitido hoje sob criptografia asimétrico clásico, cuya exigencia de confidencialidad se extienda mais allá de a llegada de um CRQC, ya deve considerarse expuesto. No há notificação de brecha quando ocurre um HNDL. No há alerta SIEM. El criptografia se sostiene —de momento— mas os dados ya têm salido do perímetro.

### 2. Riesgo de sensibilidad a longo prazo

Los dados de banca corporativa têm vidas útiles institucionales inusualmente largas. La documentación de M&A estratégica pode seguir siendo sensible ao mercado durante uma década. Las comunicações sobre secretos industriales e as valoraciones de propriedade intelectual podem seguir siendo confidenciales durante quince a veinte anos. Los registros de liquidação transfronteiriça, as exposiciones de contrapartes centrales e as avaliações de crédito de contrapartes conservan uma sensibilidad comercial muito mais allá de seu vida transaccional inmediata.

La [ecuación de Mosca ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), formulada originalmente por Michele Mosca e agora integrada em tudo marco de migración serio, formaliza o problema. Si **S** é a vida útil de os dados, **M** é o tempo necessário para migrar os sistemas que os protegen e **Q** é o tempo antes de que um CRQC esté disponible, então:

```
Si S + M > Q, os dados ya estão expuestos.
```

Para dados cuyo horizonte de confidencialidad é de veinte anos e um programa de migración que requer razonablemente cinco a sete anos, o valor Q implícito sobre ou que apuesta o consejo é de ao menos 25 anos. Um cuerpo creciente de avaliações de expertos —as [previsões APAC 2026 de Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), as encuestas anuales do Global Risk Institute e um artigo de arquitectura de febrero de 2026 que propone um CRQC com uns 100.000 qubits físicos utilizando códigos QLDPC— sugiere que essa apuesta é imprudente.

### 3. La vulnerabilidad de os handshakes centrales

El tercer vector é o mais significativo arquitectónicamente. Los cifrados simétricos (AES-256) seguem siendo comparativamente estables; o algoritmo de Grover divide a a mitad o nivel de segurança efectivo, mas duplicar a longitud de clave restaura o margen. La exposición catastrófica concierne a os algoritmos asimétricos, e são precisamente os algoritmos que sustentan tudo handshake autenticado em banca corporativa: RSA em a infraestrutura de claves públicas SWIFT, ECDSA em a autenticação cliente/servidor TLS, ECDH em o establecimiento de claves de sesión, e as variantes ECC por todas partes em a autenticação móvel do cliente, as firmas de API e as cadenas de firma de código.

Um CRQC funcional que ejecute o algoritmo de Shor no debilita progresivamente esses sistemas. Los rompe. Una vez que um CRQC sea operativo, cualquier handshake protegido por RSA, cualquier firma ECDSA e cualquier intercambio de clave por curva elíptica se vuelven recuperables, no depois de meses de esfuerzo, mas sim em questão de horas. La transición de «seguro» a «comprometido» é binaria, e se propaga simultáneamente através de cada sistema que utilice o algoritmo afectado. Ese é o fundamento sobre ou que descansa a urgencia normativa.

## Endurecimiento normativo: panorama por jurisdicción

El panorama normativo mundial em mayo de 2026 ya no é um mosaico de sugerencias. Es um conjunto coordinado de calendarios que varían em rigor mas convergen rumo a o mesmo destino. Um banco multinacional que opere em as principales plazas financeiras está sometido agora a a jurisdicción aplicable mais estricta, no a a mais permisiva.

### Estados Unidos

Estados Unidos tem a posição mais prescriptiva para cualquier institución que toque sistemas federales. La [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") de a NSA impone ML-KEM-1024 e ML-DSA-87 para os sistemas de segurança nacional, debiendo os novos sistemas desplegar a PQC a partir de enero de 2027 e debiendo completarse a migración de a infraestrutura para 2035. El Memorándum OMB M-23-02 vincula a as agencias federales a a mesma trayectoria. Para os bancos comerciales, a exposición inmediata passa por as cadenas de compras federales, os contratos adyacentes a os NSS, e a presión indirecta que as orientações de a NSA ejercen sobre ou mercado mais amplio.

### Unión Europea

La UE opera em três capas. La [folha de ruta coordinada de implementación de a Comisión Europea ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), elaborada por o Grupo de cooperación NIS em junio de 2025, fija hitos por fases em 2026 (estrategias nacionales), 2030 (sistemas de alto riesgo migrados) e 2035 (transición completa). El Cyber Resilience Act impondrá actualizaciones de segurança ao estado do arte para os productos digitais a partir de finales de 2027. NIS2 refuerza a gestión de riesgos ICT, embora ninguna de as dois directivas contiene uma exigencia PQC explícita. Los reguladores nacionales, por seu parte, têm adelantado a a Comisión. El BSI alemán impone o intercambio de claves híbrido e aprueba um panel conservador de ML-KEM, FrodoKEM e Classic McEliece. La ANSSI francesa exige o híbrido tanto para a encapsulación de claves como para as firmas. La NLNCSA neerlandesa e as autoridades noruegas tem-sen alineado com ML-KEM-1024 como referencia conservadora para os dados de larga vida útil.

### Reino Unido

El NCSC británico publicó seus orientações definitivas em marzo de 2025 e as reafirmó mediante o Annual Review 2025. El calendario em três fases é explícito:

- **Hasta 2028**: identificar os serviços criptográficos que requerem actualización, construir o plan de migración e producir um inventario criptográfico completo.
- **2028 a 2031**: ejecutar as actualizaciones prioritarias, em particular sobre os sistemas críticos e os protocolos de Internet expuestos.
- **2031 a 2035**: completar a migración em o conjunto de sistemas, serviços e productos.

Para as instituições financeiras británicas, as [orientações PQC do CMORG (Cross-Market Operational Resilience Group) ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") se inscriben junto ao marco NCSC, tratan a os bancos como infraestrutura nacional crítica e colocam o énfasis em a disponibilidade de proveedores e a alineación de a cadena de suministro.

### Asia-Pacífico

La postura APAC é mais fragmentada mas evolui rápido. La ASD australiana tem a posição mais dura a nivel mundial: a criptografia de clave pública clásica ya no deve utilizarse mais allá de finales de 2030, sem recomendación híbrida, e ML-KEM-1024 requerido (ML-KEM-768 aceptable solo hasta 2030). Las organizações deveriam disponer de um plan de transición afinado para finales de 2026. La Monetary Authority de Singapur tem publicado orientações formales de preparación quântica. Japón e Corea do Sur invierten sustancialmente, embora os dois países disponen de filiales algorítmicas nacionales (Corea tem seleccionado NTRU+ e SMAUG-T como KEM, ALMer e HAETAE como firmas). La National Quantum Mission india, dotada de uma asignación gubernamental de 6.003,65 crores de rupias, identifica explícitamente os serviços bancários e financeiros como prioridad estratégica. Las [previsões APAC 2026 de Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") evalúan em mais do 90 % o número de empresas regionales que devem invertir em tecnologias pós-quânticas este ano.

### La posição neta

Para um consejo de administración, a síntesis prática de essas posições jurisdiccionales é directa. Um banco multinacional no pode gestionar o calendario de um solo regulador; deve gestionar o mais estricto aplicable. Para a maioria de as grandes instituciones, esto significa um horizonte de planificación de finales de 2030 para os sistemas de alto riesgo e finales de 2035 para a larga cola; as entidades expuestas a a ASD apuntando a a PQC pura para 2030 e as expuestas a a CNSA apuntando a a mesma ventana com ML-KEM-1024 e ML-DSA-87 específicamente.

## BIS Project Leap: lo que a industria tem probado realmente

Project Leap merece a atención do consejo no porque sea um hito de marketing, mas sim porque trata-se de a demostración de extremo a extremo mais creíble até a fecha de a criptografia pós-quântica em um sistema de pago financeiro em producción. La conclusão principal é directa: funciona. El detalle subyacente é onde residen as implicaciones operativas.

La Fase 1, completada em 2023, estableció uma VPN resistente a lo quântico entre os sistemas IT de a Banque de France e a Deutsche Bundesbank, com mensajes de pago transmitidos entre París e Fráncfort sob um esquema de criptografia híbrido. La Fase 2, completada a finales de 2025 e [publicada em diciembre ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), foi considerablemente mais allá. El consorcio sustituyó as firmas digitais tradicionais basadas em RSA por firmas pós-quânticas em a execução de transferencias de liquidez através de TARGET2, o sistema de liquidação bruta em tempo real do Eurosistema. Los participantes —o BIS Innovation Hub Eurosystem Centre, a Banca d'Italia, a Banque de France, a Deutsche Bundesbank, Nexi-Colt (que proporciona a conectividad TARGET2) e Swift— representan precisamente as instituciones cuya infraestrutura tendrá que migrar eventualmente.

El informe fez aflorar três constataciones que tudo programa de migración deveria integrar:

- **La latencia de verificação é sensiblemente mais elevada.** La verificação de firma pós-quântica llevó materialmente mais tempo que a verificação basada em RSA em o mesmo hardware. Para um sistema RTGS diseñado em torno de um tratamiento de mensajes por embaixo do segundo, no é uma observación marginal; é um dado de planificación de capacidade.
- **Los tamaños de paquete exigen uma refactorización do sistema.** Las firmas PQC são um orden de magnitud mayores que os equivalentes ECDSA (véase mais abaixo). Los sistemas de pago cuyas colas internas, ferramentas de supervisión e esquemas de banco de dados tem-sen dimensionado para mensajes de tamaño heredado no podem acomodar a nova carga útil sem refactorización. Project Leap constató explícitamente que TARGET2 no podía «acomodar facilmente» o modelo híbrido sem reingeniería sustancial.
- **El híbrido é a resposta correcta, mas mais pesado.** Ejecutar clásico e pós-quântico em paralelo preservó a retrocompatibilidad e proporcionó defensa em profundidad, mas duplicó o coste do tratamiento criptográfico. Es o coste operativo de fazer PQC correctamente durante a transición; no é evitable solo mediante ingeniería astuta.

Para um director financeiro que examine um caso de investimento PQC, as constataciones de Project Leap são útiles precisamente porque são precisas. El coste de a migración pós-quântica no é uma sola linha capex. Es uma latencia de verificação que se propaga em os contratos SLA, uma expansão do tamaño de mensajes que afecta a os presupuestos de almacenamiento e ancho de banda, e um periodo transitorio de operações criptográficas duplicadas que afecta a a planificación de capacidade de cálculo. Ninguno de estes pontos é especulativo. Tem-sen medido em um sistema de banco central em producción.

## La caja de ferramentas NIST: ML-KEM e ML-DSA comparados

La pieza maestra técnica de tudo marco nacional creíble é a suite NIST de estándares pós-quânticos publicada em agosto de 2024. Dos de esses estándares estão em o centro de atención para ou setor bancário corporativa: ML-KEM (FIPS 203) para a encapsulación de claves e ML-DSA (FIPS 204) para as firmas digitais. Comparten um fundamento matemático —ambos se apoyan em a dificuldade de os problemas Module Learning With Errors (ML-LWE) e Module Short Integer Solution sobre retículos estructurados— mas desempeñan papeles muito distintos em o parque criptográfico, e seus perfiles de rendimiento e tamaño difieren materialmente.

### ML-KEM (FIPS 203) — encapsulación de claves

ML-KEM, derivado de [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html), é o reemplazo de ECDH e de RSA-KEM em os protocolos em os que dois partes devem establecer uma clave simétrica compartida sobre um canal no seguro. Es, em a prática, adonde van os handshakes TLS tras a retirada de RSA e de ECDH. NIST define três conjuntos de parámetros com fuerza de segurança creciente e rendimiento decreciente: ML-KEM-512 (NIST Categoría 1), ML-KEM-768 (Categoría 3) e ML-KEM-1024 (Categoría 5).

### ML-DSA (FIPS 204) — firmas digitais

ML-DSA, derivado de CRYSTALS-Dilithium, é o reemplazo de as firmas RSA e ECDSA. Soporta a firma de certificados, a firma de código, a firma de documentos e a autenticação. Los três conjuntos de parámetros são ML-DSA-44, ML-DSA-65 e ML-DSA-87, correspondientes onlines generales a as NIST Categorías 2, 3 e 5.

### Perfil de tamaño e rendimiento

Para um CIO que dimensione a capacidade de migración, as cifras mais importantes são os tamaños de artefactos. Son as entradas para a planificación de capacidade de red, as proyecciones de almacenamiento e as pruebas a nivel de protocolo.

| Algoritmo | Clave pública | Criptograma / Firma | Equivalente clásico mais cercano | Tamaño vs clásico |
|---|---|---|---|---|
| ML-KEM-512 | 800 bytes | 768 bytes (criptograma) | ECDH P-256 (~32 bytes clave pub) | ~25× mayor |
| ML-KEM-768 | 1.184 bytes | 1.088 bytes (criptograma) | ECDH P-384 | ~25× mayor |
| ML-KEM-1024 | 1.568 bytes | 1.568 bytes (criptograma) | ECDH P-521 | ~25× mayor |
| ML-DSA-44 | 1.312 bytes | ~2.420 bytes (firma) | ECDSA P-256 (firma 64 bytes) | ~38× mayor |
| ML-DSA-65 | 1.952 bytes | ~3.293 bytes (firma) | ECDSA P-384 | ~50× mayor |
| ML-DSA-87 | 2.592 bytes | ~4.595 bytes (firma) | ECDSA P-521 | ~70× mayor |

*Fuente: síntesis de as especificaciones [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") e FIPS 204, com dados comparativos procedentes de a literatura de benchmarking independiente.*

Tres implicaciones operativas se derivan directamente de ello. **Primero**, o tamaño de firma é a restricción limitante para a maioria de despliegues empresariales. Una firma ML-DSA-65 é umas cincuentàs vezes o tamaño de uma firma ECDSA P-256, e as cadenas de certificados TLS que llevan CA intermedias crescem proporcionalmente. El trabalho de capacidade sobre essa superficie no é opcional, é estructurador. **Segundo**, ML-KEM é competitivo em cálculo com ECDH e, em algunas implementaciones, materialmente mais rápido, em particular em hardware que dispone de soporte vectorial para a aritmética de retículos subyacente. **Tercero**, a verificação ML-DSA é constantemente rápida (frequentemente mais rápida que a verificação ECDSA), mas a firma ML-DSA implica um bucle de rejection sampling que pode requerer vários intentos em hardware restringido. Para os serviços de firma de alto rendimiento, é um benchmark a verificar mais que a presumir.

### Elegir os conjuntos de parámetros

Las posições jurisdiccionales sobre a elección de os parámetros no são idénticas, mas a convergencia é clara. ML-KEM-768 e ML-DSA-65 constituyen o suelo empresarial —validados por o NCSC británico como referencia para as organizações británicas e aceptables em a maioria de marcos europeos—. ML-KEM-1024 e ML-DSA-87 são o techo conservador —impuestos por a CNSA 2.0 de a NSA para os sistemas de segurança nacional estadounidenses e requeridos por a ASD para as entidades australianas reguladas para 2030—. Para os dados de sensibilidad extremadamente larga —registros de liquidação soberanos, propriedade intelectual com horizonte decenal, registros de custodia para instrumentos de largo vencimiento— os conjuntos de parámetros superiores são o valor por defecto defendible.

### Um fundamento matemático compartido, um riesgo compartido

Um ponto digno de a atención do consejo: ML-KEM e ML-DSA extraen ambos seu segurança de a mesma familia de problemas sobre retículos. Um avance criptoanalítico futuro contra Module-LWE afectaría a os dois estándares simultáneamente. Es precisamente por ello pelo que várias autoridades nacionales —notablemente o BSI alemán e a ANSSI francesa— recomiendan complementar a pila basada em retículos com firmas basadas em funciones de hash (SLH-DSA, FIPS 205) para os casos de uso de firma a longo prazo e firma de código. La agilidade criptográfica, em este sentido, no é solo a capacidade de reemplazar RSA por ML-KEM. Es a capacidade de reemplazar um algoritmo PQC por otro quando o panorama criptoanalítico evolucione.

## Um camino de migración lógico: Descubrimiento → Triaje → Despliegue híbrido

Para um consejo que apruebe um programa PQC plurianual, a questão operativa é cómo escalonar o trabalho sem asumir um riesgo inaceptable de disponibilidade de serviço. El esquema que tem emergido através de a folha de ruta do G7, o marco NCSC, BIS Project Leap e os documentos de orientação nacionales principales converge em três fases.

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│ 1. DESCUBRIMIENTO &  │ → │ 2. TRIAJE (MOSCA)    │ → │ 3. DESPLIEGUE        │
│    CBOM              │   │ Priorización por     │   │    HÍBRIDO           │
│ Inventario cripto    │   │ riesgo conforme vida    │   │ Doble sobre clásico  │
│ em todos os sistemas│   │ útil de os dados    │   │ + PQC, cripto-ágil   │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### Fase 1 — Descubrimiento e nomenclatura criptográfica (CBOM)

No se pode planificar a migración de um parque criptográfico que no foi cartografiado, e a maioria de instituciones no disponen de um mapa exacto. La primeira fase é por tanto a producción de uma Cryptographic Bill of Materials —um inventario estructurado de cada instancia de criptografia asimétrica em a organização, etiquetada cada instancia por algoritmo, longitud de clave, contexto protocolar, sensibilidad de os dados e propietario do sistema—. El escaneo automatizado sobre as bases de código, aplicações web, imagens de contenedores, configuraciones de bancos de dados, almacenes de certificados, módulos HSM e interfaces de proveedor é o mecanismo prático; o inventario manual de os sistemas heredados e os protocolos propietarios é o complemento inevitable.

La saída de a Fase 1 no é glamurosa, mas é o único fundamento sobre ou que as Fases 2 e 3 podem descansar. Es também o entregable que a maioria de funciones de auditoría interna e reguladores externos buscarán primeiro quando se empiecen a pedir as atestaciones de cumplimiento PQC.

### Fase 2 — Triaje de riesgos com a ecuación de Mosca

Una vez a CBOM em mano, a institución pode aplicar o marco de Mosca activo por activo. Para cada dependencia criptográfica, a questão é si **S + M > Q** —si a vida útil de os dados mais o tempo de migración supera o tempo estimado hasta um CRQC—. Los activos onde a desigualdad é mais aguda —dados sensibles de larga vida útil sobre uma infraestrutura que tarda anos em migrar— passam ao frente de a fila. Los activos com vidas útiles de dados cortas ou uma infraestrutura ya modernizada podem secuenciarse mais tarde em o programa.

Esta é a fase onde o apetito de riesgo do consejo é mais visible. El valor Q que a institución elige como objetivo de planificación é, em efecto, uma apuesta estratégica sobre ou ritmo de os progresos do hardware quântico. Una Q conservadora (mediados de a década de 2030) produce um plan de migración mais agresivo e uma linha capex a curto prazo mais alta. Una Q optimista (post-2040) produce um plan mais relajado e uma exposición residual mais alta a os dados ya cosechados. Ninguna está equivocada; ambas deveriam ser decisões explícitas do consejo, no defectos implícitos de a función tecnológica.

### Fase 3 — Despliegue híbrido

Una vez identificados os activos prioritarios, o despliegue deveria seguir o esquema híbrido demostrado em Project Leap e validado por o NCSC, a ANSSI, o BSI e a folha de ruta do G7. Um despliegue híbrido faz funcionar um algoritmo clásico e um algoritmo pós-quântico em paralelo, combinando seus saídas em uma sola envolvente. El compuesto é seguro contra os ataques clásicos (o algoritmo clásico se sostiene hoje) e contra os ataques quânticos (o algoritmo PQC se sostiene amanhã). Concretamente, o esquema habitual é X25519 combinado com ML-KEM-768 ou ML-KEM-1024 para a encapsulación de claves, e ECDSA combinado com ML-DSA para as firmas quando as dobles firmas são operacionalmente factibles.

La constatación de Project Leap conforme a cual o híbrido é «muito, muito mais pesado» que cualquiera de os enfoques puros é o contrapeso honesto a essa recomendación. Los consejos deveriam anticipar uma subida de capacidade de cálculo e almacenamiento, handshakes mais largos e complexidade adicional de cadenas de certificados durante a transición. La compensación: o híbrido elimina a mayor fuente única de riesgo de migración: a bascula abrupta de um fundamento criptográfico a otro em entorno de producción.

## Cuánto cuesta e por que no fazer nada cuesta mais

El análisis de Mastercard, [reportado a principios de 2026 ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs"), cifró o coste mundial de a migración PQC do sector financeiro em 28-42 mil millones de dólares. Dentro de esse agregado, as [investigaciones de RedCompass Labs e CMORG ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") que seguem os gastos institucionales reales sugieren que os bancos de primer nivel comprometen entre 20 e 30 millones de dólares ao ano em programas de preparación, com calendarios de implementación que cubren vários ciclos de liderazgo. Son cantidades sustanciales. Sin embargo, no é a comparación pertinente.

La comparación pertinente é o coste de um solo evento de decifragem retroactivo. Para uma institución cuyo tráfico de transferencias cosechado, correspondencia M&A ou dados de exposición a contrapartes se vuelven legibles para um adversario em 2032, o coste operativo e reputacional no está acotado por a linha capex de migración. Está acotado por o valor de a década de informação estratégica subyacente, que, para cualquier institución sistémica, é materialmente superior a cualquier presupuesto de migración plausible. El encuadre do G7 conforme ou cual a transición criptográfica é uma questão de gestión de riesgos sistémicos em vez de uma actualización tecnológica é correcto, e os consejos deveriam abordarlo sobre essa base.

Hay uma segunda linha de coste que merece separarse. La migración a a PQC é uma función de forzamiento para a agilidade criptográfica: a capacidade arquitectónica para reemplazar os algoritmos criptográficos sem reconstruir os sistemas que dependen de eles. A maioria de instituciones no têm hoje agilidade criptográfica; seus dependencias RSA e ECC estão profundamente integradas em as PKI, as cadenas de firma de código, as integrações de proveedores e os protocolos caseros acumulados ao longo de as décadas. La investimento em agilidade, feita sob a presión de a transición PQC, é duradera. Se movilizará de novo quando llegue a próxima transición criptográfica, ya se trate de um sucesor de a PQC basada em retículos, de uma sobrecapa de QKD ou de otra cosa que ainda no esté em a folha de ruta de os estándares. Tratado correctamente, o capex de migración PQC é uma investimento puntual que reporta opcionalidad recurrente.

## Conclusión

El argumento a favor de tratar a migración pós-quântica como uma prioridad de consejo em 2026 no descansa em a inminencia de um CRQC. Las estimaciones ao respecto seguem siendo realmente inciertas: a opinión científica creíble sitúa a probabilidad de um CRQC para 2028 muito por embaixo do uno por ciento, ascendiendo a aproximadamente o cincuenta por ciento em o horizonte 2037-2040. El argumento descansa em três observaciones mais que no são inciertas.

Primero, o HNDL se produce hoje, e os dados com uma exigencia de confidencialidad de ao menos uma década estão expuestos independientemente de cuándo llegue o CRQC. Segundo, a migración do parque criptográfico de uma gran instituição financeira lleva de cinco a sete anos incluso com financiación adecuada e atención de a direção, lo que significa que o programa iniciado em 2026 termina rumo a 2031, bien dentro do extremo conservador de a distribución de probabilidad do CRQC. Tercero, as expectativas normativas tem-sen endurecido materialmente em os últimos doce meses, e as instituciones cuyas actas de consejo 2026 consignen um programa PQC claro estarán em uma posição sensiblemente mais fuerte que aquelas cuyas actas solo consignen uma vigilancia atenta.

Las instituciones que arrancan agora têm a ventaja de a elección. Pueden secuenciar o trabalho ao longo de vários ciclos de liderazgo, integrarlo com iniciativas de resiliencia mais amplias e absorber os costes operativos do despliegue híbrido em uma planificación capitalista normal. Las instituciones que esperan afrontarán o mesmo trabalho sob prazos mais ajustados, com menos margen de secuenciación, e sobre um trasfondo de restricciones de suministro de hardware PQC, experiência e capacidade de proveedores. El coste de actuar pronto é conhecido; o coste de actuar tarde é asimétrico precisamente de a maneira que a gestión de riesgos se diseña para evitar.

Para colocar este artigo em perspectiva em este sitio, o [artigo de abril de 2026 sobre a compresión de os umbrales quânticos](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") examinaba a trayectoria material subyacente, o [análisis de noviembre de 2023 sobre CRYSTALS-Kyber](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") cubría os fundamentos matemáticos agora estandarizados sob ML-KEM, o [artigo de diciembre de 2023 sobre a distribución quântica de claves](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") trataba de a sobrecapa [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) complementaria, e a [implementación de referencia open source KyberLib](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") proporciona uma implementación Rust operativa de as primitivas subyacentes para as instituciones que deseen inspeccionar directamente a superficie criptográfica. Implicarse em o detalle prático e técnico —no solo em os titulares normativos— é a maneira em que os consejos distinguen um programa de migración creíble de um teatro de cumplimiento.

## Preguntas frecuentes

**Cuándo existirá realmente um computador quântico criptográficamente relevante?**

Las estimaciones creíbles varían ampliamente. A principios de 2026, as demostraciones quânticas públicas alcançaram entre 24 e 28 qubits lógicos, enquanto que se estima que um CRQC requer em torno de 6.000 qubits lógicos sustentados por entre 100.000 e vários millones de qubits físicos, dependiendo do enfoque de corrección de errores. El consenso experto sitúa a probabilidad de um CRQC em menos do uno por ciento para 2028, em torno do cincuenta por ciento em o horizonte 2037-2040, com uma variabilidade significativa entre previsiones. Las recientes reducciones de as estimaciones teóricas de recursos —de 20 millones de qubits faz uns anos a menos de um millón em os trabalhos de Gidney em 2025, e a aproximadamente 100.000 em o artigo QLDPC de febrero de 2026— têm comprimido o horizonte de planificación. Para as necessidades de um consejo, a hipótesis de planificación apropiada é mediados de a década de 2030 para os sistemas de alto riesgo, finales de a década de 2030 como ponto meio conservador, e antes si a exposición HNDL é a preocupação limitante.

**Por que um despliegue híbrido em vez de pós-quântico puro?**

Tres razões. Primero, ML-KEM e ML-DSA, embora seriamente validados, têm historiales criptoanalíticos mais cortos que RSA e ECC. Um esquema híbrido segue siendo seguro si cualquiera de os componentes se sostiene; um esquema PQC puro queda expuesto si o problema sobre retículos se debilita inesperadamente. Segundo, o híbrido preserva a retrocompatibilidad com as contrapartes que ainda no têm migrado, crítico em uma transición industrial plurianual. Tercero, toda autoridade principal fora de a Australian Signals Directorate recomienda explícitamente o híbrido para o periodo de transición: NCSC, ANSSI, BSI, NLNCSA e o marco G7 validan todos o enfoque de doble envolvente. La compensación, como cuantificó Project Leap, é um sobrecoste materialmente mais alto em cálculo e almacenamiento. Es o precio de a opcionalidad.

**Hace falta a a vez ML-KEM e ML-DSA, ou se pode elegir?**

Ambos. ML-KEM e ML-DSA desempeñan roles criptográficos distintos. ML-KEM reemplaza as primitivas de establecimiento de clave em TLS, as VPN, a autenticação móvel e protocolos similares em os que dois partes devem convenir uma clave simétrica compartida. ML-DSA reemplaza as primitivas de firma digital em os certificados PKI, a firma de código, a firma de documentos, a mensajería autenticada tipo SWIFT e as aserciones de identidade. El parque criptográfico de uma institución utiliza os dois tipos de primitivas em distintos lugares; a migración deve cubrir ambos. El tamaño de firma significativamente mayor de ML-DSA (50-70× ECDSA) suele ser o mais exigente de os dois a nivel operativo; o trabalho de planificación de red e almacenamiento para ML-DSA domina a maioria de avaliações de capacidade de migración.

**Cómo medir o avance de um programa de este tamaño?**

Tres indicadores são práticos e se alinean com os principales marcos normativos. **Cobertura de a CBOM**: que porcentaje de as instancias criptográficas asimétricas de a institución tem-se inventariado, clasificado e etiquetado para prioridad de migración. **Cobertura de migración de os activos de alto riesgo**: que porcentaje de os activos onde a condición S + M > Q de Mosca é verdadera tem migrado a a PQC híbrida. **Cobertura de agilidade criptográfica**: que porcentaje de os sistemas com dependencia criptográfica pode reemplazar os algoritmos sem cambio de código, solo por configuración. La folha de ruta G7 CEG, o marco em três fases do NCSC e a folha de ruta coordinada UE se conectan todos a estas três medidas, incluso quando utilizam terminología diferente.

**Cuál é o coste de esperar um ano mais?**

No é nulo, e no é simétrico. Esperar um ano renuncia a um ano de protección HNDL sobre os dados de larga vida útil: os dados cuya exigencia de confidencialidad se extiende a 2040 quedan expuestos um ano mais de lo necessário. Comprime a ventana de migración frente a prazos normativos fijos (ASD 2030, hitos NSA CNSA 2.0, objetivo UE 2030 para os sistemas críticos), lo que se traduce em um riesgo de entrega mais alto e uma flexibilidade de secuenciación reducida. Expone a a institución a restricciones de suministro de proveedores e talento que ya são visibles em o mercado e que se agravarán quando os mayores actores do sector pasen de a planificación a a execução. El coste no é catastrófico em um solo ano, mas se compone, e o entorno normativo converge rumo a uma posição em a que os consejos tendrán que explicar o retraso em vez do gasto.

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
