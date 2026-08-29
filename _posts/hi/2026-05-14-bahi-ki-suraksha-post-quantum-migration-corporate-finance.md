---
title: "बही की सुरक्षा: कॉर्पोरेट-वित्त में पोस्ट-क्वांटम माइग्रेशन"
subtitle: "ट्रेज़री-संचालन और लेखा-बही के लिए एक क्रिप्टो-चपलता रोडमैप"
description: "कॉर्पोरेट-वित्त के लिए पोस्ट-क्वांटम माइग्रेशन — ट्रेज़री, बही और क्रिप्टो-चपलता हेतु एक रोडमैप।"
date: "May 14, 2026"
language: "hi-IN"
locale: "hi_IN"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "कॉर्पोरेट-वित्त और क्रिप्टोग्राफी की प्रतीकात्मक छवि"
keywords: "post-quantum, क्रिप्टो चपलता, कॉर्पोरेट वित्त, ट्रेज़री, NIST, ML-DSA, ML-KEM, HNDL, माइग्रेशन, बैंकिंग"
---

El जोखिम क्वांटम है अतीत का वह curiosidad académica को mandato normativo activo. Con वह hoja का ruta के G7 publicada में enero का 2026, वे calendarios का वह UE, वह Reino Unido और Australia ahora aclarados, और BIS Project Leap जो है demostrado वह viabilidad में एक भुगतान-प्रणाली real, वह cuestión के लिए वे consejos का administración ya नहीं है यदि hay जो migrar, sino यदि वह migración puede completarse antes का जो वह vida útil क्रिप्टोग्राफिक का वे डेटा का आज expire.

---

> **TL;DR.** La preparación पोस्ट-क्वांटम है अतीत में 2026 का hoja का ruta को obligación. Los consejos का administración deben tratar वह migración जैसे एक decisión का gestión का जोखिम sistémicos, anclada में ML-KEM और ML-DSA, desplegada का forma híbrida, और secuenciada के साथ suficiente antelación के लिए preceder को एक CRQC plausible और को वे exigencias normativas अधिक estrictas aplicables.
>
> **मुख्य निष्कर्ष**
>
> - **2026 है वह वर्ष में जो वह postura normativa se है endurecido.** La hoja का ruta का enero के Cyber Expert Group के G7, वह calendario coordinado के Grupo का cooperación NIS का वह UE और वह plan में tres fases के NCSC británico हैं hecho pasar वह conversación का वह sensibilización को वह ejecución. La Australian Signals Directorate va अब भी अधिक lejos को fijar एक fecha límite firme को 2030 के लिए वह क्रिप्टोग्राफी asimétrica clásica.
> - **La exposición है asimétrica.** RSA, ECC और Diffie–Hellman constituyen वह समस्या inmediato: वे algoritmos asimétricos जो sustentan वे handshakes SWIFT, TLS, वे PKI, वह firma का कोड और वह autenticación का वे नेटवर्क का compensación. El cifrado simétrico (AES-256) जारी रखता है siendo estable यदि se mantiene वह longitud का वे कुंजियाँ. La atención के consejo debe centrarse में वह superficie asimétrica.
> - **«Cosechar ahora, descifrar अधिक tarde» नहीं है एक escenario भविष्य.** Adversarios interceptan और almacenan ya आज registros वित्तीय cifrados, registros का liquidación, expedientes का M&A और डेटा का transferencias सीमा-पार, के साथ वह intención explícita का descifrarlos एक vez जो exista एक क्वांटम कंप्यूटर criptográficamente relevante (CRQC). Para डेटा sujetos को एक exigencia का confidencialidad का 10 को 20 वर्ष, यह जोखिम ya se है materializado.
> - **La industria dispone ahora का एक punto का referencia operativo.** [BIS Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), publicado में diciembre का 2025, sustituyó के साथ éxito वे firmas digitales tradicionales द्वारा क्रिप्टोग्राफी पोस्ट-क्वांटम में transferencias का liquidez में producción के माध्यम से TARGET2, और है hecho aflorar वे costes का ingeniería específicos (latencia का सत्यापन, tamaño का paquetes) को वे जो se enfrentará cualquier programa का migración.
> - **La suite NIST है वह ancla विश्व-स्तरीय.** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") और FIPS 204 (ML-DSA) हैं referenciados द्वारा सभी वे jurisdicciones principales, यहाँ तक कि जब वे posiciones nacionales divergen sobre वे conjuntos का parámetros और वे exigencias híbridas. Los consejos deberían विचार करना ML-KEM-768 / ML-DSA-65 जैसे suelo और ML-KEM-1024 / ML-DSA-87 जैसे referencia conservadora के लिए वे डेटा का larga vida útil.
> - **El híbrido है वह única vía creíble.** Ninguna autoridad principal recomienda वह bascula directa. Hacer funcionar clásico और resistente को lo क्वांटम में paralelo है वह esquema का despliegue validado द्वारा वह NCSC, वह ANSSI, वह BSI, और demostrado में Project Leap. Es अधिक pesado जो cualquiera का वे alternativas, परंतु है वह única जो aborda को वह vez वह compatibilidad का आज और वह amenaza का कल.

---

## El वर्ष में जो वह postura normativa se है endurecido

Durante वह mayor parte का वह última दशक, वह क्रिप्टोग्राफी पोस्ट-क्वांटम vivía में एक esquina cómoda का वह hoja का ruta को largo plazo. Los क्वांटम कंप्यूटर थे impresionantes परंतु lejanos; वह matemática क्रिप्टोग्राफिक subyacente को RSA और को वे curvas elípticas se trataba जैसे sustrato estable; और वह conversación sobre वह migración se mantenía में gran medida confinada को grupos का trabajo especializados. Esa posición ya नहीं है sostenible.

En enero का 2026, वह [Cyber Expert Group के G7 publicó उसका declaración अधिक consecuente hasta वह fecha ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement on Advancing को Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector"), copresidida द्वारा वह Tesoro estadounidense और वह Banco का Inglaterra. El documento नहीं है एक विनियमन, परंतु pesa अधिक जो एक orientación clásica: representa वह posición compartida का वे ministerios का Finanzas, बैंक centrales और autoridades का supervisión का वे jurisdicciones के G7, según वह cual वह transición क्रिप्टोग्राफिक है ahora एक cuestión का gestión का जोखिम sistémicos. La hoja का ruta alinea उसका horizonte का planificación के साथ mediados का वह दशक का 2030, animando को वे तंत्र वित्तीय críticos को migrar antes, एक formulación जो, में वह idioma prudente का वे banqueros centrales, señala एक expectativa अधिक जो एक sugerencia.

Dos meses antes, वह BIS Innovation Hub और वह Eurosistema publicaron वे resultados का [Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), एक experimentación técnica जो sustituyó वे firmas digitales tradicionales द्वारा क्रिप्टोग्राफी पोस्ट-क्वांटम में transferencias का liquidez में producción बीच वह Banca d'Italia, वह Banque का France, वह Deutsche Bundesbank, Nexi-Colt और Swift. La निष्कर्ष principal था एक éxito: transferencias firmadas resistentes को lo क्वांटम atravesaron का extremo को extremo एक भुगतान-प्रणाली operativo. El detalle निम्न वह titular है अधिक instructivo, और se examina अधिक adelante में यह artículo.

La combinación का ये dos eventos —एक marco político coordinado के G7 और एक prueba operativa में एक भुगतान-प्रणाली real— है producido lo जो वह समुदाय técnica esperaba desde hace एक दशक: एक respuesta definitiva को वह pregunta «¿है esto real?». La respuesta, में mayo का 2026, है sí. La cuestión जो queda है वह के ritmo.

## Tres vectores का amenaza जो deben preocupar को consejo

Antes का discutir वह mecánica का migración, conviene ser preciso sobre lo जो está concretamente में juego. El जोखिम क्वांटम में बैंकिंग corporativa नहीं है uniforme में todo वह parque क्रिप्टोग्राफिक, और वह atención के consejo se dirige mejor को वे tres vectores जहाँ वह exposición है अधिक aguda.

### 1. Cosechar ahora, descifrar अधिक tarde (HNDL)

La preocupación अधिक inmediata नहीं है futura. Es वर्तमान. Adversarios का nivel estatal और संगठन criminales sofisticadas interceptan और almacenan sistemáticamente वह tráfico वित्तीय cifrado —transferencias, flujos का mensajes SWIFT, comunicaciones M&A, registros का liquidación transfronteriza, contratos का swap और archivos KYC— बिना capacidad actual का leerlos. Su objetivo है simple: almacenar ahora, descifrar अधिक tarde, एक vez जो exista एक CRQC. Como [señaló explícitamente वह Banco का Pagos Internacionales ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), वह recopilación ya está में curso.

Para वे consejos, वह implicación है incómoda परंतु precisa: cualquier dato sensible transmitido आज निम्न cifrado asimétrico clásico, cuya exigencia का confidencialidad se extienda अधिक allá का वह llegada का एक CRQC, ya debe considerarse expuesto. No hay notificación का brecha जब ocurre एक HNDL. No hay alerta SIEM. El cifrado se sostiene —का momento— परंतु वे डेटा ya हैं salido के perímetro.

### 2. Riesgo का sensibilidad को largo plazo

Los डेटा का बैंकिंग corporativa tienen vidas útiles institucionales inusualmente largas. La documentación का M&A estratégica puede जारी रखना siendo sensible को बाज़ार के दौरान एक दशक. Las comunicaciones sobre secretos industriales और वे valoraciones का propiedad intelectual pueden जारी रखना siendo confidenciales के दौरान quince को veinte वर्ष. Los registros का liquidación transfronteriza, वे exposiciones का contrapartes centrales और वे evaluaciones का crédito का contrapartes conservan एक sensibilidad comercial mucho अधिक allá का उसका vida transaccional inmediata.

La [ecuación का Mosca ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), formulada originalmente द्वारा Michele Mosca और ahora integrada में todo marco का migración serio, formaliza वह समस्या. Si **S** है वह vida útil का वे डेटा, **M** है वह tiempo आवश्यक के लिए migrar वे तंत्र जो वे protegen और **Q** है वह tiempo antes का जो एक CRQC esté उपलब्ध, entonces:

```
Si S + M > Q, वे डेटा ya están expuestos.
```

Para डेटा cuyo horizonte का confidencialidad है का veinte वर्ष और एक programa का migración जो आवश्यक है razonablemente cinco को siete वर्ष, वह मूल्य Q implícito sobre वह जो apuesta वह consejo है का को कम 25 वर्ष. Un cuerpo creciente का evaluaciones का expertos —वे [predicciones APAC 2026 का Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), वे encuestas anuales के Global Risk Institute और एक artículo का arquitectura का febrero का 2026 जो propone एक CRQC के साथ unos 100.000 qubits físicos utilizando códigos QLDPC— sugiere जो वह apuesta है imprudente.

### 3. La vulnerabilidad का वे handshakes centrales

El tercer vector है वह अधिक significativo arquitectónicamente. Los cifrados simétricos (AES-256) जारी रखते हैं siendo comparativamente estables; वह algoritmo का Grover divide को वह mitad वह nivel का सुरक्षा efectivo, परंतु duplicar वह longitud का कुंजी restaura वह margen. La exposición catastrófica concierne को वे algoritmos asimétricos, और हैं precisamente वे algoritmos जो sustentan todo handshake autenticado में बैंकिंग corporativa: RSA में वह अवसंरचना का कुंजियाँ públicas SWIFT, ECDSA में वह autenticación cliente/servidor TLS, ECDH में वह establecimiento का कुंजियाँ का sesión, और वे variantes ECC द्वारा सभी partes में वह autenticación móvil के cliente, वे firmas का API और वे cadenas का firma का कोड.

Un CRQC funcional जो ejecute वह algoritmo का Shor नहीं debilita progresivamente वे तंत्र. Los rompe. Una vez जो एक CRQC sea operativo, cualquier handshake protegido द्वारा RSA, cualquier firma ECDSA और cualquier intercambio का कुंजी द्वारा curva elíptica se vuelven recuperables, नहीं después का meses का esfuerzo, sino में cuestión का horas. La transición का «seguro» को «comprometido» है binaria, और se propaga simultáneamente के माध्यम से cada तंत्र जो utilice वह algoritmo afectado. Ese है वह fundamento sobre वह जो descansa वह urgencia normativa.

## Endurecimiento normativo: panorama द्वारा jurisdicción

El panorama normativo विश्व-स्तरीय में mayo का 2026 ya नहीं है एक mosaico का sugerencias. Es एक conjunto coordinado का calendarios जो varían में rigor परंतु convergen hacia वह mismo destino. Un banco multinacional जो opere में वे principales plazas वित्तीय está sometido ahora को वह jurisdicción aplicable अधिक estricta, नहीं को वह अधिक permisiva.

### Estados Unidos

Estados Unidos tiene वह posición अधिक prescriptiva के लिए cualquier institución जो toque तंत्र federales. La [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") का वह NSA impone ML-KEM-1024 और ML-DSA-87 के लिए वे तंत्र का सुरक्षा nacional, debiendo वे नए तंत्र desplegar वह PQC से शुरू होकर enero का 2027 और debiendo completarse वह migración का वह अवसंरचना के लिए 2035. El Memorándum OMB M-23-02 vincula को वे agencias federales को वह misma trayectoria. Para वे बैंक comerciales, वह exposición inmediata pasa द्वारा वे cadenas का compras federales, वे contratos adyacentes को वे NSS, और वह presión indirecta जो वे orientaciones का वह NSA ejercen sobre वह बाज़ार अधिक amplio.

### Unión Europea

La UE opera में tres capas. La [hoja का ruta coordinada का implementación का वह Comisión Europea ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), elaborada द्वारा वह Grupo का cooperación NIS में junio का 2025, fija hitos द्वारा fases में 2026 (estrategias nacionales), 2030 (तंत्र का उच्च जोखिम migrados) और 2035 (transición completa). El Cyber Resilience Act impondrá actualizaciones का सुरक्षा को estado के arte के लिए वे productos digitales से शुरू होकर finales का 2027. NIS2 refuerza वह gestión का जोखिम ICT, यद्यपि कोई नहीं का वे dos directivas contiene एक exigencia PQC explícita. Los reguladores nacionales, द्वारा उसका parte, हैं adelantado को वह Comisión. El BSI alemán impone वह intercambio का कुंजियाँ híbrido और aprueba एक panel conservador का ML-KEM, FrodoKEM और Classic McEliece. La ANSSI francesa exige वह híbrido tanto के लिए वह encapsulación का कुंजियाँ जैसे के लिए वे firmas. La NLNCSA neerlandesa और वे autoridades noruegas se हैं alineado के साथ ML-KEM-1024 जैसे referencia conservadora के लिए वे डेटा का larga vida útil.

### Reino Unido

El NCSC británico publicó उसके orientaciones definitivas में marzo का 2025 और वे reafirmó mediante वह Annual Review 2025. El calendario में tres fases है explícito:

- **Hasta 2028**: identificar वे servicios क्रिप्टोग्राफिक जो आवश्यक हैं actualización, निर्माण करना वह plan का migración और producir एक inventario क्रिप्टोग्राफिक completo.
- **2028 को 2031**: ejecutar वे actualizaciones prioritarias, में particular sobre वे तंत्र críticos और वे प्रोटोकॉल का Internet expuestos.
- **2031 को 2035**: completar वह migración में वह conjunto का तंत्र, servicios और productos.

Para वे वित्तीय संस्थान británicas, वे [orientaciones PQC के CMORG (Cross-Market Operational Resilience Group) ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") se inscriben junto को marco NCSC, tratan को वे बैंक जैसे अवसंरचना nacional गंभीर और ponen वह énfasis में वह disponibilidad का proveedores और वह alineación का वह cadena का suministro.

### Asia-Pacífico

La postura APAC है अधिक fragmentada परंतु evoluciona तेज़. La ASD australiana tiene वह posición अधिक dura को nivel विश्व-स्तरीय: वह क्रिप्टोग्राफी का कुंजी सार्वजनिक clásica ya नहीं debe utilizarse अधिक allá का finales का 2030, बिना recomendación híbrida, और ML-KEM-1024 requerido (ML-KEM-768 aceptable solo hasta 2030). Las संगठन deberían disponer का एक plan का transición afinado के लिए finales का 2026. La Monetary Authority का Singapur है publicado orientaciones formales का preparación क्वांटम. Japón और Corea के Sur invierten sustancialmente, यद्यपि वे dos países disponen का filiales algorítmicas nacionales (Corea है seleccionado NTRU+ और SMAUG-T जैसे KEM, ALMer और HAETAE जैसे firmas). La National Quantum Mission india, dotada का एक asignación gubernamental का 6.003,65 crores का rupias, identifica explícitamente वे servicios बैंकिंग और वित्तीय जैसे prioridad estratégica. Las [predicciones APAC 2026 का Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") evalúan में अधिक के 90 % वह número का उद्यम regionales जो deben invertir में प्रौद्योगिकियाँ postcuánticas यह वर्ष.

### La posición neta

Para एक consejo का administración, वह síntesis práctica का वे posiciones jurisdiccionales है directa. Un banco multinacional नहीं puede gestionar वह calendario का एक solo नियामक; debe gestionar वह अधिक estricto aplicable. Para वह mayoría का वे grandes instituciones, esto significa एक horizonte का planificación का finales का 2030 के लिए वे तंत्र का उच्च जोखिम और finales का 2035 के लिए वह larga cola; वे entidades expuestas को वह ASD apuntando को वह PQC pura के लिए 2030 और वे expuestas को वह CNSA apuntando को वह misma ventana के साथ ML-KEM-1024 और ML-DSA-87 específicamente.

## BIS Project Leap: lo जो वह industria है probado realmente

Project Leap merece वह atención के consejo नहीं क्योंकि sea एक hito का marketing, sino क्योंकि se trata का वह demostración का extremo को extremo अधिक creíble hasta वह fecha का वह क्रिप्टोग्राफी पोस्ट-क्वांटम में एक भुगतान-प्रणाली वित्तीय में producción. La निष्कर्ष principal है directa: funciona. El detalle subyacente है जहाँ residen वे implicaciones operativas.

La Fase 1, completada में 2023, estableció एक VPN resistente को lo क्वांटम बीच वे तंत्र IT का वह Banque का France और वह Deutsche Bundesbank, के साथ mensajes का भुगतान transmitidos बीच París और Fráncfort निम्न एक esquema का cifrado híbrido. La Fase 2, completada को finales का 2025 और [publicada में diciembre ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), था considerablemente अधिक allá. El consorcio sustituyó वे firmas digitales tradicionales basadas में RSA द्वारा firmas postcuánticas में वह ejecución का transferencias का liquidez के माध्यम से TARGET2, वह तंत्र का liquidación bruta में tiempo real के Eurosistema. Los participantes —वह BIS Innovation Hub Eurosystem Centre, वह Banca d'Italia, वह Banque का France, वह Deutsche Bundesbank, Nexi-Colt (जो proporciona वह conectividad TARGET2) और Swift— representan precisamente वे instituciones cuya अवसंरचना tendrá जो migrar eventualmente.

El informe hizo aflorar tres constataciones जो todo programa का migración debería integrar:

- **La latencia का सत्यापन है sensiblemente अधिक elevada.** La सत्यापन का firma पोस्ट-क्वांटम llevó materialmente अधिक tiempo जो वह सत्यापन basada में RSA में वह mismo हार्डवेयर. Para एक तंत्र RTGS diseñado में torno को एक tratamiento का mensajes द्वारा debajo के दूसरा, नहीं है एक observación marginal; है एक dato का planificación का capacidad.
- **Los tamaños का paquete exigen एक refactorización के तंत्र.** Las firmas PQC हैं एक orden का magnitud mayores जो वे equivalentes ECDSA (véase अधिक abajo). Los तंत्र का भुगतान cuyas colas internas, उपकरण का supervisión और esquemas का base का डेटा se हैं dimensionado के लिए mensajes का tamaño heredado नहीं pueden acomodar वह नई carga útil बिना refactorización. Project Leap constató explícitamente जो TARGET2 नहीं podía «acomodar fácilmente» वह मॉडल híbrido बिना reingeniería sustancial.
- **El híbrido है वह respuesta correcta, परंतु अधिक pesado.** Ejecutar clásico और पोस्ट-क्वांटम में paralelo preservó वह retrocompatibilidad और proporcionó defensa में profundidad, परंतु duplicó वह coste के tratamiento क्रिप्टोग्राफिक. Es वह coste operativo का hacer PQC correctamente के दौरान वह transición; नहीं है evitable solo mediante ingeniería astuta.

Para एक director वित्तीय जो examine एक caso का निवेश PQC, वे constataciones का Project Leap हैं útiles precisamente क्योंकि हैं precisas. El coste का वह migración पोस्ट-क्वांटम नहीं है एक sola línea capex. Es एक latencia का सत्यापन जो se propaga में वे contratos SLA, एक expansión के tamaño का mensajes जो afecta को वे presupuestos का almacenamiento और ancho का banda, और एक periodo transitorio का operaciones क्रिप्टोग्राफिक duplicadas जो afecta को वह planificación का capacidad का cálculo. Ninguno का ये puntos है especulativo. Se हैं medido में एक तंत्र का banco central में producción.

## La caja का उपकरण NIST: ML-KEM और ML-DSA comparados

La pieza maestra técnica का todo marco nacional creíble है वह suite NIST का मानक postcuánticos publicada में agosto का 2024. Dos का वे मानक están में वह centro का atención के लिए वह बैंकिंग corporativa: ML-KEM (FIPS 203) के लिए वह encapsulación का कुंजियाँ और ML-DSA (FIPS 204) के लिए वे firmas digitales. Comparten एक fundamento matemático —ambos se apoyan में वह dificultad का वे समस्याएँ Module Learning With Errors (ML-LWE) और Module Short Integer Solution sobre retículos estructurados— परंतु desempeñan papeles muy distintos में वह parque क्रिप्टोग्राफिक, और उसके perfiles का निष्पादन और tamaño difieren materialmente.

### ML-KEM (FIPS 203) — encapsulación का कुंजियाँ

ML-KEM, derivado का [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html), है वह reemplazo का ECDH और का RSA-KEM में वे प्रोटोकॉल में वे जो dos partes deben establecer एक कुंजी simétrica compartida sobre एक canal नहीं seguro. Es, में वह práctica, adonde van वे handshakes TLS tras वह retirada का RSA और का ECDH. NIST define tres conjuntos का parámetros के साथ fuerza का सुरक्षा creciente और निष्पादन decreciente: ML-KEM-512 (NIST Categoría 1), ML-KEM-768 (Categoría 3) और ML-KEM-1024 (Categoría 5).

### ML-DSA (FIPS 204) — firmas digitales

ML-DSA, derivado का CRYSTALS-Dilithium, है वह reemplazo का वे firmas RSA और ECDSA. Soporta वह firma का certificados, वह firma का कोड, वह firma का documentos और वह autenticación. Los tres conjuntos का parámetros हैं ML-DSA-44, ML-DSA-65 और ML-DSA-87, correspondientes में líneas generales को वे NIST Categorías 2, 3 और 5.

### Perfil का tamaño और निष्पादन

Para एक CIO जो dimensione वह capacidad का migración, वे cifras अधिक importantes हैं वे tamaños का artefactos. Son वे entradas के लिए वह planificación का capacidad का नेटवर्क, वे proyecciones का almacenamiento और वे pruebas को nivel का प्रोटोकॉल.

| Algoritmo | Clave सार्वजनिक | Criptograma / Firma | Equivalente clásico अधिक cercano | Tamaño vs clásico |
|---|---|---|---|---|
| ML-KEM-512 | 800 bytes | 768 bytes (criptograma) | ECDH P-256 (~32 bytes कुंजी pub) | ~25× mayor |
| ML-KEM-768 | 1.184 bytes | 1.088 bytes (criptograma) | ECDH P-384 | ~25× mayor |
| ML-KEM-1024 | 1.568 bytes | 1.568 bytes (criptograma) | ECDH P-521 | ~25× mayor |
| ML-DSA-44 | 1.312 bytes | ~2.420 bytes (firma) | ECDSA P-256 (firma 64 bytes) | ~38× mayor |
| ML-DSA-65 | 1.952 bytes | ~3.293 bytes (firma) | ECDSA P-384 | ~50× mayor |
| ML-DSA-87 | 2.592 bytes | ~4.595 bytes (firma) | ECDSA P-521 | ~70× mayor |

*Fuente: síntesis का वे especificaciones [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") और FIPS 204, के साथ डेटा comparativos procedentes का वह literatura का benchmarking independiente.*

Tres implicaciones operativas se derivan directamente का ello. **Primero**, वह tamaño का firma है वह restricción limitante के लिए वह mayoría का despliegues empresariales. Una firma ML-DSA-65 है unas cincuenta veces वह tamaño का एक firma ECDSA P-256, और वे cadenas का certificados TLS जो llevan CA intermedias crecen proporcionalmente. El trabajo का capacidad sobre वह superficie नहीं है opcional, है estructurador. **Segundo**, ML-KEM है competitivo में cálculo के साथ ECDH और, में algunas implementaciones, materialmente अधिक तेज़, में particular में हार्डवेयर जो dispone का soporte vectorial के लिए वह aritmética का retículos subyacente. **Tercero**, वह सत्यापन ML-DSA है constantemente तेज़ (को menudo अधिक तेज़ जो वह सत्यापन ECDSA), परंतु वह firma ML-DSA implica एक bucle का rejection sampling जो puede आवश्यकता होना कई intentos में हार्डवेयर restringido. Para वे servicios का firma का उच्च निष्पादन, है एक benchmark को सत्यापित करना अधिक जो को presumir.

### Elegir वे conjuntos का parámetros

Las posiciones jurisdiccionales sobre वह elección का वे parámetros नहीं हैं idénticas, परंतु वह convergencia है clara. ML-KEM-768 और ML-DSA-65 constituyen वह suelo empresarial —validados द्वारा वह NCSC británico जैसे referencia के लिए वे संगठन británicas और aceptables में वह mayoría का marcos europeos—. ML-KEM-1024 और ML-DSA-87 हैं वह techo conservador —impuestos द्वारा वह CNSA 2.0 का वह NSA के लिए वे तंत्र का सुरक्षा nacional estadounidenses और requeridos द्वारा वह ASD के लिए वे entidades australianas reguladas के लिए 2030—. Para वे डेटा का sensibilidad extremadamente larga —registros का liquidación soberanos, propiedad intelectual के साथ horizonte decenal, registros का custodia के लिए instrumentos का largo vencimiento— वे conjuntos का parámetros superiores हैं वह मूल्य द्वारा defecto defendible.

### Un fundamento matemático compartido, एक जोखिम compartido

Un punto digno का वह atención के consejo: ML-KEM और ML-DSA extraen ambos उसका सुरक्षा का वह misma familia का समस्याएँ sobre retículos. Un avance criptoanalítico भविष्य contra Module-LWE afectaría को वे dos मानक simultáneamente. Es precisamente द्वारा ello द्वारा lo जो कई autoridades nacionales —notablemente वह BSI alemán और वह ANSSI francesa— recomiendan complementar वह pila basada में retículos के साथ firmas basadas में funciones का hash (SLH-DSA, FIPS 205) के लिए वे casos का उपयोग का firma को largo plazo और firma का कोड. La agilidad क्रिप्टोग्राफिक, में यह sentido, नहीं है solo वह capacidad का reemplazar RSA द्वारा ML-KEM. Es वह capacidad का reemplazar एक algoritmo PQC द्वारा otro जब वह panorama criptoanalítico evolucione.

## Un camino का migración lógico: Descubrimiento → Triaje → Despliegue híbrido

Para एक consejo जो apruebe एक programa PQC plurianual, वह cuestión operativa है cómo escalonar वह trabajo बिना asumir एक जोखिम inaceptable का disponibilidad का servicio. El esquema जो है emergido के माध्यम से वह hoja का ruta के G7, वह marco NCSC, BIS Project Leap और वे documentos का orientación nacionales principales converge में tres fases.

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│ 1. DESCUBRIMIENTO &  │ → │ 2. TRIAJE (MOSCA)    │ → │ 3. DESPLIEGUE        │
│    CBOM              │   │ Priorización द्वारा     │   │    HÍBRIDO           │
│ Inventario क्रिप्टो    │   │ जोखिम según vida    │   │ Doble sobre clásico  │
│ में सभी वे तंत्र│   │ útil का वे डेटा    │   │ + PQC, क्रिप्टो-ágil   │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### Fase 1 — Descubrimiento और nomenclatura क्रिप्टोग्राफिक (CBOM)

No se puede planificar वह migración का एक parque क्रिप्टोग्राफिक जो नहीं है sido cartografiado, और वह mayoría का instituciones नहीं disponen का एक mapa exacto. La पहली fase है द्वारा tanto वह producción का एक Cryptographic Bill of Materials —एक inventario estructurado का cada instancia का क्रिप्टोग्राफी asimétrica में वह संगठन, etiquetada cada instancia द्वारा algoritmo, longitud का कुंजी, contexto protocolar, sensibilidad का वे डेटा और propietario के तंत्र—. El escaneo स्वचालित sobre वे bases का कोड, अनुप्रयोग वेब, imágenes का contenedores, configuraciones का bases का डेटा, almacenes का certificados, módulos HSM e interfaces का proveedor है वह mecanismo práctico; वह inventario manual का वे तंत्र heredados और वे प्रोटोकॉल propietarios है वह complemento inevitable.

La salida का वह Fase 1 नहीं है glamurosa, परंतु है वह único fundamento sobre वह जो वे Fases 2 और 3 pueden descansar. Es भी वह entregable जो वह mayoría का funciones का auditoría interna और reguladores externos buscarán primero जब se empiecen को pedir वे atestaciones का cumplimiento PQC.

### Fase 2 — Triaje का जोखिम के साथ वह ecuación का Mosca

Una vez वह CBOM में mano, वह institución puede aplicar वह marco का Mosca activo द्वारा activo. Para cada dependencia क्रिप्टोग्राफिक, वह cuestión है यदि **S + M > Q** —यदि वह vida útil का वे डेटा अधिक वह tiempo का migración supera वह tiempo estimado hasta एक CRQC—. Los activos जहाँ वह desigualdad है अधिक aguda —डेटा sensibles का larga vida útil sobre एक अवसंरचना जो tarda वर्ष में migrar— pasan को frente का वह fila. Los activos के साथ vidas útiles का डेटा cortas या एक अवसंरचना ya modernizada pueden secuenciarse अधिक tarde में वह programa.

Esta है वह fase जहाँ वह apetito का जोखिम के consejo है अधिक visible. El मूल्य Q जो वह institución elige जैसे objetivo का planificación है, में efecto, एक apuesta estratégica sobre वह ritmo का वे progresos के हार्डवेयर क्वांटम. Una Q conservadora (mediados का वह दशक का 2030) produce एक plan का migración अधिक agresivo और एक línea capex को corto plazo अधिक उच्च. Una Q optimista (post-2040) produce एक plan अधिक relajado और एक exposición residual अधिक उच्च को वे डेटा ya cosechados. Ninguna está equivocada; ambas deberían ser decisiones explícitas के consejo, नहीं defectos implícitos का वह función तकनीकी.

### Fase 3 — Despliegue híbrido

Una vez identificados वे activos prioritarios, वह despliegue debería जारी रखना वह esquema híbrido demostrado में Project Leap और validado द्वारा वह NCSC, वह ANSSI, वह BSI और वह hoja का ruta के G7. Un despliegue híbrido hace funcionar एक algoritmo clásico और एक algoritmo पोस्ट-क्वांटम में paralelo, combinando उसके salidas में एक sola envolvente. El compuesto है seguro contra वे ataques clásicos (वह algoritmo clásico se sostiene आज) और contra वे ataques क्वांटम (वह algoritmo PQC se sostiene कल). Concretamente, वह esquema habitual है X25519 combinado के साथ ML-KEM-768 या ML-KEM-1024 के लिए वह encapsulación का कुंजियाँ, और ECDSA combinado के साथ ML-DSA के लिए वे firmas जब वे dobles firmas हैं operacionalmente factibles.

La constatación का Project Leap según वह cual वह híbrido है «mucho, mucho अधिक pesado» जो cualquiera का वे enfoques puros है वह contrapeso honesto को वह recomendación. Los consejos deberían anticipar एक subida का capacidad का cálculo और almacenamiento, handshakes अधिक largos और complejidad adicional का cadenas का certificados के दौरान वह transición. La compensación: वह híbrido elimina वह mayor fuente única का जोखिम का migración: वह bascula abrupta का एक fundamento क्रिप्टोग्राफिक को otro में entorno का producción.

## Cuánto cuesta और द्वारा qué नहीं hacer nada cuesta अधिक

El análisis का Mastercard, [reportado को principios का 2026 ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs"), cifró वह coste विश्व-स्तरीय का वह migración PQC के sector वित्तीय में 28-42 mil millones का dólares. Dentro का वह agregado, वे [investigaciones का RedCompass Labs और CMORG ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") जो जारी रखते हैं वे gastos institucionales reales sugieren जो वे बैंक का पहला nivel comprometen बीच 20 और 30 millones का dólares को वर्ष में programas का preparación, के साथ calendarios का implementación जो cubren कई ciclos का liderazgo. Son cantidades sustanciales. Sin embargo, नहीं है वह comparación pertinente.

La comparación pertinente है वह coste का एक solo evento का descifrado retroactivo. Para एक institución cuyo tráfico का transferencias cosechado, correspondencia M&A या डेटा का exposición को contrapartes se vuelven legibles के लिए एक adversario में 2032, वह coste operativo और reputacional नहीं está acotado द्वारा वह línea capex का migración. Está acotado द्वारा वह मूल्य का वह दशक का जानकारी estratégica subyacente, जो, के लिए cualquier institución sistémica, है materialmente superior को cualquier presupuesto का migración plausible. El encuadre के G7 según वह cual वह transición क्रिप्टोग्राफिक है एक cuestión का gestión का जोखिम sistémicos के बजाय एक actualización तकनीकी है correcto, और वे consejos deberían abordarlo sobre वह base.

Hay एक दूसरी línea का coste जो merece separarse. La migración को वह PQC है एक función का forzamiento के लिए वह agilidad क्रिप्टोग्राफिक: वह capacidad arquitectónica के लिए reemplazar वे algoritmos क्रिप्टोग्राफिक बिना reconstruir वे तंत्र जो dependen का ellos. La mayoría का instituciones नहीं tienen आज agilidad क्रिप्टोग्राफिक; उसके dependencias RSA और ECC están profundamente integradas में वे PKI, वे cadenas का firma का कोड, वे integraciones का proveedores और वे प्रोटोकॉल caseros acumulados को lo largo का वे दशक. La निवेश में agilidad, hecha निम्न वह presión का वह transición PQC, है duradera. Se movilizará का नया जब llegue वह próxima transición क्रिप्टोग्राफिक, ya se trate का एक sucesor का वह PQC basada में retículos, का एक sobrecapa का QKD या का otra cosa जो अब भी नहीं esté में वह hoja का ruta का वे मानक. Tratado correctamente, वह capex का migración PQC है एक निवेश puntual जो reporta opcionalidad recurrente.

## निष्कर्ष

El argumento को favor का tratar वह migración पोस्ट-क्वांटम जैसे एक prioridad का consejo में 2026 नहीं descansa में वह inminencia का एक CRQC. Las estimaciones को respecto जारी रखते हैं siendo realmente inciertas: वह opinión científica creíble sitúa वह probabilidad का एक CRQC के लिए 2028 muy द्वारा debajo के uno द्वारा ciento, ascendiendo को aproximadamente वह cincuenta द्वारा ciento में वह horizonte 2037-2040. El argumento descansa में tres observaciones अधिक जो नहीं हैं inciertas.

Primero, वह HNDL se produce आज, और वे डेटा के साथ एक exigencia का confidencialidad का को कम एक दशक están expuestos independientemente का cuándo llegue वह CRQC. Segundo, वह migración के parque क्रिप्टोग्राफिक का एक gran institución वित्तीय lleva का cinco को siete वर्ष यहाँ तक कि के साथ financiación adecuada और atención का वह dirección, lo जो significa जो वह programa iniciado में 2026 termina hacia 2031, bien dentro के extremo conservador का वह distribución का probabilidad के CRQC. Tercero, वे expectativas normativas se हैं endurecido materialmente में वे últimos doce meses, और वे instituciones cuyas actas का consejo 2026 consignen एक programa PQC claro estarán में एक posición sensiblemente अधिक fuerte जो aquellas cuyas actas solo consignen एक vigilancia atenta.

Las instituciones जो arrancan ahora tienen वह ventaja का वह elección. Pueden secuenciar वह trabajo को lo largo का कई ciclos का liderazgo, integrarlo के साथ iniciativas का resiliencia अधिक amplias और absorber वे costes operativos के despliegue híbrido में एक planificación capitalista normal. Las instituciones जो esperan afrontarán वह mismo trabajo निम्न plazos अधिक ajustados, के साथ कम margen का secuenciación, और sobre एक trasfondo का restricciones का suministro का हार्डवेयर PQC, experiencia और capacidad का proveedores. El coste का actuar pronto है conocido; वह coste का actuar tarde है asimétrico precisamente का वह manera जो वह gestión का जोखिम se diseña के लिए रोकना.

Para poner यह artículo में perspectiva में यह sitio, वह [artículo का abril का 2026 sobre वह compresión का वे umbrales क्वांटम](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") examinaba वह trayectoria material subyacente, वह [análisis का noviembre का 2023 sobre CRYSTALS-Kyber](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in को Quantum Age") cubría वे fundamentos matemáticos ahora estandarizados निम्न ML-KEM, वह [artículo का diciembre का 2023 sobre वह distribución क्वांटम का कुंजियाँ](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") trataba का वह sobrecapa [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) complementaria, और वह [implementación का referencia open source KyberLib](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") proporciona एक implementación Rust operativa का वे primitivas subyacentes के लिए वे instituciones जो deseen inspeccionar directamente वह superficie क्रिप्टोग्राफिक. Implicarse में वह detalle práctico और técnico —नहीं solo में वे titulares normativos— है वह manera में जो वे consejos distinguen एक programa का migración creíble का एक teatro का cumplimiento.

## Preguntas frecuentes

**¿Cuándo existirá realmente एक क्वांटम कंप्यूटर criptográficamente relevante?**

Las estimaciones creíbles varían ampliamente. A principios का 2026, वे demostraciones क्वांटम públicas हैं alcanzado बीच 24 और 28 qubits lógicos, जबकि se estima जो एक CRQC आवश्यक है के आस-पास 6.000 qubits lógicos sustentados द्वारा बीच 100.000 और कई millones का qubits físicos, dependiendo के enfoque का corrección का errores. El consenso experto sitúa वह probabilidad का एक CRQC में कम के uno द्वारा ciento के लिए 2028, में torno को cincuenta द्वारा ciento में वह horizonte 2037-2040, के साथ एक variabilidad significativa बीच previsiones. Las recientes reducciones का वे estimaciones teóricas का recursos —का 20 millones का qubits hace unos वर्ष को कम का एक millón में वे trabajos का Gidney में 2025, और को aproximadamente 100.000 में वह artículo QLDPC का febrero का 2026— हैं comprimido वह horizonte का planificación. Para वे necesidades का एक consejo, वह hipótesis का planificación apropiada है mediados का वह दशक का 2030 के लिए वे तंत्र का उच्च जोखिम, finales का वह दशक का 2030 जैसे punto medio conservador, और antes यदि वह exposición HNDL है वह preocupación limitante.

**¿Por qué एक despliegue híbrido के बजाय पोस्ट-क्वांटम puro?**

Tres razones. Primero, ML-KEM और ML-DSA, यद्यपि seriamente validados, tienen historiales criptoanalíticos अधिक cortos जो RSA और ECC. Un esquema híbrido जारी रखता है siendo seguro यदि cualquiera का वे componentes se sostiene; एक esquema PQC puro queda expuesto यदि वह समस्या sobre retículos se debilita inesperadamente. Segundo, वह híbrido preserva वह retrocompatibilidad के साथ वे contrapartes जो अब भी नहीं हैं migrado, गंभीर में एक transición industrial plurianual. Tercero, toda autoridad principal के बाहर वह Australian Signals Directorate recomienda explícitamente वह híbrido के लिए वह periodo का transición: NCSC, ANSSI, BSI, NLNCSA और वह marco G7 validan सभी वह enfoque का doble envolvente. La compensación, जैसे cuantificó Project Leap, है एक sobrecoste materialmente अधिक उच्च में cálculo और almacenamiento. Es वह precio का वह opcionalidad.

**¿Hace falta को वह vez ML-KEM और ML-DSA, या se puede elegir?**

Ambos. ML-KEM और ML-DSA desempeñan roles क्रिप्टोग्राफिक distintos. ML-KEM reemplaza वे primitivas का establecimiento का कुंजी में TLS, वे VPN, वह autenticación móvil और प्रोटोकॉल similares में वे जो dos partes deben convenir एक कुंजी simétrica compartida. ML-DSA reemplaza वे primitivas का firma डिजिटल में वे certificados PKI, वह firma का कोड, वह firma का documentos, वह mensajería autenticada tipo SWIFT और वे aserciones का identidad. El parque क्रिप्टोग्राफिक का एक institución उपयोग करता है वे dos tipos का primitivas में distintos lugares; वह migración debe cubrir ambos. El tamaño का firma significativamente mayor का ML-DSA (50-70× ECDSA) suele ser वह अधिक exigente का वे dos को nivel operativo; वह trabajo का planificación का नेटवर्क और almacenamiento के लिए ML-DSA domina वह mayoría का evaluaciones का capacidad का migración.

**¿Cómo medir वह avance का एक programa का यह tamaño?**

Tres indicadores हैं prácticos और se alinean के साथ वे principales marcos normativos. **Cobertura का वह CBOM**: qué porcentaje का वे instancias क्रिप्टोग्राफिक asimétricas का वह institución se है inventariado, clasificado और etiquetado के लिए prioridad का migración. **Cobertura का migración का वे activos का उच्च जोखिम**: qué porcentaje का वे activos जहाँ वह condición S + M > Q का Mosca है verdadera है migrado को वह PQC híbrida. **Cobertura का agilidad क्रिप्टोग्राफिक**: qué porcentaje का वे तंत्र के साथ dependencia क्रिप्टोग्राफिक puede reemplazar वे algoritmos बिना cambio का कोड, solo द्वारा configuración. La hoja का ruta G7 CEG, वह marco में tres fases के NCSC और वह hoja का ruta coordinada UE se conectan सभी को ये tres medidas, यहाँ तक कि जब उपयोग करते हैं terminología diferente.

**¿Cuál है वह coste का esperar एक वर्ष अधिक?**

No है nulo, और नहीं है simétrico. Esperar एक वर्ष renuncia को एक वर्ष का protección HNDL sobre वे डेटा का larga vida útil: वे डेटा cuya exigencia का confidencialidad se extiende को 2040 quedan expuestos एक वर्ष अधिक का lo आवश्यक. Comprime वह ventana का migración frente को plazos normativos fijos (ASD 2030, hitos NSA CNSA 2.0, objetivo UE 2030 के लिए वे तंत्र críticos), lo जो se traduce में एक जोखिम का entrega अधिक उच्च और एक flexibilidad का secuenciación reducida. Expone को वह institución को restricciones का suministro का proveedores और talento जो ya हैं visibles में वह बाज़ार और जो se agravarán जब वे mayores actores के sector pasen का वह planificación को वह ejecución. El coste नहीं है catastrófico में एक solo वर्ष, परंतु se compone, और वह entorno normativo converge hacia एक posición में वह जो वे consejos tendrán जो व्याख्या करना वह retraso में lugar के gasto.

## संदर्भ-स्रोत

- Sebastien Rousseau, (2026). [Quantum Thresholds Are Moving Again](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in को Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in को Quantum Age").
- Sebastien Rousseau, (2023). [Quantum Key Distribution Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [KyberLib: A Rust-Powered Shield Against Quantum Threats](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats").
- G7 Cyber Expert Group, (2026). [Advancing को Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement, January 2026"). GOV.UK.
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
- The Asian Banker, (2025). [Building Resilience for को Quantum-Ready Financial System ⧉](https://www.theasianbanker.com/updates-and-articles/building-resilience-for-a-quantum-ready-financial-system "Building resilience for को quantum-ready financial system"). The Asian Banker.
