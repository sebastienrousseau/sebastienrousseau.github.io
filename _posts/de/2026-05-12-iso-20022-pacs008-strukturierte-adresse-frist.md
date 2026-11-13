---
title: "Die pacs.008-Frist für strukturierte Adressen im November 2026: ein Blick aus sechs Monaten Distanz"
subtitle: "Ab Mitte November 2026 wird SWIFT CBPR+ unstrukturierte Postanschriften in pacs.008 und zugehörigen grenzüberschreitenden Zahlungsnachrichten zurückweisen."
description: "Ab Mitte November 2026 wird SWIFT CBPR+ unstrukturierte Postanschriften in pacs.008 und zugehörigen Nachrichten zurückweisen. Mit rund 65 % der Nachrichten noch nicht konform und 44 % der Banken im Rückstand schließt sich das Sanierungsfenster schneller, als die meisten Vorbereitungsprogramme darauf ausgelegt sind."
date: "May 12, 2026"
language: "de"
locale: "de_DE"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "Schema einer grenzüberschreitenden Zahlungsnachricht mit strukturierter Adresse, TwnNm und Ctry hervorgehoben"
keywords: "ISO 20022, pacs.008, pacs.009, pacs.004, pacs.003, pain.001, CBPR+, SWIFT, SR2026, strukturierte Adresse, SEPA, EPC, grenzüberschreitende Zahlungen, Sanktionsscreening, pacs008"
---

Ab Mitte November 2026 wird SWIFT CBPR+ unstrukturierte Postanschriften in pacs.008 und zugehörigen grenzüberschreitenden Zahlungsnachrichten zurückweisen. Mit rund 65 % der Nachrichten noch nicht konform und 44 % der Banken im Rückstand schließt sich das Sanierungsfenster schneller, als die meisten Vorbereitungsprogramme darauf ausgelegt sind.

---

> **Wesentliche Erkenntnisse**
>
> - Ab **November 2026** akzeptiert SWIFT CBPR+ keine unstrukturierten Postanschriften mehr in grenzüberschreitenden Zahlungsnachrichten. Die Änderung gilt für **pacs.008** (Kundenzahlung), **pacs.009** (FI-Zahlung), **pacs.004** (Rückgaben) und **pacs.003** (Lastschriften) sowie für die vorgelagerten **pain.001**-Flüsse, die sie speisen.
> - Mindestens müssen **Town Name (TwnNm)** und **Country (Ctry)** in dedizierten strukturierten Feldern vorhanden sein. **Street Name (StrtNm)** sowie entweder **Building Number (BldgNb)** oder **PO Box (PstBx)** werden nachdrücklich empfohlen. Freitext-Adresszeilen (AdrLine) allein erfüllen die Anforderung für die maßgeblichen Parteifelder nicht mehr.
> - Die Änderung erhöht die Treffsicherheit beim Sanktionsscreening, senkt manuelle Nacharbeit und schützt die Straight-Through-Processing-Rate – jedoch nur für Institute, die ihre vorgelagerten Kundendaten saniert haben, nicht nur ihre Nachrichten-Engines.
> - Die Vorbereitung in der Branche ist ungleichmäßig. Stand März 2026 enthalten rund **65 % der CBPR+-Nachrichten** weiterhin unstrukturierte Adressen, **44 % der Banken** liegen nicht im Plan, und im Durchschnitt sind **32 % der Kundenadressdaten** noch unstrukturiert.
> - Open-Source-Werkzeuge – darunter **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, eine Python-Bibliothek und ein FastAPI-Service zur Erzeugung, Validierung und Orchestrierung von pacs.008-Nachrichtenflüssen – können Sanierungszeiträume verkürzen, indem sie Schema-Validierung, Adressqualitätsprüfungen und CI-seitige Durchsetzung automatisieren, bevor Nachrichten das SWIFT-Netzwerk erreichen.

---

## Eine Frist, die immer bevorstand

Die Anforderung strukturierter Adressen ab November 2026 ist kein plötzlicher regulatorischer Vorstoß. Sie steht seit der ursprünglichen Ankündigung der [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-Migration auf der SWIFT-CBPR+-Roadmap und folgt dem Ende der MT/MX-Koexistenz im November 2025. Was sich 2026 geändert hat, ist die Nähe. Mit verbleibenden rund sechs Monaten operiert die Branche nun innerhalb des Fensters, in dem ungelöste Datenqualitätsprobleme zum operationellen Risiko werden.

Die Zahlen erzählen die Geschichte unmissverständlich. Der eigene Community-Update von SWIFT vom März 2026 hält fest, dass [rund 65 % der Zahlungsnachrichten weiterhin unstrukturierte Adressen enthalten ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), und dass die Adoption über Regionen und Institutstypen hinweg uneinheitlich bleibt. Eine [RedCompass-Labs-Umfrage vom März 2026 unter 308 Senior-Payments-Verantwortlichen ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022") ergab, dass 44 % der Banken die Frist für strukturierte Adressen derzeit nicht planmäßig erreichen, obwohl sie im Schnitt 20 Millionen US-Dollar – und in den größten Häusern über 30 Millionen – für die 2026er-Bereitschaft ausgegeben und im Schnitt 13 zusätzliche Mitarbeitende für ISO-20022-Programme abgestellt haben. Dieselbe Umfrage stellte fest, dass im Durchschnitt 32 % der Kundenadressdaten unstrukturiert bleiben und dass 60 % der Banken Lücken in den Kernbankensystemen bei der Unterstützung strukturierter Adressfelder berichten.

Es ist somit kein Problem, das sich durch einen weiteren Monat Arbeit an der Nachrichten-Engine lösen lässt. Es ist ein Datenqualitätsproblem, das aus der Nachrichtenebene hinauf in Onboarding-Systeme, KYC-Prozesse, Firmenkanäle und jahrzehntealte Freitext-Stammdaten reicht.

## Was die Regel tatsächlich verlangt

Unter dem SWIFT-CBPR+-Standards-Release 2026 (SR2026) ist die Kernanforderung im Grundsatz schlicht und im Detail unerbittlich. Ab Mitte November 2026 [müssen Town Name und Country in ihren dafür vorgesehenen strukturierten Feldern angegeben werden ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), und zwar für sämtliche Agenten und Parteien in CBPR+-Zahlungsnachrichten – mit sehr begrenzten Ausnahmen (Auszüge und Benachrichtigungen in camt.052, camt.053, camt.054 sowie einige administrative Nachrichten bleiben außerhalb der strikten Anforderung). Für Agenten bleibt die fortgesetzte Verwendung des BIC allein eine gültige Alternative zu „Name und Adresse".

Nach der Umstellung sind zwei Adressformate zulässig:

- **Vollständig strukturiert** – jeder Bestandteil der Postanschrift wird auf sein dediziertes ISO-20022-Element abgebildet: StrtNm (Straßenname), BldgNb (Hausnummer) oder BldgNm (Gebäudename), PstCd (Postleitzahl), TwnNm (Ortsname), CtrySubDvsn (Verwaltungsuntereinheit), Ctry (Land, als ISO-3166-1-alpha-2-Code). Dies ist das Format, das SWIFT ausdrücklich als die nach Möglichkeit zu bevorzugende Option benennt.
- **Hybrid** – Ortsname und Land werden in ihren strukturierten Feldern gepflegt, während der Rest der Adresse bis zu zwei unstrukturierte AdrLine-Elemente nutzen darf. Wichtig: [strukturierte Elemente dürfen nicht innerhalb der unstrukturierten Zeilen wiederholt werden ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); für jeden Bestandteil ist die Adresse entweder das eine oder das andere.

Vollständig unstrukturierte Adressen – bei denen die gesamte Adresse in AdrLine-Elementen ohne TwnNm oder Ctry steht – werden für keines der betroffenen Parteifelder akzeptiert. Das European Payments Council hat sein SEPA-Rulebook auf denselben Umstellungstermin abgestimmt, sodass [ab dem 15. November 2026 das unstrukturierte Format auch in SCT, SDD und SCT Inst untersagt ist ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). Die Abstimmung ist beabsichtigt: SWIFT und das EPC haben ein einheitliches industrieweites Umstellungswochenende konzipiert.

Um Missverständnisse auszuschließen, listet die [pacs008-Dokumentation die betroffenen Nachrichten direkt auf ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (Debitor und Kreditor bei Kundenzahlungen), pacs.009 (Institutsadressen bei FI-Zahlungen und Cover-Zahlungen), pacs.004 (Parteiadressen bei Rückgaben) und pacs.003 (Lastschriften). Die Anforderung wirkt zudem nach vorn: Firmen-pain.001-Dateien mit unstrukturierten Adressen blockieren die konforme pacs.008-Erzeugung bei der empfangenden Bank.

## Warum die Branche dies zur Priorität gemacht hat

Die Begründung für strukturierte Adressen ist nicht ästhetisch. Sie ist operativ und zeigt sich an drei Stellen.

**Sanktionsscreening.** Der wichtigste praktische Nutzen ist, dass strukturierte Adressen es Screening-Systemen erlauben, Parteinamen von Ortsdaten zu trennen. Freitext-Adressblöcke verursachen regelmäßig Fehlalarme, wenn ein Ortsname zufällig mit einem Namens-Token einer sanktionierten Person überlappt oder ein im Freitext eingebettetes Land vollständig übersehen wird. Strukturierte Felder erlauben es Screening-Engines, länderspezifische Risikoregeln deterministisch anzuwenden, und ermöglichen einen Abgleich gegen den Ländercode statt gegen eine geparste Zeichenkette. Die im März 2026 veröffentlichte CGI-UK-Analyse betont diesen Punkt ausdrücklich: [Strukturierte Adressdaten werden zentral für die operationelle Resilienz und nicht nur zu einer Compliance-Pflicht ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Manuelle Nachbearbeitungsquoten.** Grenzüberschreitende Zahlungen tragen heute erhebliche operative Kosten in Form manueller Untersuchungen, Ausnahmebearbeitung und Reparaturwarteschlangen – vielfach getrieben von Adressen, die Screening- oder Routing-Systeme nicht zuverlässig parsen können. Banken, die bereits auf strukturierte Adressen umgestellt haben, berichten von spürbaren Reduktionen der STP-Ausnahmen, insbesondere in Mid-Corridor-Strömen, in denen zwischengeschaltete Agenten zuvor Freitextdaten interpretieren mussten, die sie nicht selbst erzeugt hatten.

**Durchsetzung auf Netzwerkebene.** SR2026 verschärft die Validierung auf SWIFT-Netzwerkebene. Einige der neuen Prüfungen werden anfänglich im nicht blockierenden Modus laufen – sie kennzeichnen Datenqualitätsprobleme, ohne Zahlungen anzuhalten –, doch die Stoßrichtung ist eindeutig, und nach der Umstellung werden [nicht konforme Nachrichten ohne Weiteres zurückgewiesen ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Mehrere US-Zahlungsschienen (Fedwire, CHIPS) und SWIFT CBPR+ konvergieren auf im Wesentlichen denselben Zeitplan, was die in früheren Planungen einkalkulierte Option einer gestaffelten Umstellung entfallen lässt.

## Die Feldsicht: Was sich in der Nachricht ändert

Die pacs.008-Nachricht unterstützt strukturierte Adressen seit dem Inkrafttreten der ersten CBPR+-Usage-Guidelines im März 2023. Was sich im November 2026 ändert, ist nicht das Schema, sondern die Validierung. Bisher durften Banken AdrLine-Elemente mit Freitext füllen und durch das Netzwerk leiten. Ab der Frist müssen die Inhalte der Parteiblöcke die Mindestanforderungen an strukturierte Felder erfüllen.

### Pflicht, Empfehlung und Ausmusterung

| Element | XPath (unter `PstlAdr`) | Status nach Nov. 2026 | Hinweise |
|---|---|---|---|
| Town Name | `<TwnNm>` | **Pflicht** | Mindestens ein strukturierter Town Name je betroffener Partei |
| Country | `<Ctry>` | **Pflicht** | ISO-3166-1-alpha-2-Code |
| Street Name | `<StrtNm>` | Nachdrücklich empfohlen | Pflicht für vollständig strukturiertes Format |
| Building Number | `<BldgNb>` | Empfohlen | Entweder BldgNb oder PstBx, nicht beide |
| PO Box | `<PstBx>` | Empfohlen | Alternative zu BldgNb |
| Post Code | `<PstCd>` | Empfohlen | In manchen lokalen Schemata Pflicht |
| Country Subdivision | `<CtrySubDvsn>` | Optional | Bundesstaat, Region, Provinz |
| Address Line (Freitext) | `<AdrLine>` | **Eingeschränkt** | Max. 2 Zeilen im Hybridformat; niemals neben demselben Bestandteil in strukturierten Feldern |
| Address Type | `<AdrTp>` | Optional | Verwendung von `ADDR` für Postanschriften empfohlen |

*Quelle: Synthese der SWIFT-CBPR+-Usage-Guidelines für SR2026 und der [Dokumentation strukturierter Adressen auf pacs008.com ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008").*

Die praktische Folge ist, dass jedes Institut, das weiterhin allein auf AdrLine setzt – sei es bei der eigenen Nachrichtenerzeugung, in pain.001-Dateien von Firmenkunden oder in Stammdaten zur Anreicherung laufender Zahlungen –, diese Daten vor der Umstellung in strukturierte Felder migrieren muss. Der SWIFT-In-Flow-Translation-Service kann während der Übertragung helfen, [zieht jedoch ab Januar 2026 Zusatzgebühren nach sich ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB") und kann nicht jedes Adressformat zuverlässig parsen. SWIFT hat zudem [ein quelloffenes KI-Modell zur Adressstrukturierung ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model") veröffentlicht, trainiert auf Daten aus über 200 Ländern, um Stadt und Land mit Konfidenzwerten aus unstrukturierten Altdaten abzuleiten – es ist jedoch ausdrücklich eine Sanierungshilfe und kein dauerhafter Ersatz für saubere vorgelagerte Daten.

## Wie pacs008.com hilft, den Zeitplan zu verdichten

Für Institute, die ihre Pipelines zu Adressqualität und Nachrichtenvalidierung schnell industrialisieren müssen, stellt [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") ein quelloffenes Toolkit unter MIT-Lizenz und einen FastAPI-Service bereit, die speziell auf den FI-zu-FI-Kundenzahlungs-Workflow zugeschnitten sind. Es adressiert die drei Schichten, an denen Sanierungsprogramme am häufigsten ins Stocken geraten: Datenvalidierung, XML-Erzeugung und Pipeline-Durchsetzung.

Die Strukturierte-Adresse-Funktionen des Toolkits sind auf die SR2026-Anforderungen abgestimmt:

- **Vorab-Validierung** strukturierter und hybrider Postadressfelder, sodass nicht konforme Daten erfasst werden, bevor XML erzeugt oder versendet wird.
- **Kennzeichnung unstrukturierter Adressdaten**, die nach der Frist im November 2026 scheitern würden, mit klarer Unterscheidung zwischen im Hybrid akzeptablen und vollständig unstrukturierten Fällen.
- **Dual-Format-Unterstützung** sowohl für hybride Formate vor der Frist als auch für vollständig strukturierte Layouts nach der Frist, sodass Institute schrittweise migrieren können, ohne die Interoperabilität mit Gegenparteien zu brechen, die ihren eigenen Übergang noch nicht abgeschlossen haben.
- **CI-Pipeline-Integration**, damit Adressqualitätsprüfungen Teil des Build-Prozesses werden und nicht erst am Ende des Flusses nachgeholt werden – die praktische Antwort auf die [CGI-Beobachtung, dass Datengovernance ein grundlegendes Designprinzip ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement") und kein Compliance-Aufsatz sein muss.

Über Adressen hinaus deckt das Toolkit die breitere Validierungsfläche ab, die das SR2026-Release verschärft: JSON-Schema-Validierung gegen 20 nachrichtenspezifische Schemata, IBAN-Format- und Prüfziffernkontrolle für 75 Länder, XSD-Validierung des erzeugten XML gegen die offiziellen ISO-20022-Schemata sowie versionsbewusste Erzeugung über alle 13 unterstützten pacs.008-Revisionen (pacs.008.001.01 bis pacs.008.001.13). Für Betrieb und Compliance enthält es zudem XXE-Schutz via defusedxml, strikten Schutz gegen Path-Traversal und PII-Maskierung in strukturierten JSON-Logs zur Unterstützung der Anforderungen aus DSGVO und PCI DSS – die Art von Kontrollen, die in produktiven Zahlungsflüssen nicht verhandelbar sind, in herstellergeführten Migrationen jedoch häufig spät nachgerüstet werden.

Die Bibliothek ist [auf PyPI ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") als `pip install pacs008`-Paket und auf [GitHub ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") mit vollständiger Quelltexttransparenz verfügbar. Für Institute, die ihre Optionen abwägen, ist das relevant: Open-Source-Werkzeuge erlauben es internen Teams, die Validierungslogik zu auditieren, sie ohne Lizenzverhandlungen in vorhandene Python- oder FastAPI-Landschaften zu integrieren und Korrekturen beizutragen, sobald eigene Sonderfälle auftreten.

Es lohnt sich, beim Umfang präzise zu sein. pacs008 ist ein Toolkit auf Nachrichtenebene; es ersetzt weder eine Payments-Engine noch ein Screening-System und auch nicht die Sanierung der Kundenstammdaten, die ein Institut an der Quelle leisten muss. Was es leistet, ist, diese Sanierungsarbeit durchsetzbar zu machen – die Konformität strukturierter Adressen wird vom manuellen Review am Ende einer langen Pipeline zum automatisierten Gate am Erzeugungspunkt. Für zeitlich knappe Programme ist dieses Gate der Unterschied zwischen einer sauberen Umstellung und einer Welle von Ablehnungen danach.

## Die Werkzeuglandschaft

pacs008 fügt sich in ein breiteres Ökosystem von ISO-20022-Nachrichtenwerkzeugen ein, und die Wahl des Ansatzes hängt von Stack, Größe und Migrationsphilosophie des Instituts ab. Die Open-Source- und kommerzielle Landschaft umfasst [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (umfangreiche Mehrkategorien-Python-Bibliothek mit Beta-Validierung), die zugehörige Bibliothek [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") für die vorgelagerte Zahlungsinitiierung, [Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (eine umfassende Apache-2.0-Java-Bibliothek mit kommerzieller Schicht für CBPR+-Validierung und -Übersetzungen) sowie eine Reihe kommerzieller Plattformen – Mambu, Kyriba, PaymentComponents und andere –, die ISO-20022-Funktionalität in umfassendere Treasury- oder Payments-Plattform-Angebote bündeln.

Der Abwägungsraum ist vertraut. Kommerzielle Plattformen verringern die interne Engineering-Last, binden das Institut aber an eine Anbieter-Roadmap, die womöglich nicht zur eigenen passt. Umfassende Mehrkategorien-Bibliotheken decken eine größere Fläche ab, erfordern jedoch mehr Integrationsaufwand für einen einzelnen Nachrichtentyp. Fokussierte Open-Source-Bibliotheken – pacs008 für FI-zu-FI-Kundenzahlungen, [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) für die Zahlungsinitiierung – minimieren die Integrationszeit für Institute, die gezielte Engpässe rasch adressieren müssen, und belassen die Hoheit über die eigenen Validierungsregeln beim Institut. Für das spezifische Problem strukturierter Adressen hat der fokussierte Ansatz den Vorzug, dass die durchgesetzten Regeln eng, präzise definiert und unwahrscheinlich vor der Umstellung zu ändern sind.

## Was das je Sektor bedeutet

Die Frist im November 2026 betrifft nicht alle Institute gleichermaßen. Die richtige Reaktion hängt vom Volumen des grenzüberschreitenden Verkehrs, vom Reifegrad der bestehenden Datenlandschaft und von der Rolle ab, die das Institut in der Zahlungskette einnimmt.

### Große Korrespondenz- und grenzüberschreitende Banken

Für Tier-1-Banken mit signifikantem CBPR+-Verkehr ist die Strukturierte-Adresse-Anforderung ein Arbeitsstrom innerhalb eines viel größeren SR2026-Bereitschaftsprogramms, das auch Ausnahmen und Untersuchungen, BAH-Härtung sowie (in den USA) die parallele Migration von Fedwire und CHIPS umfasst. Die RedCompass-Labs-Daten legen nahe, dass die meisten dieser Institute 20 bis 30 Millionen US-Dollar für die 2026er-Bereitschaft aufwenden, mit Lieferteams von 10 bis 20 Spezialisten. Das Risiko für diese Gruppe ist nicht die technische Fähigkeit, sondern die Lieferkapazität. Wenn mehrere parallele Arbeitsströme um dieselben Release-Fenster konkurrieren, kann die Adressqualitätssanierung lautlos hinter sichtbarere Arbeitsströme zurückfallen, bis sie zum Problem der Umstellungswoche wird. Die praktische Gegenmaßnahme besteht darin, die Adressvalidierung in der Pipeline vorzuverlagern, damit Fehlschläge in Entwicklungs- und Testumgebungen Monate vor Erreichen der Produktion sichtbar werden.

### Mittelständische Banken und Zahlungsinstitute

Für mittelständische Banken sowie EMI/PI-Institute ist die Anforderung strukturierter Adressen häufig die materiell wichtigste 2026er-Pflicht, weil sie nicht die gleichen Begleitlasten wie die Tier-1-Häuser tragen. Die Herausforderung liegt hier meist in der vorgelagerten Datenqualität. Kunden-Onboarding-Prozesse, die Adressen jahrzehntelang als Freitext erfasst haben, erzeugen Stammdatenbestände, die sich nicht ohne Weiteres parsen lassen. Automatisierte Sanierung – mit dem quelloffenen Adressstrukturierungsmodell von SWIFT, kommerziellen Adressbereinigungsdiensten oder einer Kombination – kann einen erheblichen Anteil der Datensätze adressieren, doch ein langer Rest komplexer internationaler Adressen wird manuelle Prüfung erfordern. Je früher diese Arbeit beginnt, desto kürzer wird dieser Rest.

### Unternehmen und Zahlungsdienstleister

Unternehmen, die Zahlungen via pain.001 initiieren, liegen vor der pacs.008-Erzeugung der Bank, sind jedoch nicht von der Anforderung strukturierter Adressen ausgenommen. Banken werden Begünstigtenadressen nicht rückwirkend im Namen ihrer Firmenkunden befüllen; die strukturierten Daten müssen aus den Systemen des Unternehmens selbst stammen. Für Corporate Treasurer bedeutet das, sicherzustellen, dass ERP- und Treasury-Systeme Begünstigtenadressen strukturiert erfassen, dass Daten zu Unterzeichnern und ultimativen Debitoren ebenfalls strukturiert vorliegen und dass Zahlungsinitiierungsvorlagen während der Dateierzeugung nicht stillschweigend Felder verlieren. Eine Vorflug-Validierung von pain.001-Dateien – mit eigenem Werkzeug des Unternehmens oder von der Bank bereitgestellten Services – wird zum praktischen Kontrollpunkt.

### Anbieter, FinTechs und Systemintegratoren

Für Anbieter, die auf Zahlungsschienen aufbauen, ist die Frist eine Zwangsfunktion für ISO-20022-Fähigkeiten, die womöglich in spätere Phasen verschoben worden waren. FinTechs, die grenzüberschreitende Zahlungen über Bankpartner leiten oder initiieren, müssen die Erfassung strukturierter Adressen in ihren eigenen UIs und APIs sichtbar machen – oder akzeptieren, dass aus ihren Daten keine konformen pain.001-Dateien erzeugt werden können. Für Anbieter, die sich schnell bewegen können, liegt die Chance darin, die Sanierungslast für Firmenkunden zu absorbieren – ein Compliance-Problem in einen Service zu verwandeln.

## Fazit

Die Frist für strukturierte Adressen im November 2026 ist einerseits eine enge Änderung: zwei Pflichtfelder, einige Empfehlungen und die Ausmusterung einer Freitext-Option, die von vorneherein nicht für sanktionsrelevante Daten hätte genutzt werden dürfen. Andererseits ist sie der operativ bedeutsamste ISO-20022-Meilenstein seit der ursprünglichen CBPR+-Migration, weil sie strukturierte Daten nicht nur in die Nachrichtenebene, sondern in die vorgelagerten Systeme zwingt, die sie speisen.

Das Bereitschaftsbild auf Branchenebene ist sechs Monate vor der Frist nicht ermutigend. Zwei Drittel der CBPR+-Nachrichten enthalten weiterhin unstrukturierte Adressen. Nahezu die Hälfte der Banken liegt nicht im Plan. Fast ein Drittel der Kundenadressdaten bleibt nicht parsebar. Die Mittel stehen bereit – die Umfragen zeigen konstant achts- und neunstellige Investitionen –, die Arbeit jedoch nicht, und die Datenqualitätsdimension lässt sich in den letzten Monaten nicht allein durch Ausgaben lösen.

Was jetzt hilft, ist Automatisierung am Validierungspunkt: die Regeln in Pipelines zu drücken, die Probleme abfangen, bevor sie das Netzwerk erreichen, statt danach. Für Institute mit Python- oder FastAPI-Landschaften bietet Open-Source-Werkzeug wie [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") einen pragmatischen Weg, diesen Wechsel ohne Anbieterauswahlzyklus zu vollziehen. Für alle, unabhängig vom Stack, gilt derselbe strategische Punkt: Institute, die den Wandel jetzt industrialisieren, werden weit besser dastehen als jene, die auf Last-Minute-Compliance setzen – um die Formulierung der RedCompass-Labs-Forschung aufzugreifen, die einen Großteil der 2026er-Debatte geprägt hat.

Das Umstellungswochenende im November schließt ein Kapitel. Die Institute, die mit sauberen Daten, automatisierter Validierung und einem belastbaren Verständnis dafür eintreffen, was strukturierte Adressen für das Sanktionsscreening leisten, werden dieses Wochenende mit Verkehrsbeobachtung verbringen. Diejenigen, die ohne diese Voraussetzungen ankommen, werden es am Telefon verbringen.

## Häufig gestellte Fragen

**Was ändert sich genau zur Frist im November 2026?**

Ab Mitte November 2026 weist SWIFT CBPR+ pacs.008-, pacs.009-, pacs.004- und pacs.003-Nachrichten zurück, deren Parteifelder ausschließlich unstrukturierte Postanschriften enthalten. Die strukturierte Mindestanforderung ist der Ortsname im TwnNm-Element und das Land im Ctry-Element (im ISO-3166-1-alpha-2-Code). Hybridadressen bleiben zulässig – Stadt und Land in strukturierten Feldern plus bis zu zwei Freitext-AdrLine-Elemente für die übrigen Bestandteile –, aber derselbe Bestandteil darf nicht sowohl in strukturierten als auch in unstrukturierten Feldern erscheinen. Vollständig strukturierte Adressen sind das bevorzugte Format. Das European Payments Council hat die SEPA-Schemata (SCT, SDD, SCT Inst) auf dasselbe Umstellungsdatum abgestimmt.

**Welche Nachrichten und welche Parteifelder sind betroffen?**

Für pacs.008 gilt die Anforderung für die Postanschriften von Debitor und Kreditor. Für pacs.009 gilt sie für Institutsadressen bei FI-Zahlungen und Cover-Zahlungen. Für pacs.004 gilt sie für Parteiadressen in Zahlungsrückgaben. Für pacs.003 gilt sie für Gläubiger- und Schuldneradressen bei Kundenlastschriften. Auszugs- und Benachrichtigungsmeldungen (camt.052, camt.053, camt.054) sowie bestimmte administrative Nachrichten bleiben außerhalb der strikten Anforderung. Vorgelagerte pain.001-Nachrichten von Firmenkunden unterliegen CBPR+ nicht direkt, aber unstrukturierte Adressen in pain.001-Dateien blockieren die konforme pacs.008-Erzeugung im Anschluss und liegen damit faktisch im Umfang.

**Worin unterscheiden sich strukturierte, hybride und unstrukturierte Adressen?**

Eine vollständig strukturierte Adresse bildet jeden Bestandteil auf sein dediziertes ISO-20022-Element ab: StrtNm, BldgNb oder PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. Eine hybride Adresse hat Town Name und Country in strukturierten Feldern, der Rest der Adresse steht in bis zu zwei Freitext-AdrLine-Elementen; derselbe Bestandteil darf nicht in beiden vorkommen. Eine unstrukturierte Adresse enthält die gesamte Postanschrift in AdrLine-Elementen ohne strukturiertes TwnNm oder Ctry – dies ist das Format, das im November 2026 für die betroffenen Parteifelder ausgemustert wird.

**Wie hilft pacs008.com bei diesem Übergang?**

Die Bibliothek [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") validiert strukturierte und hybride Postadressfelder vor der XML-Erzeugung, kennzeichnet unstrukturierte Daten, die nach der Frist scheitern würden, unterstützt sowohl hybride Formate vor der Frist als auch vollständig strukturierte Layouts danach und integriert sich in CI-Pipelines und Batch-Validierungs-Workflows. Sie erzeugt XML für alle 13 unterstützten pacs.008-Versionen, validiert gegen die offiziellen ISO-20022-XSD-Schemata und stellt einen FastAPI-Service zur automatisierten Orchestrierung bereit. Sie ist Open Source unter einer MIT-ähnlichen Lizenz, auf PyPI verfügbar und speziell für FI-zu-FI-Kundenzahlungs-Workflows konzipiert – die Validierungsregeln sind daher auf die SR2026-CBPR+-Usage-Guidelines kalibriert und nicht über viele Nachrichtentypen hinweg abstrahiert.

**Was passiert, wenn mein Institut bis November 2026 nicht bereit ist?**

Nachrichten mit unstrukturierten Adressen in den betroffenen Parteifeldern werden nach der Umstellung auf Netzwerkebene zurückgewiesen. In der Praxis bedeutet das Zahlungsabwicklungsfehler, höhere Ausnahmevolumina, Wellen manueller Nacharbeit und voraussichtliche Kundenwirkung. Der SWIFT-In-Flow-Translation-Service ist für einige Übergangsfälle verfügbar, zieht jedoch ab Januar 2026 Zusatzgebühren nach sich und kann nicht jedes Adressformat zuverlässig parsen. SWIFT hat zudem ein quelloffenes KI-Modell zur Adressstrukturierung veröffentlicht, das Stadt und Land aus unstrukturierten Altdaten ableitet, aber für Sanierung und Vorverarbeitung konzipiert ist und kein dauerhafter Ersatz für saubere vorgelagerte Daten. Institute, die die Frist ohne sanierten Kundenstammdatenbestand und ohne automatisierte Validierungs-Pipeline erreichen, müssen mit einer schwierigen Umstellungswoche und einem deutlichen operativen Mehraufwand in den Folgemonaten rechnen.

## Quellen

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
