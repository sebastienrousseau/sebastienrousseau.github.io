---
title: "La scadenza pacs.008 «indirizzo strutturato» di novembre 2026: vista a sei mesi"
subtitle: "A metà novembre 2026 SWIFT CBPR+ rifiuterà gli indirizzi postali non strutturati nei messaggi pacs.008"
description: "A metà novembre 2026 SWIFT CBPR+ rifiuterà gli indirizzi postali non strutturati nei messaggi pacs.008 e nei messaggi di pagamento transfrontaliero associati. Con circa il 65% dei messaggi ancora non conformi e il 44% delle banche in ritardo, la finestra di remediation si chiude più rapidamente di quanto la maggior parte dei programmi di preparazione sia progettata per gestire."
date: "May 12, 2026"
language: "it-IT"
locale: "it_IT"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "Schema di un messaggio di pagamento transfrontaliero con indirizzo strutturato, con TwnNm e Ctry evidenziati"
keywords: "ISO 20022, pacs.008, pacs.009, pacs.004, pacs.003, pain.001, CBPR+, SWIFT, SR2026, indirizzo strutturato, SEPA, EPC, pagamenti transfrontalieri, screening sanzioni, pacs008"
---

A partir di mediados di noviembre di 2026, SWIFT CBPR+ rechazará le indirizzi postali non strutturate in i messaggi pacs.008 e messaggi di pagamento transfronterizos asociados. Con vicino del 65 % dei messaggi ancora non conformes e il 44 % dei bancos atrasados, la ventana di remediación se cierra più rápido di lo che la maggior parte di i programas di preparación sono progettati per gestire.

---

> **TL;DR.** La regola SR2026 obbliga a strutturare almeno nome città e paese in pacs.008, pacs.009, pacs.004 e pacs.003 da metà novembre 2026. La preparazione del settore è disomogenea e la finestra di remediation si chiude rapidamente; le pipeline automatizzate di validazione sono oggi la leva pratica chiave.
>
> **Punti chiave**
>
> - Da **novembre 2026** SWIFT CBPR+ smetterà di accettare indirizzi postali non strutturati nei messaggi di pagamento transfrontaliero. Il cambio si applica a **pacs.008**, **pacs.009**, **pacs.004** e **pacs.003**, oltre ai flussi **pain.001** a monte.
> - Come minimo, **nome città (TwnNm)** e **paese (Ctry)** devono essere presenti in campi strutturati dedicati. **Nome via (StrtNm)** e **numero civico (BldgNb)** o **casella postale (PstBx)** sono fortemente raccomandati.
> - Il cambio migliora la precisione dello screening sanzioni, riduce le riparazioni manuali e protegge lo straight-through processing, ma solo per le istituzioni che hanno bonificato i dati cliente a monte.
> - La preparazione di settore è disomogenea: a marzo 2026 circa il **65%** dei messaggi CBPR+ porta ancora indirizzi non strutturati, il **44%** delle banche è in ritardo e il **32%** dei record cliente è ancora non strutturato in media.
> - Strumenti open source come **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, libreria Python e servizio FastAPI per generare, validare e orchestrare i flussi pacs.008, possono comprimere i tempi di remediation automatizzando validazione schema, controlli di qualità dell'indirizzo e applicazione a livello CI.

---

## Un scadenza che sempre estuvo in percorso

La exigencia di indirizzo strutturato di noviembre di 2026 non è un golpe normativo repentino. Figura in la roadmap SWIFT CBPR+ da il anuncio inicial della migración [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html), e rimane al fine di la cohabitación MT/MX di noviembre di 2025. Lo che ha cambiado in 2026 è la proximidad. Con vicino di seis meses restantes, il settore opera già all'interno di la ventana in la che i problemas di qualità dei dati non resueltos diventan in un rischio operativo.

Le cifras cuentan la historia con claridad. La actualización comunitaria di SWIFT di marzo di 2026 señala che [alrededor del 65 % dei messaggi di pagamento ancora contengono indirizzi non strutturate ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), e che la adopción rimane siendo desigual tra geografías e tipos di istituzioni. Una [encuesta di RedCompass Labs di marzo di 2026 tra 308 profesionales sénior di pagamenti ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022") constató che il 44 % dei bancos non sono actualmente per buen percorso per soddisfare il scadenza di indirizzo strutturato, nonostante haber gastado di media 20 millones di dólares —e in le mayores istituzioni più di 30 millones— in la preparación 2026, con una media di 13 colaboradores adicionales asignados ai programas ISO 20022. La stessa encuesta constató che il 32 % dei registri di indirizzo di cliente rimangono siendo non strutturati di media, e che il 60 % dei bancos señalan carencias in i sistemi core banking nel momento di soportar i campos di indirizzo strutturato.

Non è, pertanto, un problema che pueda resolverse con un mes più di trabajo su il motor di messaggi. È un problema di qualità dei dati che asciende da la capa di messaggio verso i sistemi di onboarding, i processi KYC, i canales corporativos e décadas di dati master di cliente in texto libre acumulados.

## Lo che la regola exige realmente

Sotto la SWIFT CBPR+ Standards Release 2026 (SR2026), la exigencia chiave è simple in principio e implacable in il dettaglio. A partir di mediados di noviembre di 2026, [il nombre della ciudad e il país devono proporcionarse in i suoi campos strutturati dedicados ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed") per tutti i agentes e partes in i messaggi di pagamento CBPR+, con excepciones molto limitadas (extractos e notificaciones in camt.052, camt.053, camt.054, più alcuni messaggi administrativos rimangono al di fuori di la exigencia estricta). Per i agentes, il uso continuado del BIC da solo rimane siendo una alternativa válida a name-and-address.

Dos formatos di indirizzo rimangono autorizados dopo il cambiamento:

- **Totalmente strutturato**: ogni componente della indirizzo postale se mapea a il suo elemento ISO 20022 dedicado: StrtNm (nombre di calle), BldgNb (número di edificio) o BldgNm (nombre di edificio), PstCd (código postal), TwnNm (nombre di ciudad), CtrySubDvsn (subdivisión país), Ctry (país, in código ISO 3166-1 alpha-2). È il formato che SWIFT identifica explícitamente come la opción più deseable quando è posible.
- **Híbrido**: il nombre di ciudad e il país se rellenan in i suoi campos strutturati, mentre che il resto di la indirizzo può utilizzare fino a dos elementos AdrLine non strutturati. Importante: [i elementos strutturati non devono repetirse all'interno di le líneas non strutturate ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); per un componente dado, la indirizzo è uno o altro.

Le indirizzi totalmente non strutturate —dove la indirizzo completa se encuentra in elementos AdrLine senza TwnNm ni Ctry— non se aceptarán per nessuno dei campos di parte afectados. Il European Payments Council ha alineado il suo rulebook SEPA con il stesso cambiamento, per lo che [a partire dal 15 di noviembre di 2026 il formato non strutturato anche rimane prohibido in SCT, SDD e SCT Inst ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). La alineación è deliberada: SWIFT e il EPC hanno progettato un fin di semana único di bascula industrial.

Per despejar qualsiasi ambigüedad, la [documentación di pacs008 enumera direttamente i messaggi afectados ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (deudor e acreedor in le transferencias cliente), pacs.009 (indirizzi di istituzione in le transferencias FI e i pagamenti di cobertura), pacs.004 (indirizzi di parte in le devoluciones) e pacs.003 (adeudos directos). La exigencia asciende anche aguas arriba: i file pain.001 corporativos che lleven indirizzi non strutturate bloquearán la generación conforme di pacs.008 in il banco receptor.

## Perché il settore lo ha convertido in una prioridad

Il argumento a favor delle indirizzi strutturati non è estético. È operativo, e se manifiesta in tres lugares.

**Cribado di sanciones.** Il beneficio pratico più importante è che le indirizzi strutturati consentono ai sistemi di cribado separar il nombre di parte dei dati di localización. I blocchi di indirizzo in texto libre causan regularmente falsos positivos quando un nombre di ciudad solapa con un token di nombre di persona sancionada, o quando un país enterrado in il texto libre se pasa totalmente per alto. I campos strutturati consentono ai motores di cribado applicare regole di rischio específicas di país in modo determinista, e hacen posible la applicazione del matching di lista di sanciones contra il código di país invece di adivinar su una catena parseada. Il análisis di CGI UK pubblicato in marzo di 2026 subraya questo punto explícitamente: [i dati di indirizzo strutturati se tornano centrales per la resiliencia operativa, e non simplemente una obligación di conformità ⧉](https://www.cgi.com/uk/in-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Tasas di reparación manual.** I pagamenti transfrontalieri actuales portano un costo operativo significativo in forma di ricerche manuales, gestión di excepciones e colas di reparación, in gran parte motivado per indirizzi che i sistemi di cribado o di enrutamiento non possono parsear con confianza. I bancos che già hanno pasado alle indirizzi strutturati reportan reducciones materiales di excepciones STP, in particolare in i flujos di mitad di corredor dove i agentes intermediarios prima dovevano interpretar dati in texto libre che non avevano generato.

**Aplicación a livello di rete.** SR2026 endurece la validación a livello di la rete SWIFT. Algunos dei nuovi controles operarán inicialmente in modo non bloqueante —señalando problemas di qualità dei dati senza detener i pagamenti— ma la trayectoria è chiara, e dopo il cambiamento, [i messaggi non conformes saranno rechazados in modo pura e simple ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Varios rails di pagamento estadounidenses (Fedwire, CHIPS) e SWIFT CBPR+ convergen esencialmente in il stesso calendario, lo che elimina la opción di un cambiamento escalonado che alcune istituzioni avevano supuesto in planes anteriores.

## La vista per campo: lo che cambia in il messaggio

Il messaggio pacs.008 admite indirizzi strutturati da che le primeras directrices di uso CBPR+ entraron in vigor in marzo di 2023. Lo che cambia in noviembre di 2026 non è il esquema, è la validación. Fino a ora, i bancos hanno podido poblar i elementos AdrLine con texto libre e hacerlo passare per la rete. A partir del scadenza, i contenuti dei blocchi di parte devono satisfacer i requisitos mínimos di campos strutturati.

### Requerido, recomendado e retirado

| Elemento | XPath (sotto `PstlAdr`) | Estado dopo nov. 2026 | Notas |
|---|---|---|---|
| Nombre di ciudad | `<TwnNm>` | **Obligatorio** | Al meno un nombre di ciudad strutturato per parte afectada |
| País | `<Ctry>` | **Obligatorio** | Código ISO 3166-1 alpha-2 |
| Nombre di calle | `<StrtNm>` | Altamente recomendado | Requerido per il formato totalmente strutturato |
| Número di edificio | `<BldgNb>` | Recomendado | O BldgNb, o PstBx, non ambos |
| Apartado di correos | `<PstBx>` | Recomendado | Alternativa a BldgNb |
| Código postal | `<PstCd>` | Recomendado | Requerido per alcuni esquemas locali |
| Subdivisión país | `<CtrySubDvsn>` | Opcional | Estado, región, provincia |
| Línea di indirizzo (texto libre) | `<AdrLine>` | **Restringido** | Máx. 2 líneas in híbrido; mai accanto al stesso componente in i campos strutturati |
| Tipo di indirizzo | `<AdrTp>` | Opcional | Uso di `ADDR` recomendado per le indirizzi postali |

*Fuente: síntesis delle directrices di uso SWIFT CBPR+ per SR2026 e della [documentación di indirizzo strutturato pacs008.com ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008").*

La implicación pratica è che tutta istituzione che ancora se apoye in AdrLine in solitario —già sea in il suo propia generación di messaggio, in i file pain.001 recibidos di clienti corporativos, o in i registri di dati master utilizzati per enriquecer i pagamenti in flujo— deve migrar quelli dati ai campos strutturati prima del cambiamento. Il servizio di traducción in vuelo di SWIFT può ayudar in tránsito, ma [sufre recargos a partire da enero di 2026 ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB") e non può parsear in modo fiable tutti i formatos di indirizzo. SWIFT anche ha pubblicato [un modello di IA di open source di estructuración di indirizzo ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model") entrenado con dati di più di 200 países per inferir ciudad e país a partire da dati heredados non strutturati con puntuaciones di confianza, ma è explícitamente una ayuda alla remediación, non un sustituto a lungo termine dei dati limpios aguas arriba.

## Come pacs008.com ayuda a comprimir il calendario

Per le istituzioni che necessitano industrializar i suoi pipelines di qualità di indirizzo e validación di messaggi rapidamente, [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") fornisce una toolkit di open source sotto licencia MIT e un servizio FastAPI progettati específicamente per il workflow di bonifico cliente FI a FI. Aborda le tres capas in le che i programas di remediación se estancan con più frecuencia: validación di dati, generación XML e applicazione per pipeline.

Le capacità di indirizzo strutturato della toolkit sono alineadas ai requisitos SR2026:

- **Validación pregeneración** dei campos di indirizzo postale strutturati e híbridos, affinché i dati non conformes sean interceptados prima di che se produzca o envíe XML qualcuno.
- **Marcado dei dati di indirizzo non strutturati** che fallarían dopo il scadenza di noviembre di 2026, con una distinción chiara tra casos aceptables in híbrido e casos totalmente non strutturati.
- **Soporte doble formato** per i formatos híbridos preplazo e le configuraciones totalmente strutturate posplazo, permitiendo alle istituzioni migrar progresivamente senza romper la interoperabilidad con le contrapartes che ancora non hanno completato i suoi propias transiciones.
- **Integración in pipeline CI** affinché i controles di qualità di indirizzo formen parte del processo di build, e non un afterthought alla fine dil flujo: la respuesta pratica alla observación di CGI según la quale [la gobernanza dei dati deve essere un principio di diseño fundamental ⧉](https://www.cgi.com/uk/in-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement") invece di una sobrecapa di conformità.

Más allá delle indirizzi, la toolkit copre la superficie più amplia di validación che la versión SR2026 endurece: validación JSON Schema contra 20 esquemas específicos di messaggio, verificación in modoto IBAN e checksum in 75 países, validación XSD del XML generato contra i schemi ufficiali ISO 20022, e generación version-aware attraversol conjunto delle 13 revisiones di pacs.008 soportadas (pacs.008.001.01 a pacs.008.001.13). Per i team operativos e di conformità, include anche la prevención di XXE mediante defusedxml, la protección estricta contra il path traversal e il enmascaramiento di PII in i registri JSON strutturati per soportar le exigencias di RGPD e PCI DSS, il tipo di controles non negociables in i flujos di pagamento in produzione ma spesso añadidos tardíamente in le migraciones lideradas per proveedor.

La libreria è disponible [in PyPI ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") in forma di paquete `pip install pacs008` e in [GitHub ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") con transparencia total del código fuente. Per le istituzioni che evalúan i suoi opciones, esto importa: le strumenti di open source consentono ai team internos auditar la lógica di validación, integrarla in bases Python o FastAPI existentes senza negociaciones di licencia, e aportar parches man mano che aparezcan i suoi propios casos límite.

Vale la pena essere preciso su il alcance. pacs008 è una toolkit di capa di messaggio; non reemplaza un motore di pagamento, un sistema di cribado o la remediación dei dati master di cliente che una istituzione ancora deve fare in la fuente. Lo che hace è tomar quello trabajo di remediación e hacerlo aplicable: convertir il conformità di indirizzo strutturato di una revisión manual alla fine di una catena larga in una puerta automatizada in il punto di generación. Per i programas con poco tiempo, quella puerta marca la differenza tra un cambiamento limpio e una ola di rechazos poscambio.

## Il panorama delle strumenti

pacs008 se inscribe in un ecosistema più amplio di strumenti di messaggi ISO 20022, e la elección del approccio depende del stack, la escala e la filosofía di migración della istituzione. Il paisaje open source e commerciale include [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (amplia libreria Python multicategoría con validación in beta), la libreria asociada [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") per la iniciación di pagamenti aguas arriba, [Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (una libreria Java exhaustiva Apache 2.0 con una capa commerciale per la validación e le traducciones CBPR+), e una serie di piattaforme commerciali —Mambu, Kyriba, PaymentComponents e altre— che empaquetan la capacità ISO 20022 in offerte più amplias di tesorería o di piattaforma di pagamenti.

Il compromiso è familiar. Le piattaforme commerciali reducen la carga di ingeniería interna ma atan alla istituzione a una roadmap di proveedor che può non corresponder alla suya. Le librerie multicategoría exhaustivas coprono una superficie più amplia ma exigen più trabajo di integración per un tipo di messaggio dado. Le librerie di open source focalizadas —pacs008 per la bonifico cliente FI a FI, [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) per la iniciación di pagamenti— minimizan il tiempo di integración per le istituzioni che necessitano abordar rapidamente cuellos di botella específicos, e dejan alla istituzione dueña di i suoi propias regole di validación. Per il problema di indirizzo strutturato in particolare, un approccio focalizado ha la vantaggio di che le regole applicate sono estrechas, bene definidas e poco susceptibles di cambiar prima del cambiamento.

## Lo che esto significa per settore

Il scadenza di noviembre di 2026 non riguarda a tutte le istituzioni per igual. La respuesta correcta depende del volumen di tráfico transfronterizo, della madurez del dominio di dati existente e del papel che desempeña la istituzione in la catena di pagamento.

### Grandes bancos corresponsales e transfronterizos

Per i banche di primo livello che operano un tráfico CBPR+ significativo, la exigencia di indirizzo strutturato è un workstream all'interno di un programa di preparación SR2026 molto più amplio che anche copre excepciones e ricerche, endurecimiento BAH e (in Estados Unidos) la migración simultánea di Fedwire e CHIPS. I dati di RedCompass Labs sugieren che la maggior parte di queste istituzioni gastan tra 20 e 30 millones di dólares in la preparación 2026, con team di entrega di 10 a 20 especialistas. Il rischio per questo grupo non è la capacità tecnica, è la capacità di entrega. Con diversi workstreams paralelos disputándose le stesse ventanas di release, la remediación di qualità di indirizzo può deslizarse silenciosamente per detrás di workstreams più visibles fino a convertirse in un problema di semana di cambiamento. Il paliativo pratico è subir la validación di indirizzo più arriba in il pipeline, affinché i fallos emerjan in entornos di desarrollo e prueba meses prima di haber alcanzado la produzione.

### Bancos di medie dimensioni e istituzioni di pagamento

Per i bancos di medie dimensioni e le istituzioni EMI/PI, la exigencia di indirizzo strutturato è spesso la obligación 2026 più material che afrontan, perché non portano la stessa carga di workstreams concomitantes che i banche di primo livello. Il sfida aquí è habitualmente la qualità dei dati aguas arriba. I processi di onboarding di cliente che hanno capturado indirizzi in texto libre durante décadas producen dominios di dati master che non sono inmediatamente parseables. La remediación automatizada —utilizando il modello di estructuración di indirizzo open source di SWIFT, servizi commerciali di limpieza di indirizzo o una combinación— può abordar una parte sustancial dei registri, ma una larga cola residual di indirizzi internazionali complejas requerirá una revisión manual. Cuanto prima empiece quello trabajo, più pequeña se torna quella cola.

### Corporativos e proveedores di servizi di pagamento

I corporativos che avviano pagamenti vía pain.001 sono aguas arriba della generación di pacs.008 per il banco ma non sono exentos della exigencia di indirizzo strutturato. I bancos non rellenarán retroactivamente le indirizzi di beneficiario in nombre dei clienti corporativos; i dati strutturati devono provenir dei sistemi propios del corporativo. Per i tesoreros di azienda, esto significa asegurar che i sistemi ERP e di tesorería capturen le indirizzi di beneficiario in forma strutturata, che la informazione di signatario e deudor último anche esté strutturata, e che le plantillas di iniciación di pagamento non abandonen silenciosamente campos al generare il file. La validación previa al vuelo dei file pain.001 —utilizando bene le strumenti propias del corporativo, bene servizi expuestos per il banco— diventa in il punto di control pratico.

### Proveedores, fintechs e integradores

Per i proveedores che construyen su i rails di pagamento, il scadenza è una función di forzamiento per la capacità ISO 20022 che potrebbe haberse aplazado a fases posteriores. Le fintechs che enrutan o avviano pagamenti transfrontalieri attraverso socios bancari devono subir la captura di indirizzo strutturato a i suoi propias UI e API, o accettare che i file pain.001 conformes non puedan producirse a partire da i suoi dati. La oportunidad, per i proveedores capaces di moverse rápido, è absorber la carga di remediación in nombre dei clienti corporativos: transformar un problema di conformità in servizio.

## Conclusione

Il scadenza di indirizzo strutturato di noviembre di 2026 è, in cierto sentido, un cambiamento estrecho: dos campos obligatorios, alcuni recomendados, e la retirada di una opción in texto libre che mai dovrebbe haberviene utilizzatodo per dati relevantes per il screening delle sanzioni in primer lugar. In altro sentido, è il hito ISO 20022 più significativo operacionalmente da la migración CBPR+ original, perché fuerza il dato strutturato non solo in la capa di messaggio sino in i sistemi aguas arriba che la alimentan.

Il cuadro di preparación a livello di settore, a seis meses del scadenza, non è alentador. Dos tercios dei messaggi CBPR+ rimangono llevando indirizzi non strutturate. Casi la mitad dei bancos non van per buen percorso. Cerca di un tercio dei registri di indirizzo di cliente rimangono siendo non parseables. La financiación è in il suo sitio —le encuestas mostrano constantemente inversiones di ocho e nueve cifras— ma il trabajo non, e la dimensión di qualità dei dati del problema non può resolverse solo con gasto in i últimos meses.

Lo che ayuda ora è la automatización in il punto di validación: empujar le regole a pipelines che intercepten i problemas prima di che alcancen la rete, invece di dopo. Per le istituzioni che operano bases Python o FastAPI, le strumenti open source come [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") forniscono una manera pratica di operar quello cambiamento senza ciclo di selección di proveedor. Per tutti gli altri, independientemente del stack, il punto estratégico è il stesso: le istituzioni che industrialicen il cambiamento ora saranno in una posición molto più fuerte che le che se apoyen in un conformità di última hora, per tomar prestada la formulación delle ricerche di RedCompass Labs che ha enmarcado gran parte di la conversación 2026.

Il fin di semana di cambiamento in noviembre cerrará un capítulo. Le istituzioni che lleguen a él con dati limpios, validación automatizada e comprensión operativa di lo che le indirizzi strutturati hacen realmente per il screening delle sanzioni pasarán quello fin di semana vigilando il tráfico. Le che lleguen senza quelle cosas lo pasarán al teléfono.

## Domande frequenti

**Qué cambia exactamente il scadenza di noviembre di 2026?**

A partir di mediados di noviembre di 2026, SWIFT CBPR+ rechazará i messaggi pacs.008, pacs.009, pacs.004 e pacs.003 cuyos campos di parte contengan únicamente indirizzi postali non strutturate. La exigencia strutturata mínima è il nombre di ciudad in il elemento TwnNm e il país in il elemento Ctry (utilizando il código ISO 3166-1 alpha-2). Le indirizzi híbridas rimangono permitidas —ciudad e país in campos strutturati, più fino a dos elementos AdrLine in texto libre per i componentes restantes— ma il stesso componente non può figurar allo stesso tempo in i campos strutturati e non strutturati. Le indirizzi totalmente strutturate sono il formato preferido. Il European Payments Council ha alineado i esquemas SEPA (SCT, SDD, SCT Inst) con la stessa fecha di cambiamento.

**Qué messaggi e che cosa campos di parte sono afectados?**

Per pacs.008, la exigencia se applica alle indirizzi postali del deudor e del acreedor. Per pacs.009, se applica alle indirizzi di istituzione in le transferencias FI e i pagamenti di cobertura. Per pacs.004, se applica alle indirizzi di parte in le devoluciones di pagamento. Per pacs.003, se applica alle indirizzi di acreedor e deudor in i adeudos directos di clienti. I messaggi di extracto e notificación (camt.052, camt.053, camt.054) e alcuni messaggi administrativos rimangono al di fuori di la exigencia estricta. I messaggi pain.001 aguas arriba dei clienti corporativos non se rigen direttamente per CBPR+, ma le indirizzi non strutturate in i file pain.001 bloquearán la generación conforme di pacs.008 aguas abajo e sono, pertanto, efectivamente in il alcance.

**Quale è la differenza tra indirizzo strutturato, híbrida e non strutturata?**

Una indirizzo totalmente strutturata mapea ogni componente a il suo elemento ISO 20022 dedicado: StrtNm, BldgNb o PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. Una indirizzo híbrida ha il nombre di ciudad e il país in campos strutturati, il resto di la indirizzo in fino a dos elementos AdrLine in texto libre; il stesso componente non deve figurar in i dos. Una indirizzo non strutturata ha la indirizzo postale entera in elementos AdrLine senza TwnNm ni Ctry strutturati; è il formato retirado in noviembre di 2026 per i campos di parte afectados.

**Come ayuda pacs008.com in questa transición?**

La libreria [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") valida i campos di indirizzo postale strutturati e híbridos prima della generación XML, marca i dati non strutturati che fallarían dopo il scadenza, soporta i formatos híbridos preplazo e totalmente strutturati posplazo, e se integra in i pipelines CI e workflows di validación per lote. Genera XML per le 13 versiones di pacs.008 soportadas, valida contra i esquemas XSD oficiales ISO 20022, e expone un servizio FastAPI per la orquestación automatizada. È open source sotto licencia di tipo MIT, è disponible in PyPI e è stato progettato específicamente per i workflows di bonifico cliente FI a FI; le regole di validación sono, pertanto, calibradas su le directrices di uso SWIFT CBPR+ SR2026 invece di abstraídas su numerosos tipos di messaggi.

**Qué ocurre se il mio istituzione non è lista in noviembre di 2026?**

I messaggi con indirizzi non strutturate in i campos di parte afectados saranno rechazados a livello di rete dopo il cambiamento. In la pratica, esto se traduce in fallos di pagamento, volúmenes di excepción mayores, oleadas di reparación manual e impacto probable in il cliente. Il servizio di traducción in vuelo di SWIFT è disponible per alcuni casos transitorios ma sufre recargos a partire da enero di 2026 e non può parsear in modo fiable tutti i formatos di indirizzo. SWIFT anche ha pubblicato un modello di IA di open source di estructuración di indirizzo che infiere ciudad e país a partire da dati heredados non strutturati, ma è progettato per la remediación e il preprocesamiento, non come sustituto permanente dei dati limpios aguas arriba. Le istituzioni che lleguen al scadenza senza un dominio di dati master remediado e un pipeline di validación automatizado dovrebbero esperar una semana di cambiamento difícil e una subida operativa significativa in i meses seguenti.

## Riferimenti

- Sebastien Rousseau, (2023). [Automating ISO 20022-Compliant Payment File Creation with Pain001](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html "Automating ISO 20022-Compliant Payment File Creation with Pain001").
- pacs008, (2026). [November 2026 structured-address deadline ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"). pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 Toolkit and API ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"). pacs008.com.
- SWIFT, (2026). [ISO 20022 milestone for November 2026: Unstructured addresses to be removed ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"). SWIFT.
- SWIFT, (2026). [ISO 20022 for Financial Institutions ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions "ISO 20022 for Financial Institutions"). SWIFT.
- SWIFT, (2026). [The Swift AI address structuring model ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"). SWIFT.
- RedCompass Labs, (2026). [Nearly Half of Banks Are Behind on ISO 20022 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022"). Financial IT.
- RedCompass Labs, (2026). [ISO 20022 is arriving all at once for US banks ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). RedCompass Labs.
- ClearingPost, (2026). [The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline"). ClearingPost.
- CGI UK, (2026). [2026: A defining year for ISO 20022 and structured data enforcement ⧉](https://www.cgi.com/uk/in-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"). CGI UK.
- J.P. Morgan, (2026). [ISO 20022 Migration: Guidance, Messaging & More ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration "ISO 20022 Migration: Guidance, Messaging & More"). J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/in/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022 "FAQ Swift ISO 20022 — ING"). ING Wholesale Banking.
- Mambu, (2026). [CBPR+ is live: what ISO 20022 means in practice ⧉](https://mambu.com/in/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice "CBPR+ is live: what ISO 20022 means in practice"). Mambu.
- Kyriba, (2026). [ISO 20022 migration: what every treasury team needs to know about what's next ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/ "ISO 20022 migration: what every treasury team needs to know about what's next"). Kyriba.
- Standard Chartered, (2025). [ISO 20022 – Standard Chartered Address Guidelines (H2H and API) ⧉](https://www.sc.com/in/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf "Standard Chartered ISO 20022 Address Guidelines"). Standard Chartered.
- State Street, (2025). [Client Guide to ISO 20022 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"). State Street.
- ISO 20022, (2026). [Message Definitions Catalogue ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 Message Definitions"). ISO 20022.
