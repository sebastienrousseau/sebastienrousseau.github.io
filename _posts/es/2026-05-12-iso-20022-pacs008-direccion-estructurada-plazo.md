---
title: "El plazo pacs.008 de «dirección estructurada» de noviembre de 2026: vista a seis meses"
subtitle: "A mediados de noviembre de 2026, SWIFT CBPR+ rechazará las direcciones postales no estructuradas en los mensajes pacs.008 y mensajes de pago transfronterizos asociados."
description: "A mediados de noviembre de 2026, SWIFT CBPR+ rechazará las direcciones postales no estructuradas en los mensajes pacs.008 y mensajes asociados. Con cerca del 65 % de mensajes aún no conformes y el 44 % de los bancos atrasados, la ventana de remediación se cierra más rápido de lo que la mayoría de los programas de preparación están diseñados para gestionar."
date: "May 12, 2026"
language: "es-ES"
locale: "es_ES"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "Esquema de un mensaje de pago transfronterizo con dirección estructurada, con TwnNm y Ctry resaltados"
keywords: "ISO 20022, pacs.008, pacs.009, pacs.004, pacs.003, pain.001, CBPR+, SWIFT, SR2026, dirección estructurada, SEPA, EPC, pagos transfronterizos, cribado de sanciones, pacs008"
---

A partir de mediados de noviembre de 2026, SWIFT CBPR+ rechazará las direcciones postales no estructuradas en los mensajes pacs.008 y mensajes de pago transfronterizos asociados. Con cerca del 65 % de los mensajes aún no conformes y el 44 % de los bancos atrasados, la ventana de remediación se cierra más rápido de lo que la mayoría de los programas de preparación están diseñados para gestionar.

---

> **TL;DR.** La regla SR2026 obliga a estructurar al menos el nombre de la ciudad y el país en pacs.008, pacs.009, pacs.004 y pacs.003 desde mediados de noviembre de 2026. La preparación del sector es desigual y la ventana de remediación se cierra rápidamente; los pipelines automatizados de validación son hoy el palanca práctica clave.
>
> **Conclusiones clave**
>
> - A partir de **noviembre de 2026**, SWIFT CBPR+ dejará de aceptar direcciones postales no estructuradas en los mensajes de pago transfronterizos. El cambio se aplica a **pacs.008** (transferencia cliente), **pacs.009** (transferencia interbancaria), **pacs.004** (devoluciones) y **pacs.003** (adeudos directos), así como a los flujos **pain.001** aguas arriba que los alimentan.
> - Como mínimo, el **nombre de la ciudad (TwnNm)** y el **país (Ctry)** deben estar presentes en campos estructurados dedicados. El **nombre de la calle (StrtNm)** y bien el **número de edificio (BldgNb)**, bien el **apartado de correos (PstBx)**, son altamente recomendados. Las líneas de dirección en texto libre (AdrLine) por sí solas ya no satisfarán la exigencia para los campos de partes clave.
> - El cambio mejora la precisión del cribado de sanciones, reduce las tasas de reparación manual y protege el straight-through processing, pero solo para las instituciones que han remediado sus datos de cliente aguas arriba, no solo sus motores de mensajes.
> - La preparación industrial es desigual. En marzo de 2026, alrededor del **65 % de los mensajes CBPR+ siguen llevando direcciones no estructuradas**, el **44 % de los bancos** no van por buen camino para el plazo, y el **32 % de los registros de dirección de cliente** siguen siendo no estructurados de media.
> - Herramientas de código abierto, incluida **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, una biblioteca Python y un servicio FastAPI para generar, validar y orquestar los flujos de mensajes pacs.008, pueden comprimir los plazos de remediación automatizando la validación de esquema, los controles de calidad de dirección y la aplicación en el nivel CI antes de que los mensajes alcancen la red SWIFT.

---

## Un plazo que siempre estuvo en camino

La exigencia de dirección estructurada de noviembre de 2026 no es un golpe normativo repentino. Figura en la hoja de ruta SWIFT CBPR+ desde el anuncio inicial de la migración [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html), y sigue al fin de la cohabitación MT/MX de noviembre de 2025. Lo que ha cambiado en 2026 es la proximidad. Con cerca de seis meses restantes, el sector opera ya dentro de la ventana en la que los problemas de calidad de datos no resueltos se convierten en un riesgo operativo.

Las cifras cuentan la historia con claridad. La actualización comunitaria de SWIFT de marzo de 2026 señala que [alrededor del 65 % de los mensajes de pago todavía contienen direcciones no estructuradas ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), y que la adopción sigue siendo desigual entre geografías y tipos de instituciones. Una [encuesta de RedCompass Labs de marzo de 2026 entre 308 profesionales sénior de pagos ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022") constató que el 44 % de los bancos no están actualmente por buen camino para cumplir el plazo de dirección estructurada, a pesar de haber gastado de media 20 millones de dólares —y en las mayores instituciones más de 30 millones— en la preparación 2026, con una media de 13 colaboradores adicionales asignados a los programas ISO 20022. La misma encuesta constató que el 32 % de los registros de dirección de cliente siguen siendo no estructurados de media, y que el 60 % de los bancos señalan carencias en los sistemas core banking a la hora de soportar los campos de dirección estructurada.

No es, por tanto, un problema que pueda resolverse con un mes más de trabajo sobre el motor de mensajes. Es un problema de calidad de datos que asciende desde la capa de mensaje hacia los sistemas de onboarding, los procesos KYC, los canales corporativos y décadas de datos maestros de cliente en texto libre acumulados.

## Lo que la regla exige realmente

Bajo la SWIFT CBPR+ Standards Release 2026 (SR2026), la exigencia clave es simple en principio e implacable en el detalle. A partir de mediados de noviembre de 2026, [el nombre de la ciudad y el país deben proporcionarse en sus campos estructurados dedicados ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed") para todos los agentes y partes en los mensajes de pago CBPR+, con excepciones muy limitadas (extractos y notificaciones en camt.052, camt.053, camt.054, más algunos mensajes administrativos quedan fuera de la exigencia estricta). Para los agentes, el uso continuado del BIC por sí solo sigue siendo una alternativa válida a name-and-address.

Dos formatos de dirección quedan autorizados tras el cambio:

- **Totalmente estructurado**: cada componente de la dirección postal se mapea a su elemento ISO 20022 dedicado: StrtNm (nombre de calle), BldgNb (número de edificio) o BldgNm (nombre de edificio), PstCd (código postal), TwnNm (nombre de ciudad), CtrySubDvsn (subdivisión país), Ctry (país, en código ISO 3166-1 alpha-2). Es el formato que SWIFT identifica explícitamente como la opción más deseable cuando es posible.
- **Híbrido**: el nombre de ciudad y el país se rellenan en sus campos estructurados, mientras que el resto de la dirección puede utilizar hasta dos elementos AdrLine no estructurados. Importante: [los elementos estructurados no deben repetirse dentro de las líneas no estructuradas ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); para un componente dado, la dirección es uno u otro.

Las direcciones totalmente no estructuradas —donde la dirección completa se encuentra en elementos AdrLine sin TwnNm ni Ctry— no se aceptarán para ninguno de los campos de parte afectados. El European Payments Council ha alineado su rulebook SEPA con el mismo cambio, por lo que [a partir del 15 de noviembre de 2026 el formato no estructurado también queda prohibido en SCT, SDD y SCT Inst ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). La alineación es deliberada: SWIFT y el EPC han diseñado un fin de semana único de bascula industrial.

Para despejar cualquier ambigüedad, la [documentación de pacs008 enumera directamente los mensajes afectados ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (deudor y acreedor en las transferencias cliente), pacs.009 (direcciones de institución en las transferencias FI y los pagos de cobertura), pacs.004 (direcciones de parte en las devoluciones) y pacs.003 (adeudos directos). La exigencia asciende también aguas arriba: los archivos pain.001 corporativos que lleven direcciones no estructuradas bloquearán la generación conforme de pacs.008 en el banco receptor.

## Por qué el sector lo ha convertido en una prioridad

El argumento a favor de las direcciones estructuradas no es estético. Es operativo, y se manifiesta en tres lugares.

**Cribado de sanciones.** El beneficio práctico más importante es que las direcciones estructuradas permiten a los sistemas de cribado separar el nombre de parte de los datos de localización. Los bloques de dirección en texto libre causan regularmente falsos positivos cuando un nombre de ciudad solapa con un token de nombre de persona sancionada, o cuando un país enterrado en el texto libre se pasa totalmente por alto. Los campos estructurados permiten a los motores de cribado aplicar reglas de riesgo específicas de país de manera determinista, y hacen posible la aplicación del matching de lista de sanciones contra el código de país en lugar de adivinar sobre una cadena parseada. El análisis de CGI UK publicado en marzo de 2026 subraya este punto explícitamente: [los datos de dirección estructurados se vuelven centrales para la resiliencia operativa, y no simplemente una obligación de cumplimiento ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Tasas de reparación manual.** Los pagos transfronterizos actuales llevan un coste operativo significativo en forma de investigaciones manuales, gestión de excepciones y colas de reparación, en gran parte motivado por direcciones que los sistemas de cribado o de enrutamiento no pueden parsear con confianza. Los bancos que ya han pasado a las direcciones estructuradas reportan reducciones materiales de excepciones STP, en particular en los flujos de mitad de corredor donde los agentes intermediarios antes debían interpretar datos en texto libre que no habían generado.

**Aplicación a nivel de red.** SR2026 endurece la validación a nivel de la red SWIFT. Algunos de los nuevos controles operarán inicialmente en modo no bloqueante —señalando problemas de calidad de datos sin detener los pagos— pero la trayectoria es clara, y tras el cambio, [los mensajes no conformes serán rechazados de manera pura y simple ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Varios rails de pago estadounidenses (Fedwire, CHIPS) y SWIFT CBPR+ convergen esencialmente en el mismo calendario, lo que elimina la opción de un cambio escalonado que algunas instituciones habían supuesto en planes anteriores.

## La vista por campo: lo que cambia en el mensaje

El mensaje pacs.008 admite direcciones estructuradas desde que las primeras directrices de uso CBPR+ entraron en vigor en marzo de 2023. Lo que cambia en noviembre de 2026 no es el esquema, es la validación. Hasta ahora, los bancos han podido poblar los elementos AdrLine con texto libre y hacerlo pasar por la red. A partir del plazo, los contenidos de los bloques de parte deben satisfacer los requisitos mínimos de campos estructurados.

### Requerido, recomendado y retirado

| Elemento | XPath (bajo `PstlAdr`) | Estado tras nov. 2026 | Notas |
|---|---|---|---|
| Nombre de ciudad | `<TwnNm>` | **Obligatorio** | Al menos un nombre de ciudad estructurado por parte afectada |
| País | `<Ctry>` | **Obligatorio** | Código ISO 3166-1 alpha-2 |
| Nombre de calle | `<StrtNm>` | Altamente recomendado | Requerido para el formato totalmente estructurado |
| Número de edificio | `<BldgNb>` | Recomendado | O BldgNb, o PstBx, no ambos |
| Apartado de correos | `<PstBx>` | Recomendado | Alternativa a BldgNb |
| Código postal | `<PstCd>` | Recomendado | Requerido por algunos esquemas locales |
| Subdivisión país | `<CtrySubDvsn>` | Opcional | Estado, región, provincia |
| Línea de dirección (texto libre) | `<AdrLine>` | **Restringido** | Máx. 2 líneas en híbrido; nunca junto al mismo componente en los campos estructurados |
| Tipo de dirección | `<AdrTp>` | Opcional | Uso de `ADDR` recomendado para las direcciones postales |

*Fuente: síntesis de las directrices de uso SWIFT CBPR+ para SR2026 y de la [documentación de dirección estructurada pacs008.com ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008").*

La implicación práctica es que toda institución que aún se apoye en AdrLine en solitario —ya sea en su propia generación de mensaje, en los archivos pain.001 recibidos de clientes corporativos, o en los registros de datos maestros utilizados para enriquecer los pagos en flujo— debe migrar esos datos a los campos estructurados antes del cambio. El servicio de traducción en vuelo de SWIFT puede ayudar en tránsito, pero [sufre recargos a partir de enero de 2026 ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB") y no puede parsear de manera fiable todos los formatos de dirección. SWIFT también ha publicado [un modelo de IA de código abierto de estructuración de dirección ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model") entrenado con datos de más de 200 países para inferir ciudad y país a partir de datos heredados no estructurados con puntuaciones de confianza, pero es explícitamente una ayuda a la remediación, no un sustituto a largo plazo de los datos limpios aguas arriba.

## Cómo pacs008.com ayuda a comprimir el calendario

Para las instituciones que necesitan industrializar sus pipelines de calidad de dirección y validación de mensajes rápidamente, [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") proporciona una caja de herramientas de código abierto bajo licencia MIT y un servicio FastAPI diseñados específicamente para el workflow de transferencia cliente FI a FI. Aborda las tres capas en las que los programas de remediación se estancan con más frecuencia: validación de datos, generación XML y aplicación por pipeline.

Las capacidades de dirección estructurada de la caja de herramientas están alineadas a los requisitos SR2026:

- **Validación pregeneración** de los campos de dirección postal estructurados e híbridos, para que los datos no conformes sean interceptados antes de que se produzca o envíe XML alguno.
- **Marcado de los datos de dirección no estructurados** que fallarían tras el plazo de noviembre de 2026, con una distinción clara entre casos aceptables en híbrido y casos totalmente no estructurados.
- **Soporte doble formato** para los formatos híbridos preplazo y las configuraciones totalmente estructuradas posplazo, permitiendo a las instituciones migrar progresivamente sin romper la interoperabilidad con las contrapartes que aún no han completado sus propias transiciones.
- **Integración en pipeline CI** para que los controles de calidad de dirección formen parte del proceso de build, y no un afterthought al final del flujo: la respuesta práctica a la observación de CGI según la cual [la gobernanza de los datos debe ser un principio de diseño fundamental ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement") en lugar de una sobrecapa de cumplimiento.

Más allá de las direcciones, la caja de herramientas cubre la superficie más amplia de validación que la versión SR2026 endurece: validación JSON Schema contra 20 esquemas específicos de mensaje, verificación de formato IBAN y checksum en 75 países, validación XSD del XML generado contra los esquemas oficiales ISO 20022, y generación version-aware a través del conjunto de las 13 revisiones de pacs.008 soportadas (pacs.008.001.01 a pacs.008.001.13). Para los equipos operativos y de cumplimiento, incluye también la prevención de XXE mediante defusedxml, la protección estricta contra el path traversal y el enmascaramiento de PII en los registros JSON estructurados para soportar las exigencias de RGPD y PCI DSS, el tipo de controles no negociables en los flujos de pago en producción pero a menudo añadidos tardíamente en las migraciones lideradas por proveedor.

La biblioteca está disponible [en PyPI ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") en forma de paquete `pip install pacs008` y en [GitHub ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") con transparencia total del código fuente. Para las instituciones que evalúan sus opciones, esto importa: las herramientas de código abierto permiten a los equipos internos auditar la lógica de validación, integrarla en bases Python o FastAPI existentes sin negociaciones de licencia, y aportar parches a medida que aparezcan sus propios casos límite.

Vale la pena ser preciso sobre el alcance. pacs008 es una caja de herramientas de capa de mensaje; no reemplaza un motor de pagos, un sistema de cribado o la remediación de los datos maestros de cliente que una institución todavía debe hacer en la fuente. Lo que hace es tomar ese trabajo de remediación y hacerlo aplicable: convertir el cumplimiento de dirección estructurada de una revisión manual al final de una cadena larga en una puerta automatizada en el punto de generación. Para los programas con poco tiempo, esa puerta marca la diferencia entre un cambio limpio y una ola de rechazos poscambio.

## El panorama de las herramientas

pacs008 se inscribe en un ecosistema más amplio de herramientas de mensajes ISO 20022, y la elección del enfoque depende del stack, la escala y la filosofía de migración de la institución. El paisaje open source y comercial incluye [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (amplia biblioteca Python multicategoría con validación en beta), la biblioteca asociada [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") para la iniciación de pagos aguas arriba, [Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (una biblioteca Java exhaustiva Apache 2.0 con una capa comercial para la validación y las traducciones CBPR+), y una serie de plataformas comerciales —Mambu, Kyriba, PaymentComponents y otras— que empaquetan la capacidad ISO 20022 en ofertas más amplias de tesorería o de plataforma de pagos.

El compromiso es familiar. Las plataformas comerciales reducen la carga de ingeniería interna pero atan a la institución a una hoja de ruta de proveedor que puede no corresponder a la suya. Las bibliotecas multicategoría exhaustivas cubren una superficie más amplia pero exigen más trabajo de integración para un tipo de mensaje dado. Las bibliotecas de código abierto focalizadas —pacs008 para la transferencia cliente FI a FI, [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) para la iniciación de pagos— minimizan el tiempo de integración para las instituciones que necesitan abordar rápidamente cuellos de botella específicos, y dejan a la institución dueña de sus propias reglas de validación. Para el problema de dirección estructurada en particular, un enfoque focalizado tiene la ventaja de que las reglas aplicadas son estrechas, bien definidas y poco susceptibles de cambiar antes del cambio.

## Lo que esto significa por sector

El plazo de noviembre de 2026 no afecta a todas las instituciones por igual. La respuesta correcta depende del volumen de tráfico transfronterizo, de la madurez del dominio de datos existente y del papel que desempeña la institución en la cadena de pago.

### Grandes bancos corresponsales y transfronterizos

Para los bancos de primer nivel que operan un tráfico CBPR+ significativo, la exigencia de dirección estructurada es un workstream dentro de un programa de preparación SR2026 mucho más amplio que también cubre excepciones e investigaciones, endurecimiento BAH y (en Estados Unidos) la migración simultánea de Fedwire y CHIPS. Los datos de RedCompass Labs sugieren que la mayoría de estas instituciones gastan entre 20 y 30 millones de dólares en la preparación 2026, con equipos de entrega de 10 a 20 especialistas. El riesgo para este grupo no es la capacidad técnica, es la capacidad de entrega. Con varios workstreams paralelos disputándose las mismas ventanas de release, la remediación de calidad de dirección puede deslizarse silenciosamente por detrás de workstreams más visibles hasta convertirse en un problema de semana de cambio. El paliativo práctico es subir la validación de dirección más arriba en el pipeline, para que los fallos emerjan en entornos de desarrollo y prueba meses antes de haber alcanzado la producción.

### Bancos de tamaño medio e instituciones de pago

Para los bancos de tamaño medio y las instituciones EMI/PI, la exigencia de dirección estructurada es a menudo la obligación 2026 más material que afrontan, porque no llevan la misma carga de workstreams concomitantes que los bancos de primer nivel. El desafío aquí es habitualmente la calidad de datos aguas arriba. Los procesos de onboarding de cliente que han capturado direcciones en texto libre durante décadas producen dominios de datos maestros que no son inmediatamente parseables. La remediación automatizada —utilizando el modelo de estructuración de dirección open source de SWIFT, servicios comerciales de limpieza de dirección o una combinación— puede abordar una parte sustancial de los registros, pero una larga cola residual de direcciones internacionales complejas requerirá una revisión manual. Cuanto antes empiece ese trabajo, más pequeña se vuelve esa cola.

### Corporativos y proveedores de servicios de pago

Los corporativos que inician pagos vía pain.001 están aguas arriba de la generación de pacs.008 por el banco pero no están exentos de la exigencia de dirección estructurada. Los bancos no rellenarán retroactivamente las direcciones de beneficiario en nombre de los clientes corporativos; los datos estructurados deben provenir de los sistemas propios del corporativo. Para los tesoreros de empresa, esto significa asegurar que los sistemas ERP y de tesorería capturen las direcciones de beneficiario en forma estructurada, que la información de signatario y deudor último también esté estructurada, y que las plantillas de iniciación de pago no abandonen silenciosamente campos al generar el archivo. La validación previa al vuelo de los archivos pain.001 —utilizando bien las herramientas propias del corporativo, bien servicios expuestos por el banco— se convierte en el punto de control práctico.

### Proveedores, fintechs e integradores

Para los proveedores que construyen sobre los rails de pago, el plazo es una función de forzamiento para la capacidad ISO 20022 que podría haberse aplazado a fases posteriores. Las fintechs que enrutan o inician pagos transfronterizos a través de socios bancarios deben subir la captura de dirección estructurada a sus propias UI y API, o aceptar que los archivos pain.001 conformes no puedan producirse a partir de sus datos. La oportunidad, para los proveedores capaces de moverse rápido, es absorber la carga de remediación en nombre de los clientes corporativos: transformar un problema de cumplimiento en servicio.

## Conclusión

El plazo de dirección estructurada de noviembre de 2026 es, en cierto sentido, un cambio estrecho: dos campos obligatorios, algunos recomendados, y la retirada de una opción en texto libre que nunca debería haberse utilizado para datos relevantes para el cribado de sanciones en primer lugar. En otro sentido, es el hito ISO 20022 más significativo operacionalmente desde la migración CBPR+ original, porque fuerza el dato estructurado no solo en la capa de mensaje sino en los sistemas aguas arriba que la alimentan.

El cuadro de preparación a nivel de sector, a seis meses del plazo, no es alentador. Dos tercios de los mensajes CBPR+ siguen llevando direcciones no estructuradas. Casi la mitad de los bancos no van por buen camino. Cerca de un tercio de los registros de dirección de cliente siguen siendo no parseables. La financiación está en su sitio —las encuestas muestran constantemente inversiones de ocho y nueve cifras— pero el trabajo no, y la dimensión de calidad de datos del problema no puede resolverse solo con gasto en los últimos meses.

Lo que ayuda ahora es la automatización en el punto de validación: empujar las reglas a pipelines que intercepten los problemas antes de que alcancen la red, en lugar de después. Para las instituciones que operan bases Python o FastAPI, las herramientas open source como [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") proporcionan una manera práctica de operar ese cambio sin ciclo de selección de proveedor. Para todos los demás, independientemente del stack, el punto estratégico es el mismo: las instituciones que industrialicen el cambio ahora estarán en una posición mucho más fuerte que las que se apoyen en un cumplimiento de última hora, por tomar prestada la formulación de las investigaciones de RedCompass Labs que ha enmarcado gran parte de la conversación 2026.

El fin de semana de cambio en noviembre cerrará un capítulo. Las instituciones que lleguen a él con datos limpios, validación automatizada y comprensión operativa de lo que las direcciones estructuradas hacen realmente para el cribado de sanciones pasarán ese fin de semana vigilando el tráfico. Las que lleguen sin esas cosas lo pasarán al teléfono.

## Preguntas frecuentes

**¿Qué cambia exactamente el plazo de noviembre de 2026?**

A partir de mediados de noviembre de 2026, SWIFT CBPR+ rechazará los mensajes pacs.008, pacs.009, pacs.004 y pacs.003 cuyos campos de parte contengan únicamente direcciones postales no estructuradas. La exigencia estructurada mínima es el nombre de ciudad en el elemento TwnNm y el país en el elemento Ctry (utilizando el código ISO 3166-1 alpha-2). Las direcciones híbridas siguen permitidas —ciudad y país en campos estructurados, más hasta dos elementos AdrLine en texto libre para los componentes restantes— pero el mismo componente no puede figurar a la vez en los campos estructurados y no estructurados. Las direcciones totalmente estructuradas son el formato preferido. El European Payments Council ha alineado los esquemas SEPA (SCT, SDD, SCT Inst) con la misma fecha de cambio.

**¿Qué mensajes y qué campos de parte están afectados?**

Para pacs.008, la exigencia se aplica a las direcciones postales del deudor y del acreedor. Para pacs.009, se aplica a las direcciones de institución en las transferencias FI y los pagos de cobertura. Para pacs.004, se aplica a las direcciones de parte en las devoluciones de pago. Para pacs.003, se aplica a las direcciones de acreedor y deudor en los adeudos directos de clientes. Los mensajes de extracto y notificación (camt.052, camt.053, camt.054) y algunos mensajes administrativos quedan fuera de la exigencia estricta. Los mensajes pain.001 aguas arriba de los clientes corporativos no se rigen directamente por CBPR+, pero las direcciones no estructuradas en los archivos pain.001 bloquearán la generación conforme de pacs.008 aguas abajo y están, por tanto, efectivamente en el alcance.

**¿Cuál es la diferencia entre dirección estructurada, híbrida y no estructurada?**

Una dirección totalmente estructurada mapea cada componente a su elemento ISO 20022 dedicado: StrtNm, BldgNb o PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. Una dirección híbrida tiene el nombre de ciudad y el país en campos estructurados, el resto de la dirección en hasta dos elementos AdrLine en texto libre; el mismo componente no debe figurar en los dos. Una dirección no estructurada tiene la dirección postal entera en elementos AdrLine sin TwnNm ni Ctry estructurados; es el formato retirado en noviembre de 2026 para los campos de parte afectados.

**¿Cómo ayuda pacs008.com en esta transición?**

La biblioteca [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") valida los campos de dirección postal estructurados e híbridos antes de la generación XML, marca los datos no estructurados que fallarían tras el plazo, soporta los formatos híbridos preplazo y totalmente estructurados posplazo, y se integra en los pipelines CI y workflows de validación por lote. Genera XML para las 13 versiones de pacs.008 soportadas, valida contra los esquemas XSD oficiales ISO 20022, y expone un servicio FastAPI para la orquestación automatizada. Es open source bajo licencia de tipo MIT, está disponible en PyPI y se ha diseñado específicamente para los workflows de transferencia cliente FI a FI; las reglas de validación están, por tanto, calibradas sobre las directrices de uso SWIFT CBPR+ SR2026 en lugar de abstraídas sobre numerosos tipos de mensajes.

**¿Qué ocurre si mi institución no está lista en noviembre de 2026?**

Los mensajes con direcciones no estructuradas en los campos de parte afectados serán rechazados a nivel de red tras el cambio. En la práctica, esto se traduce en fallos de pago, volúmenes de excepción mayores, oleadas de reparación manual e impacto probable en el cliente. El servicio de traducción en vuelo de SWIFT está disponible para algunos casos transitorios pero sufre recargos a partir de enero de 2026 y no puede parsear de manera fiable todos los formatos de dirección. SWIFT también ha publicado un modelo de IA de código abierto de estructuración de dirección que infiere ciudad y país a partir de datos heredados no estructurados, pero está diseñado para la remediación y el preprocesamiento, no como sustituto permanente de los datos limpios aguas arriba. Las instituciones que lleguen al plazo sin un dominio de datos maestros remediado y un pipeline de validación automatizado deberían esperar una semana de cambio difícil y una subida operativa significativa en los meses siguientes.

## Referencias

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
