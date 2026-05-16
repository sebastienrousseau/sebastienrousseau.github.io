---
title: "ISO 20022 pacs.008: de deadline voor gestructureerde adressen"
subtitle: "Vanaf november 2026 weigert SWIFT CBPR+ ongestructureerde postadressen"
description: "Vanaf november 2026 weigert SWIFT CBPR+ ongestructureerde postadressen in grensoverschrijdende betaalberichten. Wat dit betekent voor banken."
date: "May 12, 2026"
language: "nl-NL"
locale: "nl_NL"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "Visualisatie van een gestructureerd pacs.008-betaalbericht"
keywords: "ISO 20022, pacs.008, SWIFT, CBPR+, gestructureerd adres, grensoverschrijdend"
---
Ab Mitte November 2026 wordt SWIFT CBPR+ unstrukturierte Postanschriften in pacs.008 en zugehörigen grensoverschrijdende betaalberichten zurückweisen. Mit ongeveer 65 % de berichten nog niet conform en 44 % de banken in Rückstand schließt sich het Sanooitrungsfenster sneler, als de meisten Vorbereitungsprogramme darauf ausgelegd zijn.

---

> **Wesentliche inzichten**
>
> - Ab **November 2026** akzeptiert SWIFT CBPR+ keine unstrukturierten Postanschriften meer in grensoverschrijdende betaalberichten. De Änderung gilt voor **pacs.008** (klantenzahlung), **pacs.009** (FI-betaling), **pacs.004** (Rückgaben) en **pacs.003** (Lastschriften) sowie voor de vorgelagerten **pain.001**-Flüsse, de ze speisen.
> - Mindestens moeten **Town Name (TwnNm)** en **Country (Ctry)** in dedizierten strukturierten Feldern vorhanden zijn. **Street Name (StrtNm)** sowie ofwel **Building Number (BldgNb)** of **PO Box (PstBx)** worden nachdrücklich empfohlen. Freitext-Adresszeilen (AdrLine) allein erfüllen de Anforderung voor de maßgeblichen Parteifelder niet meer.
> - De Änderung erhöht de Treffsicherheit bij Sanktionsscreening, senkt manuelle Nacharbeit en schützt de Straight-Through-Processing-Rate – echter alleen voor Institute, de haar vorgelagerten klantendaten sanooitrt hebben, niet alleen haar berichten-Engines.
> - De Vorbereitung in de sector is ungleichmäßig. stand maart 2026 enthouden ongeveer **65 % de CBPR+-berichten** nog steeds unstrukturierte Adressen, **44 % de banken** liegen niet in plan, en in Durchschnitt zijn **32 % de klantenadressdaten** nog unstrukturiert.
> - open source-tools – darunter **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, een Python-bibliotheek en een FastAPI-dienst tot Erzeugung, Validierung en Orchestrierung van pacs.008-berichtenflüssen – kunnen Sanooitrungszeiträume verkürzen, doordat ze Schema-Validierung, Adressqualitätsprüfungen en CI-seitige Durchsetzung automatisieren, bevor berichten het SWIFT-netwerk erreichen.

---

## Een Frist, de altijd bevorstand

De Anforderung strukturierter Adressen ab November 2026 is kein plötzlicher regelgevender Vorstoß. U steht seit de ursprünglichen Ankündigung de [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-migratie op de SWIFT-CBPR+-routekaart en folgt de einde de MT/MX-Koexistenz in November 2025. Was sich 2026 geändert heeft, is de Nähe. Mit verbleibenden ongeveer sechs maanden operiert de sector nun innerhalb des Fensters, in de ungeontketente Datenqualitätsprobleme tot operationellen risico worden.

De Zahlen erzählen de geschiedenis unmissvpasändlich. De eigen Community-Update van SWIFT vom maart 2026 hält fest, dat [ongeveer 65 % de betaalberichten nog steeds unstrukturierte Adressen enthouden ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), en dat de adoptie over Regionen en Institutstypen hinweg uneinheitlich bleibt. Een [RedCompass-Labs-Umfrage vom maart 2026 onder 308 Senior-Payments-Verantwortlichen ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of banks Are Behind on ISO 20022") ergab, dat 44 % de banken de Frist voor strukturierte Adressen momenteel niet planmäßig erreichen, obwohl ze in Schnitt 20 miljoenen US-Dollar – en in de größten Häusern over 30 miljoenen – voor de 2026er-Bereitschaft ausgegeben en in Schnitt 13 zusätzliche Mitarbeitende voor ISO-20022-Programme abgestelt hebben. Dieselbe Umfrage stelte fest, dat in Durchschnitt 32 % de klantenadressdaten unstrukturiert bleiben en dat 60 % de banken Lücken in de Kernbankensystemen bij de Untpasützung strukturierter Adressfelder berichten.

Es is somit kein probleem, het sich door een weiteren maand Arbeit aan de berichten-Engine lösen lässt. Es is een Datenqualitätsproblem, het uit de berichtenebene hinauf in Onboarding-systeeme, KYC-procese, Firmenkanäle en jahrzehnteoude Freitext-Stammdaten reicht.

## Was de Regel tatsächlich verlangt

Unter de SWIFT-CBPR+-standaards-Release 2026 (SR2026) is de Kernanforderung in Gongeveersatz schlicht en in Detail unerbittlich. Ab Mitte November 2026 [moeten Town Name en Country in haar daarvoor vorgesehenen strukturierten Feldern angegeben worden ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), en zwar voor sämtliche Agenten en Parteien in CBPR+-betaalberichten – met zeer begrenzten Ausnahmen (Auszüge en Benachrichtigungen in camt.052, camt.053, camt.054 sowie einige administrative berichten bleiben außerhalb de strikten Anforderung). Für Agenten bleibt de fortgezete Verwendung des BIC allein een gültige Alternative tot „Name en Adresse".

Nach de Umstellung zijn zwei Adressformate zulässig:

- **Vollvoortdurend strukturiert** – iedere voorraadteil de Postanschrift wordt op zijn dediziertes ISO-20022-Element abgevormt: StrtNm (Straßenname), BldgNb (Hausnummer) of BldgNm (Gebäudename), PstCd (Postleitzahl), TwnNm (Ortsname), CtrySubDvsn (Verwoudungsuntereinheit), Ctry (land, als ISO-3166-1-alpha-2-Code). Dies is het Format, het SWIFT ausdrücklich als de na mogelijkheid tot bevorzugende Option benennt.
- **Hybrid** – Ortsname en land worden in haar strukturierten Feldern gepflegt, terwijl de Rest de Adresse bis tot zwei unstrukturierte AdrLine-Elemente benutten darf. Wichtig: [strukturierte Elemente dürfen niet innerhalb de unstrukturierten Zeilen wiederholt worden ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); voor iedere voorraadteil is de Adresse ofwel het een of het andere.

Vollvoortdurend unstrukturierte Adressen – bij denen de gesamte Adresse in AdrLine-Elementen zonder TwnNm of Ctry steht – worden voor keines de betroffenen Parteifelder akzeptiert. Het European Payments Council heeft zijn SEPA-Rulebook op denselben Umstellungstermin abgestimmt, sodass [ab de 15. November 2026 het unstrukturierte Format ook in SCT, SDD en SCT Inst untersagt is ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). De Abstimmung is beabsichtigt: SWIFT en het EPC hebben een einheitliches industrieweites Umstellungswochenende konzipiert.

Um Missvpasändnisse auszuschließen, listet de [pacs008-Dokumentation de betroffenen berichten direkt op ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (Debitor en Kreditor bij klantenzahlungen), pacs.009 (Institutsadressen bij FI-betalingen en Cover-betalingen), pacs.004 (Parteiadressen bij Rückgaben) en pacs.003 (Lastschriften). De Anforderung wirkt bovendien na vorn: Firmen-pain.001-Dateien met unstrukturierten Adressen blockieren de conforme pacs.008-Erzeugung bij de empfangenden bank.

## Warum de sector dies tot Priorität gemacht heeft

De Begründung voor strukturierte Adressen is niet ästhetisch. U is operativ en toont sich aan drei Stellen.

**Sanktionsscreening.** De belangrijkste praktische Nutzen is, dat strukturierte Adressen es Screening-systeemen erlauben, Parteinamen van Ortsdaten tot trennen. Freitext-Adressblöcke verursachen regelmäßig Fehlalarme, indien een Ortsname zufällig met een Namens-Token een sanktionooitrten persoon überlappt of een in Freitext eingebettetes land vollvoortdurend übersehen wordt. Strukturierte Felder erlauben es Screening-Engines, länderspezifische risicoregeln deterministisch anzuwenden, en mogelijk maken een Abgleich tegen de landencode statt tegen een geparste Zeichenkette. De in maart 2026 veröffentlichte CGI-UK-Analyse betont deze Punkt ausdrücklich: [Strukturierte Adressdaten worden centraal voor de operationelle Resilienz en niet alleen tot een Compliance-Pflicht ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Manuelle Nachbearbeitungsquoten.** Grenzüberschreitende betalingen tragen heute erhebliche operative kosten in Form manueller Untersuchungen, Ausnahmebearbeitung en Reparaturwarteschlangen – vielfach gedreven van Adressen, de Screening- of Routing-systeeme niet betrouwbaar parsen kunnen. banken, de reeds op strukturierte Adressen umgestelt hebben, berichten van spürbaren Reduktionen de STP-Ausnahmen, insbesondere in Mid-Corridor-Strömen, in denen zwischengeschoudete Agenten zuvor Freitextdaten interpretieren moesten, de ze niet selbst erzeugt hadden.

**Durchsetzung op netwerkebene.** SR2026 verschärft de Validierung op SWIFT-netwerkebene. Einige de nieuwen Prüfungen worden aanvankelijk in niet blockierenden Modus laufen – ze kennzeichnen Datenqualitätsprobleme, zonder betalingen anzuhouden –, toch de Stoßrichtung is eindeutig, en na de Umstellung worden [niet conforme berichten zonder Weiteres zurückgewiesen ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Mehrere US-betalingsschienen (Fedwire, CHIPS) en SWIFT CBPR+ konvergieren op in Wesentlichen denselben tijdpad, was de in früheren planungen einkalkulierte Option een gestaffelten Umstellung entfallen lässt.

## De Feldsicht: Was sich in de bericht ändert

De pacs.008-bericht untpasützt strukturierte Adressen seit de Inkrafttreten de pasen CBPR+-Usage-Guidelines in maart 2023. Was sich in November 2026 ändert, is niet het Schema, sondern de Validierung. Bisher durften banken AdrLine-Elemente met Freitext füllen en door het netwerk leiten. Ab de Frist moeten de Inhoude de Parteiblöcke de Mindestanforderungen aan strukturierte Felder erfüllen.

### Pflicht, aanbeveling en Ausmusterung

| Element | XPath (onder `PstlAdr`) | status na Nov. 2026 | Hinweise |
|---|---|---|---|
| Town Name | `<TwnNm>` | **Pflicht** | Mindestens een strukturierter Town Name je betroffener Partei |
| Country | `<Ctry>` | **Pflicht** | ISO-3166-1-alpha-2-Code |
| Street Name | `<StrtNm>` | Nachdrücklich empfohlen | Pflicht voor vollvoortdurend strukturiertes Format |
| Building Number | `<BldgNb>` | Empfohlen | Entnoch BldgNb of PstBx, niet beide |
| PO Box | `<PstBx>` | Empfohlen | Alternative tot BldgNb |
| Post Code | `<PstCd>` | Empfohlen | In manchen lokalen Schemata Pflicht |
| Country Subdivision | `<CtrySubDvsn>` | Optional | Bundesstaat, Region, Provinz |
| Address Line (Freitext) | `<AdrLine>` | **Eingeschränkt** | Max. 2 Zeilen in Hybridformat; nooitmals neben demselben voorraadteil in strukturierten Feldern |
| Address Type | `<AdrTp>` | Optional | Verwendung van `ADDR` voor Postanschriften empfohlen |

*Quelle: Synthese de SWIFT-CBPR+-Usage-Guidelines voor SR2026 en de [Dokumentation strukturierter Adressen op pacs008.com ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008").*

De praktische gevolg is, dat ieder Institut, het nog steeds allein op AdrLine zet – sei es bij de eigenn berichtenerzeugung, in pain.001-Dateien van Firmenklanten of in Stammdaten tot Anreicherung laufender betalingen –, deze Daten vóór de Umstellung in strukturierte Felder migrieren moet. De SWIFT-In-Flow-Translation-dienst kan terwijl de Übertragung helfen, [zieht echter ab januari 2026 Zusatzgebühren na sich ⧉](https://www.pcbb.com/products/internationaal-banking/internationaal-payments/iso20022-faq "ISO 20022 FAQ — PCBB") en kan niet ieder Adressformat betrouwbaar parsen. SWIFT heeft bovendien [een quelloffenes AI-model tot Adressstrukturierung ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model") veröffentlicht, trainooitrt op Daten uit over 200 landenn, um stad en land met Konfidenzwerten uit unstrukturierten Altdaten abzuleiten – es is echter ausdrücklich een Sanooitrungshilfe en kein duurzaamer Ersatz voor saubere vorgelagerte Daten.

## Wie pacs008.com hilft, de tijdpad tot verdichten

Für Institute, de haar Pipelines tot Adressqualität en berichtenvalidierung snel industrialisieren moeten, stelt [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") een quelloffenes Toolkit onder MIT-Lizenz en een FastAPI-dienst bereit, de speziell op de FI-tot-FI-klantenzahlungs-Workflow zugeschnitten zijn. Es adressiert de drei Schichten, aan denen Sanooitrungsprogramme am vaaksten ins Stocken geraten: Datenvalidierung, XML-Erzeugung en Pipeline-Durchsetzung.

De Strukturierte-Adresse-Funktionen des Toolkits zijn op de SR2026-Anforderungen abgestimmt:

- **Vorab-Validierung** strukturierter en hybrider Postadressfelder, sodass niet conforme Daten erfasst worden, bevor XML erzeugt of versendet wordt.
- **Kennzeichnung unstrukturierter Adressdaten**, de na de Frist in November 2026 scheitern würden, met duidelijker Unterscheidung tussen in Hybrid akzeptablen en vollvoortdurend unstrukturierten Fällen.
- **Dual-Format-Untpasützung** zowel voor hybride Formate vóór de Frist als voor vollvoortdurend strukturierte Layouts na de Frist, sodass Institute schrittweise migrieren kunnen, zonder de Interoperabilität met Gegenparteien tot brechen, de haar eigenn Übergang nog niet abgeschlossen hebben.
- **CI-Pipeline-Integration**, daarmee Adressqualitätsprüfungen Teil des Build-proceses worden en niet pas am einde des Flusses nachgeholt worden – de praktische antwoord op de [CGI-Beobachtung, dat Datengovernance een gongeveerleggendes Designprinzip ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement") en kein Compliance-Aufsatz zijn moet.

Über Adressen uit deckt het Toolkit de breitere Validierungsfläche ab, de het SR2026-Release verschärft: JSON-Schema-Validierung tegen 20 nachrichtenspezifische Schemata, IBAN-Format- en Prüfziffernkontrolle voor 75 landen, XSD-Validierung des erzeugten XML tegen de offiziellen ISO-20022-Schemata sowie versionsbewusste Erzeugung over alle 13 untpasützten pacs.008-Revisionen (pacs.008.001.01 bis pacs.008.001.13). Für Betrieb en Compliance enthält es bovendien XXE-bescherming via defusedxml, strikten bescherming tegen Path-Traversal en PII-Maskierung in strukturierten JSON-Logs tot Untpasützung de Anforderungen uit AVG en PCI DSS – de Art van controlen, de in produktiven betalingsflüssen niet verhandelbar zijn, in hpasellergeführten migratieen echter vaak spät nachgerüstet worden.

De bibliotheek is [op PyPI ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") als `pip install pacs008`-Paket en op [GitHub ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") met vollvoortdurender Quelltexttransparenz verfügbar. Für Institute, de haar Optionen abwägen, is het relevant: open source-tools erlauben es internen Teams, de Validierungslogik tot auditieren, ze zonder Lizenzverhandlungen in vorhandene Python- of FastAPI-landschaften tot integrieren en Korrekturen beizutragen, sobald eigen Sonderfälle auftreten.

Es lohnt sich, bij Umfang präzise tot zijn. pacs008 is een Toolkit op berichtenebene; es erzet nog een Payments-Engine nog een Screening-systeem en ook niet de Sanooitrung de klantenstammdaten, de een Institut aan de Quelle leisten moet. Was es leistet, is, deze Sanooitrungsarbeit durchsetzbar tot machen – de naleving strukturierter Adressen wordt vom manuellen Review am einde een langen Pipeline tot automatisierten Gate am Erzeugungspunkt. Für zeitlich knappe Programme is dit Gate de Unterschied tussen een sauberen Umstellung en een Welle van Ablehnungen daarna.

## De toollandschaft

pacs008 fügt sich in een breiteres Ökosystem van ISO-20022-berichtenwerkzeugen een, en de Wahl des aanpakes hängt van Stack, grootte en migratiesphilosophie des Instituts ab. De open source- en kommerzielle landschaft umfasst [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — aan ISO 20022 message generator and parser") (umfangreiche Mehrkategorien-Python-bibliotheek met Beta-Validierung), de zugehörige bibliotheek [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") voor de vorgelagerte betalingsinitiierung, [Prowide ISO 20022 ⧉](https://www.prowidesvaakware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (een umfassende Apache-2.0-Java-bibliotheek met kommerzieller Schicht voor CBPR+-Validierung en -Übersetzungen) sowie een Reihe kommerzieller platformen – Mambu, Kyriba, PaymentComponents en andere –, de ISO-20022-Funktionalität in umfassendere treasury- of Payments-platform-Angebote bündeln.

De Abwägungsraum is vertraut. Kommerzielle platformen verringern de interne Engineering-Last, binden het Institut maar aan een aanbieders-routekaart, de womogelijk niet tot eigenn passt. Umfassende Mehrkategorien-bibliotheken decken een größere Fläche ab, vereisen echter meer Integrationsaufwand voor een einzelnen berichtentyp. Fokussierte open-source-bibliotheken – pacs008 voor FI-tot-FI-klantenzahlungen, [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) voor de betalingsinitiierung – minimieren de Integrationszeit voor Institute, de gezielte knelpunten rasch adressieren moeten, en belassen de Hoheit over de eigenn Validierungsregeln bij Institut. Für het spezifische probleem strukturierter Adressen heeft de fokussierte aanpak de Vorzug, dat de durchgezeten Regeln eng, präzise definooitrt en unwahrscheinlich vóór de Umstellung tot ändern zijn.

## Was het je sector bedeutet

De Frist in November 2026 betrifft niet alle Institute gleichermaßen. De richtige Reaktion hängt vom volume des grensoverschrijdende Verkehrs, vom rijpheidgrad de bestaanden Datenlandschaft en van de Rolle ab, de het Institut in de betalingskette einnimmt.

### Große Korrespondenz- en grensoverschrijdende banken

Für Tier-1-banken met signifikantem CBPR+-Verkehr is de Strukturierte-Adresse-Anforderung een Arbeitsstrom innerhalb een veel größeren SR2026-Bereitschaftsprogramms, het ook Ausnahmen en Untersuchungen, BAH-Härtung sowie (in de USA) de parallele migratie van Fedwire en CHIPS umfasst. De RedCompass-Labs-Daten leggen nahe, dat de meisten deze Institute 20 bis 30 miljoenen US-Dollar voor de 2026er-Bereitschaft aufwenden, met Lieferteams van 10 bis 20 Spezialisten. Het risico voor deze groep is niet de technische Fähigkeit, sondern de Lieferkapazität. Wenn mehrere parallele Arbeitsströme um dieselben Release-Fenster konkurrieren, kan de Adressqualitätssanooitrung lautlos hinter sichtbarere Arbeitsströme zurückfallen, bis ze tot probleem de Umstellungswoche wordt. De praktische Gegenmaßnahme bestaat darin, de Adressvalidierung in de Pipeline vorzuverlagern, daarmee Fehlschläge in ontwikkelings- en Testumgebungen maande vóór Erreichen de production sichtbar worden.

### Mittelständische banken en betalingsinstitute

Für mittelständische banken sowie EMI/PI-Institute is de Anforderung strukturierter Adressen vaak de materiell belangrijkste 2026er-Pflicht, omdat ze niet de gleichen Begleitlasten zoals de Tier-1-Häuser tragen. De uitdaging liegt hier meist in de vorgelagerten Datenqualität. klanten-Onboarding-procese, de Adressen jahrzehntelang als Freitext erfasst hebben, erzeugen Stammdatenbestände, de sich niet zonder Weiteres parsen lassen. Automatisierte Sanooitrung – met de quelloffenen Adressstrukturierungsmodell van SWIFT, kommerziellen Adressbereinigungsdiensten of een Kombination – kan een erheblichen Anteil de Datensätze adressieren, toch een langer Rest komplexer internationaaler Adressen wordt manuelle Prüfung vereisen. Je früher deze Arbeit beginnt, desto kürzer wordt deze Rest.

### ondernemingen en betalingsdienstleister

ondernemingen, de betalingen via pain.001 initiieren, liegen vóór de pacs.008-Erzeugung de bank, zijn echter niet van de Anforderung strukturierter Adressen ausgenommen. banken worden Begünstigtenadressen niet rückwirkend in Namen haar Firmenklanten befüllen; de strukturierten Daten moeten uit de systeemen des ondernemingens selbst stammen. Für Corporate Treasurer bedeutet het, sicherzustellen, dat ERP- en treasury-systeeme Begünstigtenadressen strukturiert erfassen, dat Daten tot Unterzeichnern en ultimativen Debitoren eveneens strukturiert vorliegen en dat betalingsinitiierungsvorlagen terwijl de Dateierzeugung niet stillschweigend Felder verlieren. Een Vorflug-Validierung van pain.001-Dateien – met eigenm tool des ondernemingens of van de bank bereitgestelten diensts – wordt tot praktischen controlepunt.

### aanbieders, FinTechs en systeemintegratoren

Für aanbieders, de op betalingsschienen aufbouwen, is de Frist een Zwangsfunktion voor ISO-20022-Fähigkeiten, de womogelijk in spätere Phasen verschoben worden waren. FinTechs, de grensoverschrijdende betalingen over bankpartner leiten of initiieren, moeten de Erfassung strukturierter Adressen in haar eigenn UIs en APIs sichtbar machen – of akzeptieren, dat uit haar Daten keine conformen pain.001-Dateien erzeugt worden kunnen. Für aanbieders, de sich snel bewegen kunnen, liegt de Chance darin, de Sanooitrungslast voor Firmenklanten tot absorbieren – een Compliance-probleem in een dienst tot verwandeln.

## Fazit

De Frist voor strukturierte Adressen in November 2026 is einerseits een enge Änderung: zwei Pflichtfelder, einige aanbevelingen en de Ausmusterung een Freitext-Option, de van vorneherein niet voor sanktionsrelevante Daten hätte gebenut worden dürfen. Andererseits is ze de operativ bedeutsamste ISO-20022-Meilenstein seit de ursprünglichen CBPR+-migratie, omdat ze strukturierte Daten niet alleen in de berichtenebene, sondern in de vorgelagerten systeeme zwingt, de ze speisen.

Het Bereitschaftsbild op sectornebene is sechs maande vóór de Frist niet ermutigend. Zwei Drittel de CBPR+-berichten enthouden nog steeds unstrukturierte Adressen. Nahezu de Hälfte de banken liegt niet in plan. Fast een Drittel de klantenadressdaten bleibt niet parsebar. De Mittel stehen bereit – de Umfragen tonen konstant achts- en nieuwnstellige investeringen –, de Arbeit echter niet, en de Datenqualitätsdimension lässt sich in de letzten maanden niet allein door Ausgaben lösen.

Was jetzt hilft, is Automatisierung am Validierungspunkt: de Regeln in Pipelines tot drücken, de probleeme abfangen, bevor ze het netwerk erreichen, statt daarna. Für Institute met Python- of FastAPI-landschaften biedt open source-tool zoals [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") een pragmatischen Weg, deze Wechsel zonder aanbiedersauswahlzyklus tot vollziehen. Für alle, onafhankelijk vom Stack, gilt derselbe strategische Punkt: Institute, de de Wandel jetzt industrialisieren, worden weit beter dastehen als jene, de op Last-minuut-Compliance zetten – um de Formulierung de RedCompass-Labs-onderzoek aufzugrijpen, de een Großteil de 2026er-Debatte geprägt heeft.

Het Umstellungswochenende in November schließt een Kapitel. De Institute, de met sauberen Daten, automatisierter Validierung en een belastbaren Vpasändnis daarvoor eintreffen, was strukturierte Adressen voor het Sanktionsscreening leisten, worden dit weeknende met Verkehrsbeobachtung verbringen. Diejenigen, de zonder deze Voraussetzungen ankommen, worden es am Telefon verbringen.

## Veelgestelde vragen

**Was ändert sich nauwkeurig tot Frist in November 2026?**

Ab Mitte November 2026 weist SWIFT CBPR+ pacs.008-, pacs.009-, pacs.004- en pacs.003-berichten zurück, deren Parteifelder ausuiteindelijk unstrukturierte Postanschriften enthouden. De strukturierte Mindestanforderung is de Ortsname in TwnNm-Element en het land in Ctry-Element (in ISO-3166-1-alpha-2-Code). Hybridadressen bleiben zulässig – stad en land in strukturierten Feldern plus bis tot zwei Freitext-AdrLine-Elemente voor de übrigen voorraadteile –, maar derselbe voorraadteil darf niet zowel in strukturierten als in unstrukturierten Feldern verschijnen. Vollvoortdurend strukturierte Adressen zijn het bevorzugte Format. Het European Payments Council heeft de SEPA-Schemata (SCT, SDD, SCT Inst) op dasselbe Umstellungsdatum abgestimmt.

**Welche berichten en welche Parteifelder zijn betroffen?**

Für pacs.008 gilt de Anforderung voor de Postanschriften van Debitor en Kreditor. Für pacs.009 gilt ze voor Institutsadressen bij FI-betalingen en Cover-betalingen. Für pacs.004 gilt ze voor Parteiadressen in betalingsrückgaben. Für pacs.003 gilt ze voor Gläubiger- en schuldneradressen bij klantenlastschriften. Auszugs- en Benachrichtigungsmeldungen (camt.052, camt.053, camt.054) sowie bestimmte administrative berichten bleiben außerhalb de strikten Anforderung. Vorgelagerte pain.001-berichten van Firmenklanten unterliegen CBPR+ niet direkt, maar unstrukturierte Adressen in pain.001-Dateien blockieren de conforme pacs.008-Erzeugung in Anschluss en liegen daarmee faktisch in Umfang.

**Worin unterscheiden sich strukturierte, hybride en unstrukturierte Adressen?**

Een vollvoortdurend strukturierte Adresse vormt iedere voorraadteil op zijn dediziertes ISO-20022-Element ab: StrtNm, BldgNb of PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. Een hybride Adresse heeft Town Name en Country in strukturierten Feldern, de Rest de Adresse steht in bis tot zwei Freitext-AdrLine-Elementen; derselbe voorraadteil darf niet in beiden vorkommen. Een unstrukturierte Adresse enthält de gesamte Postanschrift in AdrLine-Elementen zonder strukturiertes TwnNm of Ctry – dies is het Format, het in November 2026 voor de betroffenen Parteifelder ausgemustert wordt.

**Wie hilft pacs008.com bij deze Übergang?**

De bibliotheek [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") gevalideerd strukturierte en hybride Postadressfelder vóór de XML-Erzeugung, kennzeichnet unstrukturierte Daten, de na de Frist scheitern würden, untpasützt zowel hybride Formate vóór de Frist als vollvoortdurend strukturierte Layouts daarna en integriert sich in CI-Pipelines en Batch-Validierungs-Workflows. U erzeugt XML voor alle 13 untpasützten pacs.008-Versionen, gevalideerd tegen de offiziellen ISO-20022-XSD-Schemata en stelt een FastAPI-dienst tot automatisierten Orchestrierung bereit. U is open source onder een MIT-vergelijkbaaren Lizenz, op PyPI verfügbar en speziell voor FI-tot-FI-klantenzahlungs-Workflows konzipiert – de Validierungsregeln zijn daarom op de SR2026-CBPR+-Usage-Guidelines kalibriert en niet over veel berichtentypen hinweg abstrahiert.

**Was passiert, indien mein Institut bis November 2026 niet bereit is?**

berichten met unstrukturierten Adressen in de betroffenen Parteifeldern worden na de Umstellung op netwerkebene zurückgewiesen. In de praktijk bedeutet het betalingsabwicklungsfehler, hogere Ausnahmevolumina, Wellen manueller Nacharbeit en voraussichtliche klantenwirkung. De SWIFT-In-Flow-Translation-dienst is voor einige Übergangsfälle verfügbar, zieht echter ab januari 2026 Zusatzgebühren na sich en kan niet ieder Adressformat betrouwbaar parsen. SWIFT heeft bovendien een quelloffenes AI-model tot Adressstrukturierung veröffentlicht, het stad en land uit unstrukturierten Altdaten ableitet, maar voor Sanooitrung en Vorverarbeitung konzipiert is en kein duurzaamer Ersatz voor saubere vorgelagerte Daten. Institute, de de Frist zonder sanooitrten klantenstammdatenbestand en zonder automatisierte Validierungs-Pipeline erreichen, moeten met een schwierigen Umstellungswoche en een duidelijken operativen Mehraufwand in de gevolgmonaten rechnen.

## Quellen

- Sebastien Rousseau, (2023). [Automating ISO 20022-Compliant Payment File Creation with Pain001](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html "Automating ISO 20022-Compliant Payment File Creation with Pain001").
- pacs008, (2026). [November 2026 structured-address deadline ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"). pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 Toolkit and API ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"). pacs008.com.
- SWIFT, (2026). [ISO 20022 milestone for November 2026: Unstructured addresses to be removed ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"). SWIFT.
- SWIFT, (2026). [ISO 20022 for Financial Institutions ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions "ISO 20022 for Financial Institutions"). SWIFT.
- SWIFT, (2026). [The Swift AI address structuring model ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"). SWIFT.
- RedCompass Labs, (2026). [Nearly Half of banks Are Behind on ISO 20022 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of banks Are Behind on ISO 20022"). Financial IT.
- RedCompass Labs, (2026). [ISO 20022 is arriving all at once for US banks ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). RedCompass Labs.
- ClearingPost, (2026). [The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline"). ClearingPost.
- CGI UK, (2026). [2026: A defining year for ISO 20022 and structured data enforcement ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"). CGI UK.
- J.P. Morgan, (2026). [ISO 20022 migratie: Guidance, Messaging & More ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration "ISO 20022 migratie: Guidance, Messaging & More"). J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022 "FAQ Swift ISO 20022 — ING"). ING Wholesale banking.
- Mambu, (2026). [CBPR+ is live: what ISO 20022 means in practice ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice "CBPR+ is live: what ISO 20022 means in practice"). Mambu.
- Kyriba, (2026). [ISO 20022 migration: what every treasury team needs to know about what's next ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/ "ISO 20022 migration: what every treasury team needs to know about what's next"). Kyriba.
- standaard Chartered, (2025). [ISO 20022 – standaard Chartered Address Guidelines (H2H and API) ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf "standaard Chartered ISO 20022 Address Guidelines"). standaard Chartered.
- State Street, (2025). [Client Guide to ISO 20022 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"). State Street.
- ISO 20022, (2026). [Message Definitions Catalogue ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 Message Definitions"). ISO 20022.
