---
title: "El prazo pacs.008 de «direção estructurada» de noviembre de 2026: vista a seis meses"
subtitle: "A mediados de noviembre de 2026, SWIFT CBPR+ rechazará as direções postales no estructuradas em os mensajes pacs.008 e mensajes de pagamento transfronteiriços asociados."
description: "A mediados de noviembre de 2026, SWIFT CBPR+ rechazará as direções postales no estructuradas em os mensajes pacs.008 e mensajes asociados. Con perto do 65 % de mensajes ainda no conformes e o 44 % de os bancos atrasados, a ventana de remediación se cierra mais rápido de lo que a maioria de os programas de preparación estão diseñados para gestionar."
date: "May 12, 2026"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "Esquema de um mensaje de pagamento transfronteiriço com direção estructurada, com TwnNm e Ctry resaltados"
keywords: "ISO 20022, pacs.008, pacs.009, pacs.004, pacs.003, pain.001, CBPR+, SWIFT, SR2026, direção estructurada, SEPA, EPC, pagamentos transfronteiriços, cribado de sanciones, pacs008"
---

A partir de mediados de noviembre de 2026, SWIFT CBPR+ rechazará as direções postales no estructuradas em os mensajes pacs.008 e mensajes de pagamento transfronteiriços asociados. Con perto do 65 % de os mensajes ainda no conformes e o 44 % de os bancos atrasados, a ventana de remediación se cierra mais rápido de lo que a maioria de os programas de preparación estão diseñados para gestionar.

---

> **TL;DR.** La regla SR2026 obliga a estructurar ao menos o nombre de a cidade e o país em pacs.008, pacs.009, pacs.004 e pacs.003 desde mediados de noviembre de 2026. La preparación do sector é desigual e a ventana de remediación se cierra rapidamente; os pipelines automatizados de validação são hoje o palanca prática clave.
>
> **Principais Conclusões**
>
> - A partir de **noviembre de 2026**, SWIFT CBPR+ dejará de aceptar direções postales no estructuradas em os mensajes de pagamento transfronteiriços. El cambio se aplica a **pacs.008** (transferencia cliente), **pacs.009** (transferencia interbancaria), **pacs.004** (devoluciones) e **pacs.003** (adeudos directos), assim como a os flujos **pain.001** aguas acima que os alimentan.
> - Como mínimo, o **nombre de a cidade (TwnNm)** e o **país (Ctry)** devem estar presentes em campos estructurados dedicados. El **nombre de a calle (StrtNm)** e bien o **número de edificio (BldgNb)**, bien o **apartado de correos (PstBx)**, são altamente recomendados. Las linhas de direção em texto libre (AdrLine) por sim solas ya no satisfarán a exigencia para os campos de partes clave.
> - El cambio mejora a precisión do cribado de sanciones, reduce as tasas de reparación manual e protege o straight-through processing, mas solo para as instituciones que têm remediado seus dados de cliente aguas acima, no solo seus motores de mensajes.
> - La preparación industrial é desigual. En marzo de 2026, em torno do **65 % de os mensajes CBPR+ seguem llevando direções no estructuradas**, o **44 % de os bancos** no van por buen camino para o prazo, e o **32 % de os registros de direção de cliente** seguem siendo no estructurados de media.
> - Herramientas de código aberto, incluída **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, uma biblioteca Python e um serviço FastAPI para generar, validar e orquestar os flujos de mensajes pacs.008, podem comprimir os prazos de remediación automatizando a validação de esquema, os controles de qualidade de direção e a aplicação em o nivel CI antes de que os mensajes alcancen a red SWIFT.

---

## Um prazo que sempre esteve em camino

La exigencia de direção estructurada de noviembre de 2026 no é um golpe normativo repentino. Figura em a folha de ruta SWIFT CBPR+ desde ou anuncio inicial de a migración [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html), e segue ao fin de a cohabitación MT/MX de noviembre de 2025. Lo que mudou em 2026 é a proximidad. Con perto de seis meses restantes, o sector opera ya dentro de a ventana em a que os problemas de qualidade de dados no resueltos se convierten em um riesgo operativo.

Las cifras cuentan a historia com claridad. La actualización comunitaria de SWIFT de marzo de 2026 señala que [em torno do 65 % de os mensajes de pago ainda contienen direções no estructuradas ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), e que a adoção segue siendo desigual entre geografías e tipos de instituciones. Una [encuesta de RedCompass Labs de marzo de 2026 entre 308 profesionales sénior de pagos ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022") constató que o 44 % de os bancos no estão atualmente por buen camino para cumplir o prazo de direção estructurada, apesar de haver gastado de media 20 millones de dólares —e em as mayores instituciones mais de 30 millones— em a preparación 2026, com uma media de 13 colaboradores adicionales asignados a os programas ISO 20022. La mesma encuesta constató que o 32 % de os registros de direção de cliente seguem siendo no estructurados de media, e que o 60 % de os bancos señalan carencias em os sistemas core banking a a hora de soportar os campos de direção estructurada.

No é, por tanto, um problema que pueda resolverse com um mes mais de trabalho sobre ou motor de mensajes. Es um problema de qualidade de dados que asciende desde a capa de mensaje rumo a os sistemas de onboarding, os procesos KYC, os canales corporativos e décadas de dados maestros de cliente em texto libre acumulados.

## Lo que a regla exige realmente

Bajo a SWIFT CBPR+ Standards Release 2026 (SR2026), a exigencia clave é simple em principio e implacable em o detalle. A partir de mediados de noviembre de 2026, [o nombre de a cidade e o país devem proporcionarse em seus campos estructurados dedicados ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed") para todos os agentes e partes em os mensajes de pago CBPR+, com excepciones muito limitadas (extractos e notificações em camt.052, camt.053, camt.054, mais algunos mensajes administrativos quedan fora de a exigencia estricta). Para os agentes, o uso continuado do BIC por sim solo segue siendo uma alternativa válida a name-and-address.

Dos formatos de direção quedan autorizados tras o cambio:

- **Totalmente estructurado**: cada componente de a direção postal se mapea a seu elemento ISO 20022 dedicado: StrtNm (nombre de calle), BldgNb (número de edificio) ou BldgNm (nombre de edificio), PstCd (código postal), TwnNm (nombre de cidade), CtrySubDvsn (subdivisión país), Ctry (país, em código ISO 3166-1 alpha-2). Es o formato que SWIFT identifica explícitamente como a opção mais deseable quando é posible.
- **Híbrido**: o nombre de cidade e o país se rellenan em seus campos estructurados, enquanto que o resto de a direção pode utilizar hasta dois elementos AdrLine no estructurados. Importante: [os elementos estructurados no devem repetirse dentro de as linhas no estructuradas ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); para um componente dado, a direção é uno u otro.

Las direções totalmente no estructuradas —onde a direção completa se encontra em elementos AdrLine sem TwnNm ni Ctry— no se aceptarán para ninguno de os campos de parte afectados. El European Payments Council tem alineado seu rulebook SEPA com o mesmo cambio, pelo que [a partir do 15 de noviembre de 2026 o formato no estructurado também queda prohibido em SCT, SDD e SCT Inst ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). La alineación é deliberada: SWIFT e o EPC têm diseñado um fin de semana único de bascula industrial.

Para despejar cualquier ambigüedad, a [documentación de pacs008 enumera directamente os mensajes afectados ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (deudor e acreedor em as transferencias cliente), pacs.009 (direções de institución em as transferencias FI e os pagos de cobertura), pacs.004 (direções de parte em as devoluciones) e pacs.003 (adeudos directos). La exigencia asciende também aguas acima: os arquivos pain.001 corporativos que lleven direções no estructuradas bloquearán a geração conforme de pacs.008 em o banco receptor.

## Por que o sector lo tem convertido em uma prioridad

El argumento a favor de as direções estructuradas no é estético. Es operativo, e se manifiesta em três lugares.

**Cribado de sanciones.** El beneficio prático mais importante é que as direções estructuradas permitem a os sistemas de cribado separar o nombre de parte de os dados de localización. Los bloques de direção em texto libre causan regularmente falsos positivos quando um nombre de cidade solapa com um token de nombre de persona sancionada, ou quando um país enterrado em o texto libre se passa totalmente por alto. Los campos estructurados permitem a os motores de cribado aplicar reglas de riesgo específicas de país de maneira determinista, e fazem posible a aplicação do matching de lista de sanciones contra ou código de país em vez de adivinar sobre uma cadena parseada. El análisis de CGI UK publicado em marzo de 2026 subraya este ponto explícitamente: [os dados de direção estructurados se vuelven centrales para a resiliencia operativa, e no simplesmente uma obligación de cumplimiento ⧉](https://www.cgi.com/uk/em-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Tasas de reparación manual.** Los pagamentos transfronteiriços actuales llevan um coste operativo significativo em forma de investigaciones manuales, gestión de excepciones e colas de reparación, em grande parte motivado por direções que os sistemas de cribado ou de enrutamiento no podem parsear com confiança. Los bancos que ya têm passado a as direções estructuradas reportan reducciones materiales de excepciones STP, em particular em os flujos de mitad de corredor onde os agentes intermediarios antes debían interpretar dados em texto libre que no tinham generado.

**Aplicación a nivel de red.** SR2026 endurece a validação a nivel de a red SWIFT. Algunos de os novos controles operarán inicialmente em modo no bloqueante —señalando problemas de qualidade de dados sem detener os pagos— mas a trayectoria é clara, e tras o cambio, [os mensajes no conformes serão rechazados de maneira pura e simple ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Varios rails de pago estadounidenses (Fedwire, CHIPS) e SWIFT CBPR+ convergen esencialmente em o mesmo calendario, lo que elimina a opção de um cambio escalonado que algunas instituciones tinham supuesto em planes anteriores.

## La vista por campo: lo que cambia em o mensaje

El mensaje pacs.008 admite direções estructuradas desde que as primeiras directrices de uso CBPR+ entraron em vigor em marzo de 2023. Lo que cambia em noviembre de 2026 no é o esquema, é a validação. Hasta agora, os bancos puderam poblar os elementos AdrLine com texto libre e hacerlo passar por a red. A partir do prazo, os contenidos de os bloques de parte devem satisfacer os requisitos mínimos de campos estructurados.

### Requerido, recomendado e retirado

| Elemento | XPath (sob `PstlAdr`) | Estado tras nov. 2026 | Notas |
|---|---|---|---|
| Nombre de cidade | `<TwnNm>` | **Obligatorio** | Al menos um nombre de cidade estructurado por parte afectada |
| País | `<Ctry>` | **Obligatorio** | Código ISO 3166-1 alpha-2 |
| Nombre de calle | `<StrtNm>` | Altamente recomendado | Requerido para o formato totalmente estructurado |
| Número de edificio | `<BldgNb>` | Recomendado | O BldgNb, ou PstBx, no ambos |
| Apartado de correos | `<PstBx>` | Recomendado | Alternativa a BldgNb |
| Código postal | `<PstCd>` | Recomendado | Requerido por algunos esquemas locales |
| Subdivisión país | `<CtrySubDvsn>` | Opcional | Estado, región, provincia |
| Línea de direção (texto libre) | `<AdrLine>` | **Restringido** | Máx. 2 linhas em híbrido; nunca junto ao mesmo componente em os campos estructurados |
| Tipo de direção | `<AdrTp>` | Opcional | Uso de `ADDR` recomendado para as direções postales |

*Fuente: síntesis de as directrices de uso SWIFT CBPR+ para SR2026 e de a [documentación de direção estructurada pacs008.com ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008").*

La implicación prática é que toda institución que ainda se apoye em AdrLine em solitario —ya sea em seu própria geração de mensaje, em os arquivos pain.001 recibidos de clientes corporativos, ou em os registros de dados maestros utilizados para enriquecer os pagos em flujo— deve migrar esses dados a os campos estructurados antes do cambio. El serviço de traducción em vuelo de SWIFT pode ayudar em tránsito, mas [sufre recargos a partir de enero de 2026 ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB") e no pode parsear de maneira fiable todos os formatos de direção. SWIFT também tem publicado [um modelo de IA de código aberto de estructuración de direção ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model") entrenado com dados de mais de 200 países para inferir cidade e país a partir de dados heredados no estructurados com puntuaciones de confiança, mas é explícitamente uma ayuda a a remediación, no um sustituto a longo prazo de os dados limpios aguas acima.

## Cómo pacs008.com ayuda a comprimir o calendario

Para as instituciones que precisam industrializar seus pipelines de qualidade de direção e validação de mensajes rapidamente, [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") proporciona uma caja de ferramentas de código aberto sob licencia MIT e um serviço FastAPI diseñados específicamente para o workflow de transferencia cliente FI a FI. Aborda as três capas em as que os programas de remediación se estancan com mais frecuencia: validação de dados, geração XML e aplicação por pipeline.

Las capacidades de direção estructurada de a caja de ferramentas estão alineadas a os requisitos SR2026:

- **Validación pregeneración** de os campos de direção postal estructurados e híbridos, para que os dados no conformes sean interceptados antes de que se produzca ou envíe XML alguno.
- **Marcado de os dados de direção no estructurados** que fallarían tras o prazo de noviembre de 2026, com uma distinción clara entre casos aceptables em híbrido e casos totalmente no estructurados.
- **Soporte doble formato** para os formatos híbridos preplazo e as configuraciones totalmente estructuradas posplazo, permitiendo a as instituciones migrar progresivamente sem romper a interoperabilidade com as contrapartes que ainda no têm completado seus próprias transiciones.
- **Integración em pipeline CI** para que os controles de qualidade de direção formen parte do proceso de build, e no um afterthought ao final do flujo: a resposta prática a a observación de CGI conforme a cual [a gobernanza de os dados deve ser um principio de diseño fundamental ⧉](https://www.cgi.com/uk/em-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement") em vez de uma sobrecapa de cumplimiento.

Más allá de as direções, a caja de ferramentas cubre a superficie mais amplia de validação que a versión SR2026 endurece: validação JSON Schema contra 20 esquemas específicos de mensaje, verificação de formato IBAN e checksum em 75 países, validação XSD do XML generado contra os esquemas oficiales ISO 20022, e geração version-aware através do conjunto de as 13 revisiones de pacs.008 soportadas (pacs.008.001.01 a pacs.008.001.13). Para os equipes operativos e de cumplimiento, inclui também a prevención de XXE mediante defusedxml, a protección estricta contra ou path traversal e o enmascaramiento de PII em os registros JSON estructurados para soportar as exigencias de RGPD e PCI DSS, o tipo de controles no negociables em os flujos de pago em producción mas frequentemente añadidos tardíamente em as migraciones lideradas por proveedor.

La biblioteca está disponible [em PyPI ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") em forma de paquete `pip install pacs008` e em [GitHub ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") com transparencia total do código-fonte. Para as instituciones que evalúan seus opções, esto importa: as ferramentas de código aberto permitem a os equipes internos auditar a lógica de validação, integrarla em bases Python ou FastAPI existentes sem negociaciones de licencia, e aportar parches à medida que aparezcan seus próprios casos límite.

Vale a pena ser preciso sobre ou alcance. pacs008 é uma caja de ferramentas de capa de mensaje; no reemplaza um motor de pagos, um sistema de cribado ou a remediación de os dados maestros de cliente que uma institución ainda deve fazer em a fuente. Lo que faz é tomar esse trabalho de remediación e hacerlo aplicable: convertir o cumplimiento de direção estructurada de uma revisión manual ao final de uma cadena larga em uma puerta automatizada em o ponto de geração. Para os programas com poco tempo, essa puerta marca a diferença entre um cambio limpio e uma ola de rechazos poscambio.

## El panorama de as ferramentas

pacs008 se inscribe em um ecosistema mais amplio de ferramentas de mensajes ISO 20022, e a elección do enfoque depende do stack, a escala e a filosofía de migración de a institución. El paisaje open source e comercial inclui [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (amplia biblioteca Python multicategoría com validação em beta), a biblioteca asociada [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") para a iniciación de pagos aguas acima, [Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (uma biblioteca Java exhaustiva Apache 2.0 com uma capa comercial para a validação e as traducciones CBPR+), e uma serie de plataformas comerciales —Mambu, Kyriba, PaymentComponents e otras— que empaquetan a capacidade ISO 20022 em ofertas mais amplias de tesorería ou de plataforma de pagos.

El compromiso é familiar. Las plataformas comerciales reducen a carga de ingeniería interna mas atan a a institución a uma folha de ruta de proveedor que pode no corresponder a a suya. Las bibliotecas multicategoría exhaustivas cubren uma superficie mais amplia mas exigen mais trabalho de integração para um tipo de mensaje dado. Las bibliotecas de código aberto focalizadas —pacs008 para a transferencia cliente FI a FI, [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) para a iniciación de pagos— minimizan o tempo de integração para as instituciones que precisam abordar rapidamente cuellos de botella específicos, e dejan a a institución dueña de seus próprias reglas de validação. Para o problema de direção estructurada em particular, um enfoque focalizado tem a ventaja de que as reglas aplicadas são estrechas, bien definidas e poco susceptibles de cambiar antes do cambio.

## Lo que esto significa por sector

El prazo de noviembre de 2026 no afecta a todas as instituciones por igual. La resposta correcta depende do volumen de tráfico transfronteiriço, de a madurez do dominio de dados existente e do papel que desempeña a institución em a cadena de pago.

### Grandes bancos corresponsales e transfronteiriços

Para os bancos de primer nivel que operan um tráfico CBPR+ significativo, a exigencia de direção estructurada é um workstream dentro de um programa de preparación SR2026 muito mais amplio que também cubre excepciones e investigaciones, endurecimiento BAH e (em Estados Unidos) a migración simultánea de Fedwire e CHIPS. Los dados de RedCompass Labs sugieren que a maioria de estas instituciones gastan entre 20 e 30 millones de dólares em a preparación 2026, com equipes de entrega de 10 a 20 especialistas. El riesgo para este grupo no é a capacidade técnica, é a capacidade de entrega. Con vários workstreams paralelos disputándose as mesmas ventanas de release, a remediación de qualidade de direção pode deslizarse silenciosamente por atrás de workstreams mais visibles hasta convertirse em um problema de semana de cambio. El paliativo prático é subir a validação de direção mais acima em o pipeline, para que os fallos emerjan em entornos de desenvolvimento e prueba meses antes de haver alcançado a producción.

### Bancos de tamaño meio e instituciones de pago

Para os bancos de tamaño meio e as instituciones EMI/PI, a exigencia de direção estructurada é frequentemente a obligación 2026 mais material que afrontan, porque no llevan a mesma carga de workstreams concomitantes que os bancos de primer nivel. El desafío aqui é habitualmente a qualidade de dados aguas acima. Los procesos de onboarding de cliente que têm capturado direções em texto libre durante décadas producen dominios de dados maestros que no são inmediatamente parseables. La remediación automatizada —utilizando o modelo de estructuración de direção open source de SWIFT, serviços comerciales de limpieza de direção ou uma combinación— pode abordar uma parte sustancial de os registros, mas uma larga cola residual de direções internacionales complejas requerirá uma revisión manual. Cuanto antes empiece esse trabalho, mais pequeña se vuelve essa cola.

### Corporativos e proveedores de serviços de pago

Los corporativos que inician pagos vía pain.001 estão aguas acima de a geração de pacs.008 por o banco mas no estão exentos de a exigencia de direção estructurada. Los bancos no rellenarán retroactivamente as direções de beneficiario em nombre de os clientes corporativos; os dados estructurados devem provenir de os sistemas próprios do corporativo. Para os tesoreros de empresa, esto significa asegurar que os sistemas ERP e de tesorería capturen as direções de beneficiario em forma estructurada, que a informação de signatario e deudor último também esté estructurada, e que as plantillas de iniciación de pago no abandonen silenciosamente campos ao generar o arquivo. La validação previa ao vuelo de os arquivos pain.001 —utilizando bien as ferramentas próprias do corporativo, bien serviços expuestos por o banco— se convierte em o ponto de control prático.

### Proveedores, fintechs e integradores

Para os proveedores que construyen sobre os rails de pago, o prazo é uma función de forzamiento para a capacidade ISO 20022 que poderia haberse aplazado a fases posteriores. Las fintechs que enrutan ou inician pagamentos transfronteiriços através de socios bancários devem subir a captura de direção estructurada a seus próprias UI e API, ou aceptar que os arquivos pain.001 conformes no puedan producirse a partir de seus dados. La oportunidade, para os proveedores capaces de moverse rápido, é absorber a carga de remediación em nombre de os clientes corporativos: transformar um problema de cumplimiento em serviço.

## Conclusión

El prazo de direção estructurada de noviembre de 2026 é, em cierto sentido, um cambio estrecho: dois campos obligatorios, algunos recomendados, e a retirada de uma opção em texto libre que nunca deveria haberse utilizado para dados relevantes para o cribado de sanciones em primer lugar. En otro sentido, é o hito ISO 20022 mais significativo operacionalmente desde a migración CBPR+ original, porque fuerza o dado estructurado no solo em a capa de mensaje mas sim em os sistemas aguas acima que a alimentan.

El cuadro de preparación a nivel de sector, a seis meses do prazo, no é alentador. Dos tercios de os mensajes CBPR+ seguem llevando direções no estructuradas. Casi a mitad de os bancos no van por buen camino. Cerca de um tercio de os registros de direção de cliente seguem siendo no parseables. La financiación está em seu sitio —as encuestas mostram constantemente investimentos de oito e nove cifras— mas o trabalho no, e a dimensão de qualidade de dados do problema no pode resolverse solo com gasto em os últimos meses.

Lo que ayuda agora é a automação em o ponto de validação: empujar as reglas a pipelines que intercepten os problemas antes de que alcancen a red, em vez de depois. Para as instituciones que operan bases Python ou FastAPI, as ferramentas open source como [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") proporcionan uma maneira prática de operar esse cambio sem ciclo de selección de proveedor. Para todos os demás, independientemente do stack, o ponto estratégico é o mesmo: as instituciones que industrialicen o cambio agora estarán em uma posição muito mais fuerte que as que se apoyen em um cumplimiento de última hora, por tomar prestada a formulación de as investigaciones de RedCompass Labs que tem enmarcado grande parte de a conversación 2026.

El fin de semana de cambio em noviembre cerrará um capítulo. Las instituciones que lleguen a ele com dados limpios, validação automatizada e comprensión operativa de lo que as direções estructuradas fazem realmente para o cribado de sanciones pasarán esse fin de semana vigilando o tráfico. Las que lleguen sem essas cosas lo pasarán ao telefone.

## Preguntas frecuentes

**Qué cambia exactamente o prazo de noviembre de 2026?**

A partir de mediados de noviembre de 2026, SWIFT CBPR+ rechazará os mensajes pacs.008, pacs.009, pacs.004 e pacs.003 cuyos campos de parte contengan unicamente direções postales no estructuradas. La exigencia estructurada mínima é o nombre de cidade em o elemento TwnNm e o país em o elemento Ctry (utilizando o código ISO 3166-1 alpha-2). Las direções híbridas seguem permitidas —cidade e país em campos estructurados, mais hasta dois elementos AdrLine em texto libre para os componentes restantes— mas o mesmo componente no pode figurar a a vez em os campos estructurados e no estructurados. Las direções totalmente estructuradas são o formato preferido. El European Payments Council tem alineado os esquemas SEPA (SCT, SDD, SCT Inst) com a mesma fecha de cambio.

**Qué mensajes e que campos de parte estão afectados?**

Para pacs.008, a exigencia se aplica a as direções postales do deudor e do acreedor. Para pacs.009, se aplica a as direções de institución em as transferencias FI e os pagos de cobertura. Para pacs.004, se aplica a as direções de parte em as devoluciones de pago. Para pacs.003, se aplica a as direções de acreedor e deudor em os adeudos directos de clientes. Los mensajes de extracto e notificação (camt.052, camt.053, camt.054) e algunos mensajes administrativos quedan fora de a exigencia estricta. Los mensajes pain.001 aguas acima de os clientes corporativos no se rigen directamente por CBPR+, mas as direções no estructuradas em os arquivos pain.001 bloquearán a geração conforme de pacs.008 aguas abaixo e estão, por tanto, efetivamente em o alcance.

**Cuál é a diferença entre direção estructurada, híbrida e no estructurada?**

Una direção totalmente estructurada mapea cada componente a seu elemento ISO 20022 dedicado: StrtNm, BldgNb ou PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. Una direção híbrida tem o nombre de cidade e o país em campos estructurados, o resto de a direção em hasta dois elementos AdrLine em texto libre; o mesmo componente no deve figurar em os dois. Una direção no estructurada tem a direção postal entera em elementos AdrLine sem TwnNm ni Ctry estructurados; é o formato retirado em noviembre de 2026 para os campos de parte afectados.

**Cómo ayuda pacs008.com em esta transición?**

La biblioteca [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") valida os campos de direção postal estructurados e híbridos antes de a geração XML, marca os dados no estructurados que fallarían tras o prazo, soporta os formatos híbridos preplazo e totalmente estructurados posplazo, e se integra em os pipelines CI e workflows de validação por lote. Genera XML para as 13 versiones de pacs.008 soportadas, valida contra os esquemas XSD oficiales ISO 20022, e expone um serviço FastAPI para a orquestación automatizada. Es open source sob licencia de tipo MIT, está disponible em PyPI e tem-se diseñado específicamente para os workflows de transferencia cliente FI a FI; as reglas de validação estão, por tanto, calibradas sobre as directrices de uso SWIFT CBPR+ SR2026 em vez de abstraídas sobre numerosos tipos de mensajes.

**Qué ocurre si meu institución no está lista em noviembre de 2026?**

Los mensajes com direções no estructuradas em os campos de parte afectados serão rechazados a nivel de red tras o cambio. En a prática, esto se traduce em fallos de pago, volúmenes de excepción mayores, oleadas de reparación manual e impacto probable em o cliente. El serviço de traducción em vuelo de SWIFT está disponible para algunos casos transitorios mas sufre recargos a partir de enero de 2026 e no pode parsear de maneira fiable todos os formatos de direção. SWIFT também tem publicado um modelo de IA de código aberto de estructuración de direção que infiere cidade e país a partir de dados heredados no estructurados, mas está diseñado para a remediación e o preprocesamiento, no como sustituto permanente de os dados limpios aguas acima. Las instituciones que lleguen ao prazo sem um dominio de dados maestros remediado e um pipeline de validação automatizado deveriam esperar uma semana de cambio difícil e uma subida operativa significativa em os meses seguintes.

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
- CGI UK, (2026). [2026: A defining year for ISO 20022 and structured data enforcement ⧉](https://www.cgi.com/uk/em-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"). CGI UK.
- J.P. Morgan, (2026). [ISO 20022 Migration: Guidance, Messaging & More ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration "ISO 20022 Migration: Guidance, Messaging & More"). J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022 "FAQ Swift ISO 20022 — ING"). ING Wholesale Banking.
- Mambu, (2026). [CBPR+ is live: what ISO 20022 means in practice ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice "CBPR+ is live: what ISO 20022 means in practice"). Mambu.
- Kyriba, (2026). [ISO 20022 migration: what every treasury team needs to know about what's next ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/ "ISO 20022 migration: what every treasury team needs to know about what's next"). Kyriba.
- Standard Chartered, (2025). [ISO 20022 – Standard Chartered Address Guidelines (H2H and API) ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf "Standard Chartered ISO 20022 Address Guidelines"). Standard Chartered.
- State Street, (2025). [Client Guide to ISO 20022 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"). State Street.
- ISO 20022, (2026). [Message Definitions Catalogue ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 Message Definitions"). ISO 20022.
