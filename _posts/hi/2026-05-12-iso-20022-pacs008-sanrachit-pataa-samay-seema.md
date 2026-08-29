---
title: "ISO 20022 pacs.008: संरचित-पता समय-सीमा"
subtitle: "नवंबर 2026 की समय-सीमा से पहले बैंकों को क्या करना चाहिए"
description: "ISO 20022 pacs.008 संरचित-पते की समय-सीमा से पहले बैंकों के लिए एक व्यावहारिक रोडमैप।"
date: "May 12, 2026"
language: "hi-IN"
locale: "hi_IN"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "ISO 20022 संदेश-प्रवाह की प्रतीकात्मक छवि"
keywords: "ISO 20022, pacs.008, संरचित पता, SWIFT, CBPR+, समय सीमा, बैंकिंग, भुगतान, माइग्रेशन, अनुपालन"
---

A partir का mediados का noviembre का 2026, SWIFT CBPR+ rechazará वे direcciones postales नहीं estructuradas में वे mensajes pacs.008 और mensajes का भुगतान सीमा-पार asociados. Con cerca के 65 % का वे mensajes अब भी नहीं conformes और वह 44 % का वे बैंक atrasados, वह ventana का remediación se cierra अधिक तेज़ का lo जो वह mayoría का वे programas का preparación están diseñados के लिए gestionar.

---

> **TL;DR.** La regla SR2026 obliga को estructurar को कम वह nombre का वह ciudad और वह país में pacs.008, pacs.009, pacs.004 और pacs.003 desde mediados का noviembre का 2026. La preparación के sector है desigual और वह ventana का remediación se cierra rápidamente; वे pipelines automatizados का मान्यकरण हैं आज वह palanca práctica कुंजी.
>
> **मुख्य निष्कर्ष**
>
> - A partir का **noviembre का 2026**, SWIFT CBPR+ dejará का aceptar direcciones postales नहीं estructuradas में वे mensajes का भुगतान सीमा-पार. El cambio se aplica को **pacs.008** (transferencia cliente), **pacs.009** (transferencia interbancaria), **pacs.004** (devoluciones) और **pacs.003** (adeudos directos), así जैसे को वे flujos **pain.001** aguas arriba जो वे alimentan.
> - Como mínimo, वह **nombre का वह ciudad (TwnNm)** और वह **país (Ctry)** deben estar presentes में campos estructurados dedicados. El **nombre का वह calle (StrtNm)** और bien वह **número का edificio (BldgNb)**, bien वह **apartado का correos (PstBx)**, हैं altamente recomendados. Las líneas का dirección में texto libre (AdrLine) द्वारा sí solas ya नहीं satisfarán वह exigencia के लिए वे campos का partes कुंजी.
> - El cambio mejora वह precisión के cribado का sanciones, reduce वे tasas का reparación manual और protege वह straight-through processing, परंतु solo के लिए वे instituciones जो हैं remediado उसके डेटा का cliente aguas arriba, नहीं solo उसके motores का mensajes.
> - La preparación industrial है desigual. En marzo का 2026, alrededor के **65 % का वे mensajes CBPR+ जारी रखते हैं llevando direcciones नहीं estructuradas**, वह **44 % का वे बैंक** नहीं van द्वारा buen camino के लिए वह plazo, और वह **32 % का वे registros का dirección का cliente** जारी रखते हैं siendo नहीं estructurados का media.
> - Herramientas का ओपन-सोर्स, incluida **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, एक biblioteca Python और एक servicio FastAPI के लिए generar, मान्य करना और orquestar वे flujos का mensajes pacs.008, pueden comprimir वे plazos का remediación automatizando वह मान्यकरण का esquema, वे controles का calidad का dirección और वह अनुप्रयोग में वह nivel CI antes का जो वे mensajes alcancen वह नेटवर्क SWIFT.

---

## Un plazo जो siempre estuvo में camino

La exigencia का dirección estructurada का noviembre का 2026 नहीं है एक golpe normativo repentino. Figura में वह hoja का ruta SWIFT CBPR+ desde वह anuncio प्रारंभिक का वह migración [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html), और जारी रखता है को fin का वह cohabitación MT/MX का noviembre का 2025. Lo जो है cambiado में 2026 है वह proximidad. Con cerca का seis meses restantes, वह sector opera ya के भीतर वह ventana में वह जो वे समस्याएँ का calidad का डेटा नहीं resueltos se convierten में एक जोखिम operativo.

Las cifras cuentan वह historia के साथ claridad. La actualización comunitaria का SWIFT का marzo का 2026 señala जो [alrededor के 65 % का वे mensajes का भुगतान todavía contienen direcciones नहीं estructuradas ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), और जो वह adopción जारी रखता है siendo desigual बीच geografías और tipos का instituciones. Una [encuesta का RedCompass Labs का marzo का 2026 बीच 308 profesionales sénior का भुगतान ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022") constató जो वह 44 % का वे बैंक नहीं están actualmente द्वारा buen camino के लिए cumplir वह plazo का dirección estructurada, के बावजूद haber gastado का media 20 millones का dólares —और में वे mayores instituciones अधिक का 30 millones— में वह preparación 2026, के साथ एक media का 13 colaboradores adicionales asignados को वे programas ISO 20022. La misma encuesta constató जो वह 32 % का वे registros का dirección का cliente जारी रखते हैं siendo नहीं estructurados का media, और जो वह 60 % का वे बैंक señalan carencias में वे तंत्र core banking को वह hora का soportar वे campos का dirección estructurada.

No है, द्वारा tanto, एक समस्या जो pueda resolverse के साथ एक mes अधिक का trabajo sobre वह motor का mensajes. Es एक समस्या का calidad का डेटा जो asciende desde वह capa का mensaje hacia वे तंत्र का onboarding, वे procesos KYC, वे canales corporativos और दशक का डेटा maestros का cliente में texto libre acumulados.

## Lo जो वह regla exige realmente

Bajo वह SWIFT CBPR+ Standards Release 2026 (SR2026), वह exigencia कुंजी है simple में principio e implacable में वह detalle. A partir का mediados का noviembre का 2026, [वह nombre का वह ciudad और वह país deben proporcionarse में उसके campos estructurados dedicados ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed") के लिए सभी वे agentes और partes में वे mensajes का भुगतान CBPR+, के साथ excepciones muy limitadas (extractos और notificaciones में camt.052, camt.053, camt.054, अधिक algunos mensajes administrativos quedan के बाहर वह exigencia estricta). Para वे agentes, वह उपयोग continuado के BIC द्वारा sí solo जारी रखता है siendo एक alternativa válida को name-and-address.

Dos formatos का dirección quedan autorizados tras वह cambio:

- **Totalmente estructurado**: cada componente का वह dirección postal se mapea को उसका elemento ISO 20022 dedicado: StrtNm (nombre का calle), BldgNb (número का edificio) या BldgNm (nombre का edificio), PstCd (कोड postal), TwnNm (nombre का ciudad), CtrySubDvsn (subdivisión país), Ctry (país, में कोड ISO 3166-1 alpha-2). Es वह formato जो SWIFT identifica explícitamente जैसे वह opción अधिक deseable जब है संभव.
- **Híbrido**: वह nombre का ciudad और वह país se rellenan में उसके campos estructurados, जबकि वह resto का वह dirección puede उपयोग करना hasta dos elementos AdrLine नहीं estructurados. Importante: [वे elementos estructurados नहीं deben repetirse के भीतर वे líneas नहीं estructuradas ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); के लिए एक componente dado, वह dirección है uno u otro.

Las direcciones totalmente नहीं estructuradas —जहाँ वह dirección completa se encuentra में elementos AdrLine बिना TwnNm ni Ctry— नहीं se aceptarán के लिए ninguno का वे campos का parte afectados. El European Payments Council है alineado उसका rulebook SEPA के साथ वह mismo cambio, द्वारा lo जो [को partir के 15 का noviembre का 2026 वह formato नहीं estructurado भी queda prohibido में SCT, SDD और SCT Inst ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). La alineación है deliberada: SWIFT और वह EPC हैं diseñado एक fin का semana único का bascula industrial.

Para despejar cualquier ambigüedad, वह [documentación का pacs008 enumera directamente वे mensajes afectados ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (deudor और acreedor में वे transferencias cliente), pacs.009 (direcciones का institución में वे transferencias FI और वे भुगतान का cobertura), pacs.004 (direcciones का parte में वे devoluciones) और pacs.003 (adeudos directos). La exigencia asciende भी aguas arriba: वे archivos pain.001 corporativos जो lleven direcciones नहीं estructuradas bloquearán वह generación conforme का pacs.008 में वह banco receptor.

## Por qué वह sector lo है convertido में एक prioridad

El argumento को favor का वे direcciones estructuradas नहीं है estético. Es operativo, और se manifiesta में tres lugares.

**Cribado का sanciones.** El beneficio práctico अधिक महत्वपूर्ण है जो वे direcciones estructuradas permiten को वे तंत्र का cribado separar वह nombre का parte का वे डेटा का localización. Los bloques का dirección में texto libre causan regularmente falsos positivos जब एक nombre का ciudad solapa के साथ एक टोकन का nombre का persona sancionada, या जब एक país enterrado में वह texto libre se pasa totalmente द्वारा उच्च. Los campos estructurados permiten को वे motores का cribado aplicar reglas का जोखिम específicas का país का manera determinista, और hacen संभव वह अनुप्रयोग के matching का lista का sanciones contra वह कोड का país के बजाय adivinar sobre एक cadena parseada. El análisis का CGI UK publicado में marzo का 2026 subraya यह punto explícitamente: [वे डेटा का dirección estructurados se vuelven centrales के लिए वह resiliencia operativa, और नहीं simplemente एक obligación का cumplimiento ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Tasas का reparación manual.** Los भुगतान सीमा-पार actuales llevan एक coste operativo significativo में forma का investigaciones manuales, gestión का excepciones और colas का reparación, में gran parte motivado द्वारा direcciones जो वे तंत्र का cribado या का enrutamiento नहीं pueden parsear के साथ विश्वास. Los बैंक जो ya हैं अतीत को वे direcciones estructuradas reportan reducciones materiales का excepciones STP, में particular में वे flujos का mitad का corredor जहाँ वे agentes बिचौलिये antes debían interpretar डेटा में texto libre जो नहीं habían generado.

**Aplicación को nivel का नेटवर्क.** SR2026 endurece वह मान्यकरण को nivel का वह नेटवर्क SWIFT. Algunos का वे नए controles operarán inicialmente में modo नहीं bloqueante —señalando समस्याएँ का calidad का डेटा बिना detener वे भुगतान— परंतु वह trayectoria है clara, और tras वह cambio, [वे mensajes नहीं conformes होंगे rechazados का manera pura और simple ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Varios rails का भुगतान estadounidenses (Fedwire, CHIPS) और SWIFT CBPR+ convergen esencialmente में वह mismo calendario, lo जो elimina वह opción का एक cambio escalonado जो algunas instituciones habían supuesto में planes anteriores.

## La vista द्वारा campo: lo जो cambia में वह mensaje

El mensaje pacs.008 admite direcciones estructuradas desde जो वे primeras directrices का उपयोग CBPR+ entraron में vigor में marzo का 2023. Lo जो cambia में noviembre का 2026 नहीं है वह esquema, है वह मान्यकरण. Hasta ahora, वे बैंक हैं podido poblar वे elementos AdrLine के साथ texto libre और hacerlo pasar द्वारा वह नेटवर्क. A partir के plazo, वे contenidos का वे bloques का parte deben satisfacer वे requisitos mínimos का campos estructurados.

### Requerido, recomendado और retirado

| Elemento | XPath (निम्न `PstlAdr`) | Estado tras nov. 2026 | Notas |
|---|---|---|---|
| Nombre का ciudad | `<TwnNm>` | **Obligatorio** | Al कम एक nombre का ciudad estructurado द्वारा parte afectada |
| País | `<Ctry>` | **Obligatorio** | Código ISO 3166-1 alpha-2 |
| Nombre का calle | `<StrtNm>` | Altamente recomendado | Requerido के लिए वह formato totalmente estructurado |
| Número का edificio | `<BldgNb>` | Recomendado | O BldgNb, या PstBx, नहीं ambos |
| Apartado का correos | `<PstBx>` | Recomendado | Alternativa को BldgNb |
| Código postal | `<PstCd>` | Recomendado | Requerido द्वारा algunos esquemas locales |
| Subdivisión país | `<CtrySubDvsn>` | Opcional | Estado, región, provincia |
| Línea का dirección (texto libre) | `<AdrLine>` | **Restringido** | Máx. 2 líneas में híbrido; nunca junto को mismo componente में वे campos estructurados |
| Tipo का dirección | `<AdrTp>` | Opcional | Uso का `ADDR` recomendado के लिए वे direcciones postales |

*Fuente: síntesis का वे directrices का उपयोग SWIFT CBPR+ के लिए SR2026 और का वह [documentación का dirección estructurada pacs008.com ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008").*

La implicación práctica है जो toda institución जो अब भी se apoye में AdrLine में solitario —ya sea में उसका propia generación का mensaje, में वे archivos pain.001 recibidos का ग्राहक corporativos, या में वे registros का डेटा maestros utilizados के लिए enriquecer वे भुगतान में flujo— debe migrar वे डेटा को वे campos estructurados antes के cambio. El servicio का traducción में vuelo का SWIFT puede ayudar में tránsito, परंतु [sufre recargos से शुरू होकर enero का 2026 ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB") और नहीं puede parsear का manera fiable सभी वे formatos का dirección. SWIFT भी है publicado [एक मॉडल का IA का ओपन-सोर्स का estructuración का dirección ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model") entrenado के साथ डेटा का अधिक का 200 países के लिए inferir ciudad और país से शुरू होकर डेटा heredados नहीं estructurados के साथ puntuaciones का विश्वास, परंतु है explícitamente एक ayuda को वह remediación, नहीं एक sustituto को largo plazo का वे डेटा limpios aguas arriba.

## Cómo pacs008.com ayuda को comprimir वह calendario

Para वे instituciones जो necesitan industrializar उसके pipelines का calidad का dirección और मान्यकरण का mensajes rápidamente, [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") proporciona एक caja का उपकरण का ओपन-सोर्स निम्न licencia MIT और एक servicio FastAPI diseñados específicamente के लिए वह workflow का transferencia cliente FI को FI. Aborda वे tres capas में वे जो वे programas का remediación se estancan के साथ अधिक frecuencia: मान्यकरण का डेटा, generación XML और अनुप्रयोग द्वारा pipeline.

Las capacidades का dirección estructurada का वह caja का उपकरण están alineadas को वे requisitos SR2026:

- **Validación pregeneración** का वे campos का dirección postal estructurados e híbridos, के लिए जो वे डेटा नहीं conformes sean interceptados antes का जो se produzca या envíe XML alguno.
- **Marcado का वे डेटा का dirección नहीं estructurados** जो fallarían tras वह plazo का noviembre का 2026, के साथ एक distinción clara बीच casos aceptables में híbrido और casos totalmente नहीं estructurados.
- **Soporte doble formato** के लिए वे formatos híbridos preplazo और वे configuraciones totalmente estructuradas posplazo, permitiendo को वे instituciones migrar progresivamente बिना romper वह इंटरऑपरेबिलिटी के साथ वे contrapartes जो अब भी नहीं हैं completado उसके propias transiciones.
- **Integración में pipeline CI** के लिए जो वे controles का calidad का dirección formen parte के proceso का build, और नहीं एक afterthought को अंतिम के flujo: वह respuesta práctica को वह observación का CGI según वह cual [वह शासन का वे डेटा debe ser एक principio का diseño मूलभूत ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement") के बजाय एक sobrecapa का cumplimiento.

Más allá का वे direcciones, वह caja का उपकरण cubre वह superficie अधिक amplia का मान्यकरण जो वह versión SR2026 endurece: मान्यकरण JSON Schema contra 20 esquemas específicos का mensaje, सत्यापन का formato IBAN और checksum में 75 países, मान्यकरण XSD के XML generado contra वे esquemas oficiales ISO 20022, और generación version-aware को través के conjunto का वे 13 revisiones का pacs.008 soportadas (pacs.008.001.01 को pacs.008.001.13). Para वे equipos operativos और का cumplimiento, incluye भी वह prevención का XXE mediante defusedxml, वह protección estricta contra वह path traversal और वह enmascaramiento का PII में वे registros JSON estructurados के लिए soportar वे exigencias का RGPD और PCI DSS, वह tipo का controles नहीं negociables में वे flujos का भुगतान में producción परंतु को menudo añadidos tardíamente में वे migraciones lideradas द्वारा proveedor.

La biblioteca está उपलब्ध [में PyPI ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") में forma का paquete `pip install pacs008` और में [GitHub ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") के साथ पारदर्शिता total के स्रोत-कोड. Para वे instituciones जो evalúan उसके opciones, esto importa: वे उपकरण का ओपन-सोर्स permiten को वे equipos internos auditar वह lógica का मान्यकरण, integrarla में bases Python या FastAPI existentes बिना negociaciones का licencia, और aportar parches को medida जो aparezcan उसके propios casos límite.

Vale वह pena ser preciso sobre वह alcance. pacs008 है एक caja का उपकरण का capa का mensaje; नहीं reemplaza एक motor का भुगतान, एक तंत्र का cribado या वह remediación का वे डेटा maestros का cliente जो एक institución todavía debe hacer में वह fuente. Lo जो hace है tomar वह trabajo का remediación और hacerlo aplicable: convertir वह cumplimiento का dirección estructurada का एक revisión manual को अंतिम का एक cadena larga में एक puerta स्वचालित में वह punto का generación. Para वे programas के साथ poco tiempo, वह puerta marca वह diferencia बीच एक cambio limpio और एक ola का rechazos poscambio.

## El panorama का वे उपकरण

pacs008 se inscribe में एक तंत्र अधिक amplio का उपकरण का mensajes ISO 20022, और वह elección के enfoque depende के stack, वह escala और वह filosofía का migración का वह institución. El paisaje open source और comercial incluye [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (amplia biblioteca Python multicategoría के साथ मान्यकरण में beta), वह biblioteca asociada [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") के लिए वह iniciación का भुगतान aguas arriba, [Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (एक biblioteca Java exhaustiva Apache 2.0 के साथ एक capa comercial के लिए वह मान्यकरण और वे traducciones CBPR+), और एक serie का प्लेटफ़ॉर्म comerciales —Mambu, Kyriba, PaymentComponents और otras— जो empaquetan वह capacidad ISO 20022 में ofertas अधिक amplias का tesorería या का प्लेटफ़ॉर्म का भुगतान.

El compromiso है familiar. Las प्लेटफ़ॉर्म comerciales reducen वह carga का ingeniería interna परंतु atan को वह institución को एक hoja का ruta का proveedor जो puede नहीं corresponder को वह suya. Las bibliotecas multicategoría exhaustivas cubren एक superficie अधिक amplia परंतु exigen अधिक trabajo का integración के लिए एक tipo का mensaje dado. Las bibliotecas का ओपन-सोर्स focalizadas —pacs008 के लिए वह transferencia cliente FI को FI, [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) के लिए वह iniciación का भुगतान— minimizan वह tiempo का integración के लिए वे instituciones जो necesitan abordar rápidamente cuellos का botella específicos, और dejan को वह institución dueña का उसके propias reglas का मान्यकरण. Para वह समस्या का dirección estructurada में particular, एक enfoque focalizado tiene वह ventaja का जो वे reglas aplicadas हैं estrechas, bien definidas और poco susceptibles का cambiar antes के cambio.

## Lo जो esto significa द्वारा sector

El plazo का noviembre का 2026 नहीं afecta को सभी वे instituciones द्वारा igual. La respuesta correcta depende के volumen का tráfico सीमा-पार, का वह madurez के dominio का डेटा existente और के papel जो desempeña वह institución में वह cadena का भुगतान.

### Grandes बैंक corresponsales और सीमा-पार

Para वे बैंक का पहला nivel जो operan एक tráfico CBPR+ significativo, वह exigencia का dirección estructurada है एक workstream के भीतर एक programa का preparación SR2026 mucho अधिक amplio जो भी cubre excepciones e investigaciones, endurecimiento BAH और (में Estados Unidos) वह migración simultánea का Fedwire और CHIPS. Los डेटा का RedCompass Labs sugieren जो वह mayoría का ये instituciones gastan बीच 20 और 30 millones का dólares में वह preparación 2026, के साथ equipos का entrega का 10 को 20 especialistas. El जोखिम के लिए यह grupo नहीं है वह capacidad técnica, है वह capacidad का entrega. Con कई workstreams paralelos disputándose वे mismas ventanas का release, वह remediación का calidad का dirección puede deslizarse silenciosamente द्वारा detrás का workstreams अधिक visibles hasta convertirse में एक समस्या का semana का cambio. El paliativo práctico है subir वह मान्यकरण का dirección अधिक arriba में वह pipeline, के लिए जो वे fallos emerjan में entornos का विकास और prueba meses antes का haber alcanzado वह producción.

### Bancos का tamaño medio e instituciones का भुगतान

Para वे बैंक का tamaño medio और वे instituciones EMI/PI, वह exigencia का dirección estructurada है को menudo वह obligación 2026 अधिक material जो afrontan, क्योंकि नहीं llevan वह misma carga का workstreams concomitantes जो वे बैंक का पहला nivel. El चुनौती aquí है habitualmente वह calidad का डेटा aguas arriba. Los procesos का onboarding का cliente जो हैं capturado direcciones में texto libre के दौरान दशक producen dominios का डेटा maestros जो नहीं हैं inmediatamente parseables. La remediación स्वचालित —utilizando वह मॉडल का estructuración का dirección open source का SWIFT, servicios comerciales का limpieza का dirección या एक combinación— puede abordar एक parte sustancial का वे registros, परंतु एक larga cola residual का direcciones internacionales complejas requerirá एक revisión manual. Cuanto antes empiece वह trabajo, अधिक pequeña se vuelve वह cola.

### Corporativos और proveedores का servicios का भुगतान

Los corporativos जो inician भुगतान vía pain.001 están aguas arriba का वह generación का pacs.008 द्वारा वह banco परंतु नहीं están exentos का वह exigencia का dirección estructurada. Los बैंक नहीं rellenarán retroactivamente वे direcciones का beneficiario में nombre का वे ग्राहक corporativos; वे डेटा estructurados deben provenir का वे तंत्र propios के corporativo. Para वे tesoreros का उद्यम, esto significa asegurar जो वे तंत्र ERP और का tesorería capturen वे direcciones का beneficiario में forma estructurada, जो वह जानकारी का signatario और deudor último भी esté estructurada, और जो वे plantillas का iniciación का भुगतान नहीं abandonen silenciosamente campos को generar वह archivo. La मान्यकरण previa को vuelo का वे archivos pain.001 —utilizando bien वे उपकरण propias के corporativo, bien servicios expuestos द्वारा वह banco— se convierte में वह punto का नियंत्रण práctico.

### Proveedores, fintechs e integradores

Para वे proveedores जो construyen sobre वे rails का भुगतान, वह plazo है एक función का forzamiento के लिए वह capacidad ISO 20022 जो podría haberse aplazado को fases posteriores. Las fintechs जो enrutan या inician भुगतान सीमा-पार के माध्यम से socios बैंकिंग deben subir वह captura का dirección estructurada को उसके propias UI और API, या aceptar जो वे archivos pain.001 conformes नहीं puedan producirse से शुरू होकर उसके डेटा. La अवसर, के लिए वे proveedores capaces का moverse तेज़, है absorber वह carga का remediación में nombre का वे ग्राहक corporativos: बदलना एक समस्या का cumplimiento में servicio.

## निष्कर्ष

El plazo का dirección estructurada का noviembre का 2026 है, में cierto sentido, एक cambio estrecho: dos campos obligatorios, algunos recomendados, और वह retirada का एक opción में texto libre जो nunca debería haberse उपयोग किया गया के लिए डेटा relevantes के लिए वह cribado का sanciones में पहला lugar. En otro sentido, है वह hito ISO 20022 अधिक significativo operacionalmente desde वह migración CBPR+ original, क्योंकि fuerza वह dato estructurado नहीं solo में वह capa का mensaje sino में वे तंत्र aguas arriba जो वह alimentan.

El cuadro का preparación को nivel का sector, को seis meses के plazo, नहीं है alentador. Dos tercios का वे mensajes CBPR+ जारी रखते हैं llevando direcciones नहीं estructuradas. Casi वह mitad का वे बैंक नहीं van द्वारा buen camino. Cerca का एक tercio का वे registros का dirección का cliente जारी रखते हैं siendo नहीं parseables. La financiación está में उसका sitio —वे encuestas muestran constantemente निवेश का ocho और nueve cifras— परंतु वह trabajo नहीं, और वह dimensión का calidad का डेटा के समस्या नहीं puede resolverse solo के साथ gasto में वे últimos meses.

Lo जो ayuda ahora है वह स्वचालन में वह punto का मान्यकरण: empujar वे reglas को pipelines जो intercepten वे समस्याएँ antes का जो alcancen वह नेटवर्क, के बजाय después. Para वे instituciones जो operan bases Python या FastAPI, वे उपकरण open source जैसे [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") proporcionan एक manera práctica का operar वह cambio बिना ciclo का selección का proveedor. Para सभी वे demás, independientemente के stack, वह punto estratégico है वह mismo: वे instituciones जो industrialicen वह cambio ahora estarán में एक posición mucho अधिक fuerte जो वे जो se apoyen में एक cumplimiento का última hora, द्वारा tomar prestada वह formulación का वे investigaciones का RedCompass Labs जो है enmarcado gran parte का वह conversación 2026.

El fin का semana का cambio में noviembre cerrará एक capítulo. Las instituciones जो lleguen को él के साथ डेटा limpios, मान्यकरण स्वचालित और comprensión operativa का lo जो वे direcciones estructuradas hacen realmente के लिए वह cribado का sanciones pasarán वह fin का semana vigilando वह tráfico. Las जो lleguen बिना वे cosas lo pasarán को teléfono.

## Preguntas frecuentes

**¿Qué cambia exactamente वह plazo का noviembre का 2026?**

A partir का mediados का noviembre का 2026, SWIFT CBPR+ rechazará वे mensajes pacs.008, pacs.009, pacs.004 और pacs.003 cuyos campos का parte contengan únicamente direcciones postales नहीं estructuradas. La exigencia estructurada mínima है वह nombre का ciudad में वह elemento TwnNm और वह país में वह elemento Ctry (utilizando वह कोड ISO 3166-1 alpha-2). Las direcciones híbridas जारी रखते हैं permitidas —ciudad और país में campos estructurados, अधिक hasta dos elementos AdrLine में texto libre के लिए वे componentes restantes— परंतु वह mismo componente नहीं puede figurar को वह vez में वे campos estructurados और नहीं estructurados. Las direcciones totalmente estructuradas हैं वह formato preferido. El European Payments Council है alineado वे esquemas SEPA (SCT, SDD, SCT Inst) के साथ वह misma fecha का cambio.

**¿Qué mensajes और qué campos का parte están afectados?**

Para pacs.008, वह exigencia se aplica को वे direcciones postales के deudor और के acreedor. Para pacs.009, se aplica को वे direcciones का institución में वे transferencias FI और वे भुगतान का cobertura. Para pacs.004, se aplica को वे direcciones का parte में वे devoluciones का भुगतान. Para pacs.003, se aplica को वे direcciones का acreedor और deudor में वे adeudos directos का ग्राहक. Los mensajes का extracto और notificación (camt.052, camt.053, camt.054) और algunos mensajes administrativos quedan के बाहर वह exigencia estricta. Los mensajes pain.001 aguas arriba का वे ग्राहक corporativos नहीं se rigen directamente द्वारा CBPR+, परंतु वे direcciones नहीं estructuradas में वे archivos pain.001 bloquearán वह generación conforme का pacs.008 aguas abajo और están, द्वारा tanto, efectivamente में वह alcance.

**¿Cuál है वह diferencia बीच dirección estructurada, híbrida और नहीं estructurada?**

Una dirección totalmente estructurada mapea cada componente को उसका elemento ISO 20022 dedicado: StrtNm, BldgNb या PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. Una dirección híbrida tiene वह nombre का ciudad और वह país में campos estructurados, वह resto का वह dirección में hasta dos elementos AdrLine में texto libre; वह mismo componente नहीं debe figurar में वे dos. Una dirección नहीं estructurada tiene वह dirección postal entera में elementos AdrLine बिना TwnNm ni Ctry estructurados; है वह formato retirado में noviembre का 2026 के लिए वे campos का parte afectados.

**¿Cómo ayuda pacs008.com में यह transición?**

La biblioteca [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") valida वे campos का dirección postal estructurados e híbridos antes का वह generación XML, marca वे डेटा नहीं estructurados जो fallarían tras वह plazo, soporta वे formatos híbridos preplazo और totalmente estructurados posplazo, और se integra में वे pipelines CI और workflows का मान्यकरण द्वारा lote. Genera XML के लिए वे 13 versiones का pacs.008 soportadas, valida contra वे esquemas XSD oficiales ISO 20022, और expone एक servicio FastAPI के लिए वह orquestación स्वचालित. Es open source निम्न licencia का tipo MIT, está उपलब्ध में PyPI और se है diseñado específicamente के लिए वे workflows का transferencia cliente FI को FI; वे reglas का मान्यकरण están, द्वारा tanto, calibradas sobre वे directrices का उपयोग SWIFT CBPR+ SR2026 के बजाय abstraídas sobre numerosos tipos का mensajes.

**¿Qué ocurre यदि mi institución नहीं está lista में noviembre का 2026?**

Los mensajes के साथ direcciones नहीं estructuradas में वे campos का parte afectados होंगे rechazados को nivel का नेटवर्क tras वह cambio. En वह práctica, esto se traduce में fallos का भुगतान, volúmenes का excepción mayores, oleadas का reparación manual e impacto probable में वह cliente. El servicio का traducción में vuelo का SWIFT está उपलब्ध के लिए algunos casos transitorios परंतु sufre recargos से शुरू होकर enero का 2026 और नहीं puede parsear का manera fiable सभी वे formatos का dirección. SWIFT भी है publicado एक मॉडल का IA का ओपन-सोर्स का estructuración का dirección जो infiere ciudad और país से शुरू होकर डेटा heredados नहीं estructurados, परंतु está diseñado के लिए वह remediación और वह preprocesamiento, नहीं जैसे sustituto permanente का वे डेटा limpios aguas arriba. Las instituciones जो lleguen को plazo बिना एक dominio का डेटा maestros remediado और एक pipeline का मान्यकरण स्वचालित deberían esperar एक semana का cambio difícil और एक subida operativa significativa में वे meses siguientes.

## संदर्भ-स्रोत

- Sebastien Rousseau, (2023). [Automating ISO 20022-Compliant Payment File Creation with Pain001](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html "Automating ISO 20022-Compliant Payment File Creation with Pain001").
- pacs008, (2026). [November 2026 structured-address deadline ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"). pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 Toolkit and API ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"). pacs008.com.
- SWIFT, (2026). [ISO 20022 milestone for November 2026: Unstructured addresses to be removed ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"). SWIFT.
- SWIFT, (2026). [ISO 20022 for Financial Institutions ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions "ISO 20022 for Financial Institutions"). SWIFT.
- SWIFT, (2026). [The Swift AI address structuring model ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"). SWIFT.
- RedCompass Labs, (2026). [Nearly Half of Banks Are Behind on ISO 20022 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022"). Financial IT.
- RedCompass Labs, (2026). [ISO 20022 is arriving all at once for US banks ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). RedCompass Labs.
- ClearingPost, (2026). [The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline"). ClearingPost.
- CGI UK, (2026). [2026: A defining year for ISO 20022 and structured data enforcement ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"). CGI UK.
- J.P. Morgan, (2026). [ISO 20022 Migration: Guidance, Messaging & More ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration "ISO 20022 Migration: Guidance, Messaging & More"). J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022 "FAQ Swift ISO 20022 — ING"). ING Wholesale Banking.
- Mambu, (2026). [CBPR+ is live: what ISO 20022 means in practice ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice "CBPR+ is live: what ISO 20022 means in practice"). Mambu.
- Kyriba, (2026). [ISO 20022 migration: what every treasury team needs to know about what's next ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/ "ISO 20022 migration: what every treasury team needs to know about what's next"). Kyriba.
- Standard Chartered, (2025). [ISO 20022 – Standard Chartered Address Guidelines (H2H and API) ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf "Standard Chartered ISO 20022 Address Guidelines"). Standard Chartered.
- State Street, (2025). [Client Guide to ISO 20022 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"). State Street.
- ISO 20022, (2026). [Message Definitions Catalogue ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 Message Definitions"). ISO 20022.
