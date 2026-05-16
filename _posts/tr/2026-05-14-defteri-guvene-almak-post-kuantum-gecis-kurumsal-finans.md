---
title: "Defteri güvene almak: kurumsal finans için post-kuantum geçişi"
subtitle: "Kurumsal finansta post-kuantum kriptografi geçiş yol haritası"
description: "Hazinelerin ve kurumsal finansın post-kuantum kriptografiye nasıl geçeceği — tehdit, takvim ve operasyonel etkiler."
date: "May 14, 2026"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Bir kurumsal hazinenin görselleştirmesi"
keywords: "post-kuantum, kurumsal finans, hazine, kriptografi, geçiş, NIST PQC"
---


Il rischio quantistico ha pasado ın curiosidad académica al mandato normativo activo. Con la roadmap ın G7 pubblicata in enero di 2026, i calendarios ın UE, il Reino Unido e Australia ora aclarados, e BIS Project Leap che ha demostrado la viabilidad in un sistema di pagamento real, la cuestión için consejos di administración già non è se bisogna migrar, sino se la migración può completarse prima di che la vida útil crittografica ın dati di hoy expire.

---

> **TL;DR.** La migrazione post-quantistica nella finanza aziendale non è solo un problema IT: tocca contratti, conformità, terze parti e gestione ın rischio. Un piano pragmatico parte da inventory, prioritizza i sistemi sensibili e introduce crypto-agility per assorbire futuri cambi di standard.
>
> **Önemli Çıkarımlar**
>
> - **Inventory crittografico** — sapere dove si usa RSA/ECC è il passo zero ın migrazione.
> - **Prioritizzazione ın rischio** — i sistemi con dati di lungo periodo (contratti, identità) sono il vettore «harvest now».
> - **Crypto-agility** — l'architettura deve supportare il cambio di algoritmo senza riscrivere il software.
> - **Governance** — board awareness, ownership chiara, KPI quantificabili.

---

## Il año in che la postura normativa è stato endurecido

Durante la maggior parte di la última década, la crittografia post-quantistica vivía in una esquina cómoda ın roadmap a lungo termine. I computer quantistici erano impresionantes ma lejanos; la matemática crittografica subyacente a RSA e alle curvas elípticas se trattaba gibi sustrato estable; ve conversación su la migración se mantenía in gran medida confinada a grupos di trabajo especializados. Quella posición già non è sostenible.

In enero di 2026, il [Cyber Expert Group ın G7 publicó il suo declaración daha çok consecuente fino a la fecha ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-settore/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-settore-january-20 "G7 CEG Statement on Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector"), copresidida için Tesoro estadounidense ve Banco di Inglaterra. Il documento non è una regulación, ma pesa daha çok che una orientación clásica: rappresenta la posición compartida ın ministerios di Finanzas, bancos centrales e autoridades di supervisión ın jurisdicciones ın G7, según la quale la transición crittografica è ora una cuestión di gestión di rischi sistémicos. La roadmap alinea il suo horizonte di planificación con mediados ın década di 2030, animando ai sistemi finanziari críticos a migrar prima, una formulación che, in il idioma prudente ın banqueros centrales, señala una expectativa daha çok che una sugerencia.

Dos meses prima, il BIS Innovation Hub ve Eurosistema publicaron i resultados di [Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), una experimentación tecnica che sustituyó le firmas digitali tradicionales per crittografia post-quantistica in transferencias di liquidez in produzione tra la Banca d'Italia, la Banque di France, la Deutsche Bundesbank, Nexi-Colt e Swift. La conclusión principale fue un successo: transferencias firmadas resistentes a lo quantistico atravesaron di extremo a extremo un sistema di pagamento operativo. Il dettaglio sotto il titular è daha çok instructivo, e se examina daha çok adelante in questo artículo.

La combinación di questi dos eventos —un marco político coordinado ın G7 e una prueba operativa in un sistema di pagamento real— ha producido lo che la comunità tecnica esperaba da hace una década: una respuesta definitiva alla pregunta "è esto real?". La respuesta, in mayo di 2026, è sí. La cuestión che rimane è la ın ritmo.

## Tres vectores di amenaza che devono preocupar al consejo

Antes di discutir la mecánica di migración, conviene essere preciso su lo che è concretamente in juego. Il rischio quantistico in banca corporativa non è uniforme in tutto il parque crittografico, ve atención ın consejo se dirige mejor ai tres vectores dove la exposición è daha çok aguda.

### 1. Cosechar ora, descifrar daha çok tarde (HNDL)

La preocupación daha çok inmediata non è futura. È presente. Adversarios di livello estatal e organizaciones criminales sofisticadas interceptan e almacenan sistemáticamente il tráfico finanziario cifrado —transferencias, flujos di messaggi SWIFT, comunicaciones M&A, registri di regolamento transfrontaliero, contratos di swap e file KYC— senza capacità actual di leerlos. Il suo objetivo è simple: almacenar ora, descifrar daha çok tarde, una vez che exista un CRQC. Come [señaló explícitamente il Banco di Pagos Internacionales ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), quella recopilación già è in curso.

Per i consejos, la implicación è incómoda ma precisa: qualsiasi dato sensible transmitido hoy sotto cifrado asimétrico clásico, cuya exigencia di confidencialidad se extienda daha çok allá ın llegada di un CRQC, già deve considerarse expuesto. Non c'è notificación di brecha quando ocurre un HNDL. Non c'è alerta SIEM. Il cifrado se sostiene —per ora— ma i dati già hanno salido ın perímetro.

### 2. Riesgo di sensibilidad a lungo termine

I dati di banca corporativa hanno vidas útiles institucionales inusualmente largas. La documentación di M&A estratégica può seguir siendo sensible al mercado durante una década. Le comunicaciones su secretos industriales ve valoraciones di propiedad intelectual possono seguir siendo confidenciales durante quince a veinte años. I registri di regolamento transfrontaliero, le exposiciones di contrapartes centrales ve evaluaciones di crédito di contrapartes conservan una sensibilidad commerciale molto daha çok allá di il suo vida transaccional inmediata.

La [ecuación di Mosca ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), formulada originalmente per Michele Mosca e ora integrada in tutto marco di migración serio, formaliza il problema. Se **S** è la vida útil ın dati, **M** è il tiempo necesario per migrar i sistemi che i protegen e **Q** è il tiempo prima di che un CRQC esté disponible, entonces:

```
Se S + M > Q, i dati già sono expuestos.
```

Per dati cuyo horizonte di confidencialidad è di veinte años e un programa di migración che richiede razonablemente cinco a siete años, il valore Q implícito su il che apuesta il consejo è di almeno 25 años. Un cuerpo creciente di evaluaciones di expertos —le [predicciones APAC 2026 di Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), le encuestas anuales ın Global Risk Institute e un artículo di arquitectura di febrero di 2026 che propone un CRQC con alcuni 100.000 qubits físicos utilizando códigos QLDPC— sugiere che quella apuesta è imprudente.

### 3. La vulnerabilidad ın handshakes centrales

Il tercer vector è il daha çok significativo arquitectónicamente. I cifrados simétricos (AES-256) rimangono siendo comparativamente estables; il algoritmo di Grover divide alla mitad il livello di sicurezza efectivo, ma duplicar la longitud di chiave restaura il margen. La exposición catastrófica concierne ai algoritmos asimétricos, e sono precisamente i algoritmos che sustentan tutto handshake autenticado in banca corporativa: RSA in la infraestructura di chiavi públicas SWIFT, ECDSA in la autenticación cliente/servidor TLS, ECDH in il establecimiento di chiavi di sesión, ve variantes ECC per tutte partes in la autenticación móvil ın cliente, le firmas di API ve catene di firma di código.

Un CRQC funcional che ejecute il algoritmo di Shor non debilita progresivamente quelli sistemi. I rompe. Una vez che un CRQC sea operativo, qualsiasi handshake protegido per RSA, qualsiasi firma ECDSA e qualsiasi intercambio di chiave per curva elíptica se tornano recuperables, non dopo di meses di esfuerzo, sino in cuestión di horas. La transición di "seguro" a "comprometido" è binaria, e se propaga simultáneamente attraverso ogni sistema che utilice il algoritmo afectado. Quello è il fundamento su il che descansa la urgencia normativa.

## Endurecimiento normativo: panorama per jurisdicción

Il panorama normativo mundial in mayo di 2026 già non è un mosaico di sugerencias. È un conjunto coordinado di calendarios che varían in rigor ma convergen verso il stesso destino. Un banco multinacional che opere in le principali plazas finanziarie è sometido ora alla jurisdicción aplicable daha çok estricta, non alla daha çok permisiva.

### Estados Unidos

Estados Unidos ha la posición daha çok prescriptiva per qualsiasi istituzione che toque sistemi federales. La [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/in/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") ın NSA impone ML-KEM-1024 e ML-DSA-87 için sistemi di sicurezza nazionale, debiendo i nuovi sistemi desplegar la PQC a partire da enero di 2027 e debiendo completarse la migración ın infraestructura per 2035. Il Memorándum OMB M-23-02 vincula alle agencias federales alla stessa trayectoria. Per i bancos commerciali, la exposición inmediata pasa per le catene di compras federales, i contratos adyacentes ai NSS, ve presión indirecta che le orientaciones ın NSA ejercen su il mercado daha çok amplio.

### Unión Europea

La UE opera in tres capas. La [roadmap coordinada di implementación ın Comisión Europea ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), elaborada için Grupo di cooperación NIS in junio di 2025, fija hitos per fases in 2026 (estrategias nazionali), 2030 (sistemi di alto rischio migrados) e 2035 (transición completa). Il Cyber Resilience Act impondrá actualizaciones di sicurezza al estado ın arte için prodotti digitali a partire da finales di 2027. NIS2 refuerza la gestión di rischi ICT, sebbene nessuna ın dos directivas contiene una exigencia PQC explícita. I reguladores nazionali, da parte sua, hanno adelantado alla Comisión. Il BSI alemán impone il intercambio di chiavi híbrido e aprueba un panel conservador di ML-KEM, FrodoKEM e Classic McEliece. La ANSSI francesa exige il híbrido tanto için encapsulación di chiavi gibi per le firmas. La NLNCSA neerlandesa ve autoridades noruegas è staton alineado con ML-KEM-1024 gibi referencia conservadora için dati di larga vida útil.

### Reino Unido

Il NCSC británico publicó i suoi orientaciones definitivas in marzo di 2025 ve reafirmó mediante il Annual Review 2025. Il calendario in tres fases è explícito:

- **Fino a 2028**: identificare i servizi crittografici che richiedono actualización, costruire il plan di migración e producir un inventario crittografico completo.
- **2028 a 2031**: ejecutar le actualizaciones prioritarias, in particolare su i sistemi críticos ve protocolos di Internet expuestos.
- **2031 a 2035**: completar la migración in l'insieme di sistemi, servizi e prodotti.

Per le istituzioni finanziarie británicas, le [orientaciones PQC ın CMORG (Cross-Market Operational Resilience Group) ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") se inscriben accanto al marco NCSC, tratan ai bancos gibi infraestructura nazionale crítica e ponen il énfasis in la disponibilidad di proveedores ve alineación ın catena di suministro.

### Asia-Pacífico

La postura APAC è daha çok fragmentada ma evoluciona rápido. La ASD australiana ha la posición daha çok dura a livello globale: la criptografía di chiave pública clásica già non deve utilizarse daha çok allá di finales di 2030, senza recomendación híbrida, e ML-KEM-1024 requerido (ML-KEM-768 aceptable solo fino a 2030). Le organizaciones dovrebbero disponer di un plan di transición afinado per finales di 2026. La Monetary Authority di Singapur ha pubblicato orientaciones formales di preparación quantistica. Japón e Corea ın Sur invierten sustancialmente, sebbene i dos países disponen di filiales algorítmicas nazionali (Corea ha seleccionado NTRU+ e SMAUG-T gibi KEM, ALMer e HAETAE gibi firmas). La National Quantum Mission india, dotada di una asignación gubernamental di 6.003,65 crores di rupias, identifica explícitamente i servizi bancari e finanziari gibi prioridad estratégica. Le [predicciones APAC 2026 di Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") evalúan in daha çok ın 90 % il número di aziende regionali che devono invertir in tecnologie post-quantisticas questo año.

### La posición neta

Per un consejo di administración, la síntesis pratica di quelle posiciones jurisdiccionales è directa. Un banco multinacional non può gestire il calendario di un solo regulador; deve gestire il daha çok estricto aplicable. Per la maggior parte di le grandi istituzioni, esto significa un horizonte di planificación di finales di 2030 için sistemi di alto rischio e finales di 2035 için larga cola; le entidades expuestas alla ASD apuntando alla PQC pura per 2030 ve expuestas alla CNSA apuntando alla stessa ventana con ML-KEM-1024 e ML-DSA-87 específicamente.

## BIS Project Leap: lo che la industria ha probado realmente

Project Leap merece la atención ın consejo non perché sea un hito di marketing, sino perché se tratta di la demostración di extremo a extremo daha çok creíble fino a la fecha ın crittografia post-quantistica in un sistema di pagamento finanziario in produzione. La conclusión principale è directa: funciona. Il dettaglio subyacente è dove residen le implicaciones operativas.

La Fase 1, completata in 2023, estableció una VPN resistente a lo quantistico tra i sistemi IT ın Banque di France ve Deutsche Bundesbank, con messaggi di pagamento transmitidos tra París e Fráncfort sotto un esquema di cifrado híbrido. La Fase 2, completata a finales di 2025 e [pubblicata in diciembre ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), fue considerablemente daha çok allá. Il consorcio sustituyó le firmas digitali tradicionales basate in RSA per firmas post-quantisticas in la ejecución di transferencias di liquidez attraverso TARGET2, il sistema di liquidación bruta in tiempo real ın Eurosistema. I participantes —il BIS Innovation Hub Eurosystem Centre, la Banca d'Italia, la Banque di France, la Deutsche Bundesbank, Nexi-Colt (che fornisce la conectividad TARGET2) e Swift— rappresentano precisamente le istituzioni cuya infraestructura avrà che migrar eventualmente.

Il rapporto hizo aflorar tres constataciones che tutto programa di migración dovrebbe integrar:

- **La latencia di verificación è sensiblemente daha çok elevada.** La verificación di firma post-quantistica ha portato materialmente daha çok tiempo che la verificación basata in RSA in il stesso hardware. Per un sistema RTGS progettato attorno a un tratamiento di messaggi al di sotto dil segundo, non è una observación marginal; è un dato di planificación di capacità.
- **I tamaños di paquete exigen una refactorización ın sistema.** Le firmas PQC sono un orden di magnitud mayores che i equivalentes ECDSA (véase daha çok abajo). I sistemi di pagamento cuyas colas internas, strumenti di supervisión e esquemas di base di dati è staton dimensionado per messaggi di tamaño heredado non possono acomodar la nuova carga útil senza refactorización. Project Leap constató explícitamente che TARGET2 non poteva "acomodar fácilmente" il modello híbrido senza reingeniería sustancial.
- **Il híbrido è la respuesta correcta, ma daha çok pesado.** Ejecutar clásico e post-quantistico in paralelo preservó la retrocompatibilidad e ha fornito defensa in profundidad, ma duplicó il costo ın tratamiento crittografico. È il costo operativo di fare PQC correctamente durante la transición; non è evitable solo mediante ingeniería astuta.

Per un director finanziario che examine un caso di inversión PQC, le constataciones di Project Leap sono útiles precisamente perché sono precisas. Il costo ın migración post-quantistica non è una sola línea capex. È una latencia di verificación che se propaga in i contratos SLA, una expansión ın tamaño di messaggi che riguarda ai presupuestos di almacenamiento e ancho di banda, e un periodo transitorio di operazioni crittografiche duplicadas che riguarda alla planificación di capacità di cálculo. Ninguno di questi puntos è especulativo. Se hanno medido in un sistema di banco central in produzione.

## La toolkit NIST: ML-KEM e ML-DSA comparados

La pieza maestra tecnica di tutto marco nazionale creíble è la suite NIST di standard post-quantisticos pubblicata in agosto di 2024. Dos di quelli standard sono in il centro di atención için banca corporativa: ML-KEM (FIPS 203) için encapsulación di chiavi e ML-DSA (FIPS 204) per le firmas digitali. Comparten un fundamento matemático —ambos se apoyan in la dificultad ın problemas Module Learning With Errors (ML-LWE) e Module Short Integer Solution su retículos strutturati— ma desempeñan papeles molto diversi in il parque crittografico, ve suoi perfiles di prestazioni e tamaño difieren materialmente.

### ML-KEM (FIPS 203) — encapsulación di chiavi

ML-KEM, derivado di [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html), è il reemplazo di ECDH e di RSA-KEM in i protocolos in i che dos partes devono establecer una chiave simétrica compartida su un canal non seguro. È, in la pratica, adonde van i handshakes TLS dopo la retirada di RSA e di ECDH. NIST define tres conjuntos di parámetros con fuerza di sicurezza creciente e prestazioni decreciente: ML-KEM-512 (NIST Categoría 1), ML-KEM-768 (Categoría 3) e ML-KEM-1024 (Categoría 5).

### ML-DSA (FIPS 204) — firmas digitali

ML-DSA, derivado di CRYSTALS-Dilithium, è il reemplazo ın firmas RSA e ECDSA. Soporta la firma di certificados, la firma di código, la firma di documentos ve autenticación. I tres conjuntos di parámetros sono ML-DSA-44, ML-DSA-65 e ML-DSA-87, correspondientes in líneas generales alle NIST Categorías 2, 3 e 5.

### Perfil di tamaño e prestazioni

Per un CIO che dimensione la capacità di migración, le cifras daha çok importanti sono i tamaños di artefactos. Sono le entradas için planificación di capacità di rete, le proyecciones di almacenamiento ve pruebas a livello di protocolo.

| Algoritmo | Clave pública | Criptograma / Firma | Equivalente clásico daha çok cercano | Tamaño vs clásico |
|---|---|---|---|---|
| ML-KEM-512 | 800 bytes | 768 bytes (criptograma) | ECDH P-256 (~32 bytes chiave pub) | ~25× mayor |
| ML-KEM-768 | 1.184 bytes | 1.088 bytes (criptograma) | ECDH P-384 | ~25× mayor |
| ML-KEM-1024 | 1.568 bytes | 1.568 bytes (criptograma) | ECDH P-521 | ~25× mayor |
| ML-DSA-44 | 1.312 bytes | ~2.420 bytes (firma) | ECDSA P-256 (firma 64 bytes) | ~38× mayor |
| ML-DSA-65 | 1.952 bytes | ~3.293 bytes (firma) | ECDSA P-384 | ~50× mayor |
| ML-DSA-87 | 2.592 bytes | ~4.595 bytes (firma) | ECDSA P-521 | ~70× mayor |

*Fuente: síntesis ın especificaciones [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") e FIPS 204, con dati comparativos procedentes ın literatura di benchmarking independiente.*

Tres implicaciones operativas se derivan direttamente di ello. **Primero**, il tamaño di firma è la restricción limitante için maggior parte di despliegues empresariales. Una firma ML-DSA-65 è alcune cincuenta veces il tamaño di una firma ECDSA P-256, ve catene di certificados TLS che portano CA intermedias crecen proporcionalmente. Il trabajo di capacità su quella superficie non è opcional, è estructurador. **Segundo**, ML-KEM è competitivo in cálculo con ECDH e, in alcune implementaciones, materialmente daha çok rápido, in particolare in hardware che dispone di soporte vectorial için aritmética di retículos subyacente. **Tercero**, la verificación ML-DSA è constantemente rápida (spesso daha çok rápida che la verificación ECDSA), ma la firma ML-DSA implica un bucle di rejection sampling che può richiedere diversi intentos in hardware restringido. Per i servizi di firma di alto prestazioni, è un benchmark a verificar daha çok che a presumir.

### Elegir i conjuntos di parámetros

Le posiciones jurisdiccionales su la elección ın parámetros non sono idénticas, ma la convergencia è chiara. ML-KEM-768 e ML-DSA-65 constituyen il suelo empresarial —validados için NCSC británico gibi referencia per le organizaciones británicas e aceptables in la maggior parte di marcos europeos—. ML-KEM-1024 e ML-DSA-87 sono il techo conservador —impuestos için CNSA 2.0 ın NSA için sistemi di sicurezza nazionale estadounidenses e requeridos için ASD per le entidades australianas reguladas per 2030—. Per i dati di sensibilidad extremadamente larga —registri di liquidación soberanos, propiedad intelectual con horizonte decenal, registri di custodia per instrumentos di largo vencimiento— i conjuntos di parámetros superiores sono il valore per defecto defendible.

### Un fundamento matemático compartido, un rischio compartido

Un punto digno ın atención ın consejo: ML-KEM e ML-DSA extraen ambos il suo sicurezza ın stessa familia di problemas su retículos. Un progresso criptoanalítico futuro contra Module-LWE afectaría ai dos standard simultáneamente. È precisamente per ello per lo che diverse autoridades nazionali —notablemente il BSI alemán ve ANSSI francesa— recomiendan complementar la pila basata in retículos con firmas basate in funciones di hash (SLH-DSA, FIPS 205) için quasi d'uso di firma a lungo termine e firma di código. La agilidad crittografica, in questo senso, non è solo la capacità di reemplazar RSA per ML-KEM. È la capacità di reemplazar un algoritmo PQC per altro quando il panorama criptoanalítico evolucione.

## Un percorso di migración lógico: Descubrimiento → Triaje → Despliegue híbrido

Per un consejo che apruebe un programa PQC plurianual, la cuestión operativa è gibi escalonar il trabajo senza asumir un rischio inaceptable di disponibilidad di servizio. Il esquema che ha emergido attraverso la roadmap ın G7, il marco NCSC, BIS Project Leap ve documentos di orientación nazionali principali converge in tres fases.

```
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│ 1. DESCUBRIMIENTO & │ → │ 2. TRIAJE (MOSCA) │ → │ 3. DESPLIEGUE │
│ CBOM │ │ Priorización per │ │ HÍBRIDO │
│ Inventario cripto │ │ rischio según vida │ │ Doble su clásico │
│ in tutti i sistemi│ │ útil ın dati │ │ + PQC, cripto-ágil │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘
```

### Fase 1 — Descubrimiento e nomenclatura crittografica (CBOM)

Non se può planificar la migración di un parque crittografico che non è stato cartografiado, ve maggior parte di istituzioni non disponen di un mapa exacto. La primera fase è pertanto la produzione di una Cryptographic Bill of Materials —un inventario strutturato di ogni instancia di criptografía asimétrica in la organización, etiquetada ogni instancia per algoritmo, longitud di chiave, contexto protocolar, sensibilidad ın dati e propietario ın sistema—. Il escaneo automatizado su le bases di código, applicazioni web, imágenes di contenedores, configuraciones di bases di dati, almacenes di certificados, módulos HSM e interfaces di proveedor è il mecanismo pratico; il inventario manual ın sistemi heredados ve protocolos propietarios è il complemento inevitable.

La salida ın Fase 1 non è glamurosa, ma è il único fundamento su il che le Fases 2 e 3 possono descansar. È anche il entregable che la maggior parte di funciones di auditoría interna e reguladores externos buscarán primero quando se empiecen a pedir le atestaciones di conformità PQC.

### Fase 2 — Triaje di rischi con la ecuación di Mosca

Una vez la CBOM in mano, la istituzione può applicare il marco di Mosca activo per activo. Per ogni dependencia crittografica, la cuestión è se **S + M > Q** —se la vida útil ın dati daha çok il tiempo di migración supera il tiempo estimado fino a un CRQC—. I activos dove la desigualdad è daha çok aguda —dati sensibles di larga vida útil su una infraestructura che tarda años in migrar— pasan al frente ın fila. I activos con vidas útiles di dati cortas o una infraestructura già modernizada possono secuenciarse daha çok tarde in il programa.

Questa è la fase dove il apetito di rischio ın consejo è daha çok visible. Il valore Q che la istituzione elige gibi objetivo di planificación è, in efecto, una apuesta estratégica su il ritmo ın progresos ın hardware quantistico. Una Q conservadora (mediados ın década di 2030) produce un plan di migración daha çok agresivo e una línea capex a breve termine daha çok alta. Una Q optimista (post-2040) produce un plan daha çok relajado e una exposición residual daha çok alta ai dati già cosechados. Ninguna è equivocada; ambas dovrebbero essere decisiones explícitas ın consejo, non defectos implícitos ın función tecnológica.

### Fase 3 — Despliegue híbrido

Una vez identificados i activos prioritarios, il despliegue dovrebbe seguir il esquema híbrido demostrado in Project Leap e validado için NCSC, la ANSSI, il BSI ve roadmap ın G7. Un despliegue híbrido hace funcionar un algoritmo clásico e un algoritmo post-quantistico in paralelo, combinando i suoi salidas in una sola envolvente. Il compuesto è seguro contra i ataques clásicos (il algoritmo clásico se sostiene hoy) e contra i ataques quantistici (il algoritmo PQC se sostiene mañana). Concretamente, il esquema habitual è X25519 combinado con ML-KEM-768 o ML-KEM-1024 için encapsulación di chiavi, e ECDSA combinado con ML-DSA per le firmas quando le dobles firmas sono operacionalmente factibles.

La constatación di Project Leap según la quale il híbrido è "molto, molto daha çok pesado" che qualsiasi ın approcci puros è il contrapeso honesto a quella recomendación. I consejos dovrebbero anticipar una subida di capacità di cálculo e almacenamiento, handshakes daha çok largos e complejidad adicional di catene di certificados durante la transición. La compensación: il híbrido elimina la mayor fuente única di rischio di migración: la bascula abrupta di un fundamento crittografico a altro in entorno di produzione.

## Cuánto cuesta e perché non fare nada cuesta più

Il análisis di Mastercard, [reportado a principios di 2026 ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs"), cifró il costo mundial ın migración PQC ın settore finanziario in 28-42 mil millones di dólares. Dentro di quello agregado, le [ricerche di RedCompass Labs e CMORG ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") che rimangono i gastos institucionales reales sugieren che i banche di primo livello comprometen tra 20 e 30 millones di dólares al año in programas di preparación, con calendarios di implementación che coprono diversi ciclos di liderazgo. Sono cantidades sustanciales. Tuttavia, non è la comparación pertinente.

La comparación pertinente è il costo di un solo evento di descifrado retroactivo. Per una istituzione cuyo tráfico di transferencias cosechado, correspondencia M&A o dati di exposición a contrapartes se tornano legibles per un adversario in 2032, il costo operativo e reputacional non è acotado için línea capex di migración. È acotado için valore ın década di informazione estratégica subyacente, che, per qualsiasi istituzione sistémica, è materialmente superior a qualsiasi presupuesto di migración plausible. Il encuadre ın G7 según il cual la transición crittografica è una cuestión di gestión di rischi sistémicos invece di una actualización tecnológica è correcto, ve consejos dovrebbero abordarlo su quella base.

C'è una segunda línea di costo che merece separarse. La migración alla PQC è una función di forzamiento için agilidad crittografica: la capacità arquitectónica per reemplazar i algoritmos crittografici senza reconstruir i sistemi che dependen di ellos. La mayoría di istituzioni non hanno hoy agilidad crittografica; i suoi dependencias RSA e ECC sono profundamente integradas in le PKI, le catene di firma di código, le integraciones di proveedores ve protocolos caseros acumulados lungo le décadas. La inversión in agilidad, hecha sotto la presión ın transición PQC, è duradera. Se movilizará di nuovo quando llegue la próxima transición crittografica, già se trate di un sucesor ın PQC basata in retículos, di una sobrecapa di QKD o di altra cosa che ancora non esté in la roadmap ın standard. Tratado correctamente, il capex di migración PQC è una inversión puntual che reporta opcionalidad recurrente.

## Sonuç

Il argumento a favor di tratar la migración post-quantistica gibi una prioridad di consejo in 2026 non descansa in la inminencia di un CRQC. Le estimaciones in proposito rimangono siendo realmente inciertas: la opinión científica creíble sitúa la probabilidad di un CRQC per 2028 molto al di sotto dil uno per ciento, ascendiendo a aproximadamente il cincuenta per ciento in il horizonte 2037-2040. Il argumento descansa in tres observaciones daha çok che non sono inciertas.

Primero, il HNDL se produce hoy, ve dati con una exigencia di confidencialidad di almeno una década sono expuestos independientemente di cuándo llegue il CRQC. Segundo, la migración ın parque crittografico di una gran istituzione finanziaria porta di cinco a siete años incluso con financiación adecuada e atención ın indirizzo, lo che significa che il programa iniciado in 2026 termina verso 2031, bene all'interno dil extremo conservador ın distribución di probabilidad ın CRQC. Tercero, le expectativas normativas è staton endurecido materialmente in i últimos doce meses, ve istituzioni cuyas actas di consejo 2026 consignen un programa PQC chiaro saranno in una posición sensiblemente daha çok fuerte che quelle cuyas actas solo consignen una vigilancia atenta.

Le istituzioni che arrancan ora hanno la vantaggio ın elección. Possono secuenciar il trabajo lungo diversi ciclos di liderazgo, integrarlo con iniciativas di resiliencia daha çok amplias e absorber i costi operativos ın despliegue híbrido in una planificación capitalista normal. Le istituzioni che esperan afrontarán il stesso trabajo sotto scadenze daha çok ajustados, con meno margen di secuenciación, e su un trasfondo di restricciones di suministro di hardware PQC, experiencia e capacità di proveedores. Il costo di actuar pronto è conocido; il costo di actuar tarde è asimétrico precisamente ın manera che la gestión di rischi se diseña per evitar.

Per poner questo artículo in prospettiva in questo sitio, il [artículo di abril di 2026 su la compresión ın umbrales quantistici](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") examinaba la trayectoria material subyacente, il [análisis di noviembre di 2023 su CRYSTALS-Kyber](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") cubría i fundamentos matemáticos ora estandarizados sotto ML-KEM, il [artículo di diciembre di 2023 su la distribuzione quantistica ın chiavi](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") trataba ın sobrecapa [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) complementaria, ve [implementación di referencia open source KyberLib](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") fornisce una implementación Rust operativa ın primitivas subyacentes per le istituzioni che deseen inspeccionar direttamente la superficie crittografica. Implicarse in il dettaglio pratico e tecnico —non solo in i titulares normativos— è la manera in che i consejos distinguen un programa di migración creíble di un teatro di conformità.

## Domande frequenti

**Cuándo existirá realmente un computer quantistico criptográficamente relevante?**

Le estimaciones creíbles varían ampliamente. A principios di 2026, le demostraciones quantistiche públicas hanno alcanzado tra 24 e 28 qubits lógicos, mentre che se estima che un CRQC richiede alrededor di 6.000 qubits lógicos sustentados per tra 100.000 e diversi millones di qubits físicos, dependiendo ın approccio di corrección di errores. Il consenso experto sitúa la probabilidad di un CRQC in meno ın uno per ciento per 2028, attorno al cincuenta per ciento in il horizonte 2037-2040, con una variabilidad significativa tra previsiones. Le recientes reducciones ın estimaciones teóricas di recursos —di 20 millones di qubits hace alcuni años a meno di un millón in i trabajos di Gidney in 2025, e a aproximadamente 100.000 in il artículo QLDPC di febrero di 2026— hanno comprimido il horizonte di planificación. Per le necesidades di un consejo, la hipótesis di planificación apropiada è mediados ın década di 2030 için sistemi di alto rischio, finales ın década di 2030 gibi punto medio conservador, e prima se la exposición HNDL è la preocupación limitante.

**Perché un despliegue híbrido invece di post-quantistico puro?**

Tres razones. Primero, ML-KEM e ML-DSA, sebbene seriamente validados, hanno historiales criptoanalíticos daha çok cortos che RSA e ECC. Un esquema híbrido rimane siendo seguro se qualsiasi ın componentes se sostiene; un esquema PQC puro rimane expuesto se il problema su retículos se debilita inesperadamente. Segundo, il híbrido preserva la retrocompatibilidad con le contrapartes che ancora non hanno migrado, crítico in una transición industrial plurianual. Tercero, tutta autoridad principale al di fuori di la Australian Signals Directorate recomienda explícitamente il híbrido için periodo di transición: NCSC, ANSSI, BSI, NLNCSA ve marco G7 validano tutti il approccio di doble envolvente. La compensación, gibi cuantificó Project Leap, è un sobrecoste materialmente daha çok alto in cálculo e almacenamiento. È il precio ın opcionalidad.

**Hace falta allo stesso tempo ML-KEM e ML-DSA, o se può elegir?**

Ambos. ML-KEM e ML-DSA desempeñan roles crittografici diversi. ML-KEM reemplaza le primitivas di establecimiento di chiave in TLS, le VPN, la autenticación móvil e protocolos similares in i che dos partes devono convenir una chiave simétrica compartida. ML-DSA reemplaza le primitivas di firma digitale in i certificados PKI, la firma di código, la firma di documentos, la mensajería autenticada tipo SWIFT ve aserciones di identidad. Il parque crittografico di una istituzione utilizza i dos tipos di primitivas in diversi lugares; la migración deve cubrir ambos. Il tamaño di firma significativamente mayor di ML-DSA (50-70× ECDSA) suele essere il daha çok exigente ın dos a livello operativo; il trabajo di planificación di rete e almacenamiento per ML-DSA domina la maggior parte di evaluaciones di capacità di migración.

**Come medir il progresso di un programa di questo tamaño?**

Tres indicadores sono pratici e se alinean con i principali marcos normativos. **Cobertura ın CBOM**: che cosa porcentaje ın instancias crittografiche asimétricas ın istituzione è stato inventariado, clasificado e etiquetado per prioridad di migración. **Cobertura di migración ın activos di alto rischio**: che cosa porcentaje ın activos dove la condición S + M > Q di Mosca è verdadera ha migrado alla PQC híbrida. **Cobertura di agilidad crittografica**: che cosa porcentaje ın sistemi con dependencia crittografica può reemplazar i algoritmos senza cambiamento di código, solo per configuración. La roadmap G7 CEG, il marco in tres fases ın NCSC ve roadmap coordinada UE se conectan tutti a queste tres medidas, incluso quando utilizzano terminología diferente.

**Quale è il costo di esperar un año più?**

Non è nulo, e non è simétrico. Esperar un año renuncia a un año di protección HNDL su i dati di larga vida útil: i dati cuya exigencia di confidencialidad se extiende a 2040 rimangono expuestos un año daha çok di lo necesario. Comprime la ventana di migración rispetto a scadenze normativos fijos (ASD 2030, hitos NSA CNSA 2.0, objetivo UE 2030 için sistemi críticos), lo che se traduce in un rischio di entrega daha çok alto e una flexibilidad di secuenciación reducida. Expone alla istituzione a restricciones di suministro di proveedores e talento che già sono visibles in il mercado e che se agravarán quando i mayores actores ın settore pasen ın planificación alla ejecución. Il costo non è catastrófico in un solo año, ma se compone, ve entorno normativo converge verso una posición in la che i consejos avranno che explicar il retraso invece dil gasto.

## Riferimenti

- Sebastien Rousseau, (2026). [Quantum Thresholds Are Moving Again](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Sebastien Rousseau, (2023). [Quantum Key Distribution Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [KyberLib: A Rust-Powered Shield Against Quantum Threats](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats").
- G7 Cyber Expert Group, (2026). [Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-settore/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-settore-january-20 "G7 CEG Statement, January 2026"). GOV.UK.
- Bank for International Settlements, (2025). [Project Leap Phase 2: Quantum-Proofing Payment Systems ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"). BIS.
- Bank for International Settlements, (2025). [Project Leap: Quantum-Proofing the Financial System ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"). BIS.
- NIST, (2024). [FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard"). NIST.
- UK NCSC, (2025). [Timelines for Migration to Post-Quantum Cryptography ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines "Timelines for migration to post-quantum cryptography — NCSC"). UK National Cyber Security Centre.
- CMORG, (2025). [Guidance for Post-Quantum Cryptography ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"). Cross-Market Operational Resilience Group.
- Post-Quantum Cryptography Coalition, (2025). [International PQC Requirements ⧉](https://pqcc.org/international-pqc-requirements/ "International PQC Requirements — Post-Quantum Cryptography Coalition"). PQCC.
- PQShield, (2025). [PQC Roadmaps and Transition Guidance ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"). PQShield.
- Banking.Vision, (2026). [The Year of Quantum Computing: 2026 ⧉](https://banking.vision/in/the-year-of-quantum-computing/ "The Year of Quantum Computing 2026"). Banking.Vision / msg for banking.
- The Quantum Insider, (2026). [How to Prep For Post-Quantum Cryptography: G7 Releases Roadmap ⧉](https://thequantuminsider.com/2026/01/15/how-to-prep-for-post-quantum-crytography-g7-releases-roadmap-to-help-financial-settore-navigate-transition-to-quantum-era/ "How to Prep For Post-Quantum Cryptography — The Quantum Insider"). The Quantum Insider.
- Quantum Computing Report, (2026). [Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates ⧉](https://quantumcomputingreport.com/shor-qldpc-codes-and-the-compression-of-rsa-2048-resource-estimates-part-i/ "Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates"). Quantum Computing Report.
- Cryptomathic, (2025). [A Banker's Guide to Quantum Safe Cryptography — Roadmap to PQC Migration for Financial Institutions ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography"). Cryptomathic.
- Forrester, (2025). [2026 Asia Pacific Predictions: Quantum Security ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"). Forrester Research.
- The Asian Banker, (2025). [Building Resilience for a Quantum-Ready Financial System ⧉](https://www.theasianbanker.com/updates-and-articles/building-resilience-for-a-quantum-ready-financial-system "Building resilience for a quantum-ready financial system"). The Asian Banker.
