---
title: "Das Hauptbuch sichern: ein Leitfaden für Aufsichtsgremien zur Post-Quanten-Migration im Corporate Finance"
subtitle: "Das Quantenrisiko hat sich von einer Forschungsneugier zu einem aktiven aufsichtsrechtlichen Mandat entwickelt. Mit dem G7-Fahrplan, BIS Project Leap und den geklärten Zeitplänen in EU, UK und Australien stellt sich Aufsichtsräten nicht mehr die Frage des Ob, sondern des Wie."
description: "Das Quantenrisiko hat sich von einer Forschungsneugier zu einem aktiven aufsichtsrechtlichen Mandat entwickelt. Mit dem im Januar 2026 veröffentlichten G7-Fahrplan, mittlerweile geklärten Zeitplänen für EU, UK und Australien und BIS Project Leap, das die Machbarkeit in einem realen Zahlungssystem nachgewiesen hat, stellt sich Aufsichtsräten nicht mehr die Frage, ob migriert wird, sondern ob die Migration abgeschlossen werden kann, bevor die kryptografische Haltbarkeit heutiger Daten abläuft."
date: "May 14, 2026"
language: "de"
locale: "de_DE"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Offene Tresortür in goldenem Licht – visuelle Metapher für den kryptografischen Schutz von Finanzarchiven"
keywords: "Post-Quanten-Kryptografie, ML-KEM, ML-DSA, FIPS 203, FIPS 204, BIS Project Leap, G7 CEG, NCSC, ANSSI, BSI, ASD, CNSA 2.0, kryptografische Agilität, Corporate Finance, Wholesale Payments"
---

Das Quantenrisiko hat sich von einer Forschungsneugier zu einem aktiven aufsichtsrechtlichen Mandat entwickelt. Mit dem im Januar 2026 veröffentlichten G7-Fahrplan, mittlerweile geklärten Zeitplänen für EU, Vereinigtes Königreich und Australien und BIS Project Leap, das die Machbarkeit in einem realen Zahlungssystem nachgewiesen hat, stellt sich Aufsichtsräten nicht mehr die Frage, ob migriert wird, sondern ob die Migration abgeschlossen werden kann, bevor die kryptografische Haltbarkeit heutiger Daten abläuft.

---

> **Wesentliche Erkenntnisse**
>
> - **2026 ist das Jahr, in dem sich die aufsichtsrechtliche Haltung verfestigt hat.** Der Januar-Fahrplan der G7 Cyber Expert Group, der koordinierte Zeitplan der NIS-Kooperationsgruppe der EU und der Drei-Phasen-Plan des britischen NCSC haben die Diskussion vom Bewusstsein zur Umsetzung geführt. Das Australian Signals Directorate geht noch weiter und setzt 2030 als harte Frist für klassische asymmetrische Kryptografie.
> - **Die Exposition ist asymmetrisch.** RSA, ECC und Diffie–Hellman sind das unmittelbare Problem – die asymmetrischen Algorithmen, die SWIFT-Handshakes, TLS, PKI, Code-Signing und die Authentifizierung der Clearingnetze tragen. Symmetrische Verschlüsselung (AES-256) bleibt stabil, sofern die Schlüssellängen gewahrt werden. Der Fokus des Aufsichtsgremiums muss auf der asymmetrischen Fläche liegen.
> - **„Jetzt ernten, später entschlüsseln" ist kein Zukunftsszenario.** Gegner fangen heute Finanzprotokolle, Settlement-Daten, M&A-Material und grenzüberschreitende Überweisungsdaten ab und speichern sie, mit der erklärten Absicht, sie zu entschlüsseln, sobald ein kryptografisch relevanter Quantencomputer (CRQC) existiert. Für Daten mit einer Vertraulichkeitsanforderung von 10–20 Jahren ist dieses Risiko bereits realisiert.
> - **Die Branche verfügt nun über einen belastbaren Referenzpunkt.** [BIS Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), veröffentlicht im Dezember 2025, hat in produktiven Liquiditätstransfers über TARGET2 erfolgreich traditionelle digitale Signaturen durch Post-Quanten-Kryptografie ersetzt – und die konkreten Engineering-Kosten (Verifikationslatenz, Paketgröße) sichtbar gemacht, mit denen jedes Migrationsprogramm rechnen muss.
> - **Die NIST-Suite ist der globale Anker.** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") und FIPS 204 (ML-DSA) werden von jeder großen Jurisdiktion referenziert, auch dort, wo nationale Positionen bei Parameter-Sets und Hybridanforderungen abweichen. Aufsichtsräte sollten ML-KEM-768/ML-DSA-65 als Untergrenze und ML-KEM-1024/ML-DSA-87 als konservative Basislinie für langlebige Daten ansehen.
> - **Hybrid ist der einzige glaubwürdige Pfad.** Reine Umstellungen werden von keiner maßgeblichen Behörde empfohlen. Der Parallelbetrieb klassischer und quantenresistenter Verfahren ist das Bereitstellungsmuster, das NCSC, ANSSI, BSI bestätigen und das Project Leap erprobt hat. Es ist schwerer als jede der Alternativen, aber das Einzige, das zugleich die heutige Kompatibilität und die morgige Bedrohung adressiert.

---

## Das Jahr, in dem die aufsichtsrechtliche Haltung verfestigt wurde

Für einen Großteil des vergangenen Jahrzehnts lebte die Post-Quanten-Kryptografie in einer komfortablen Ecke der Langfrist-Roadmap. Quantencomputer waren beeindruckend, aber fern; die der RSA- und Elliptische-Kurven-Mathematik zugrunde liegenden Annahmen galten als stabiles Substrat; und die Migrationsdebatte blieb weitgehend Spezialarbeitskreisen vorbehalten. Diese Position lässt sich nicht länger halten.

Im Januar 2026 hat die [G7 Cyber Expert Group ihre bisher folgenreichste Erklärung veröffentlicht ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement on Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector"), unter dem Co-Vorsitz des US-Finanzministeriums und der Bank of England. Das Dokument ist keine Regulierung, hat aber mehr Gewicht als übliche Leitlinien: Es bringt die gemeinsame Haltung der Finanzministerien, Zentralbanken und Aufsichtsbehörden der G7-Jurisdiktionen zum Ausdruck, dass die kryptografische Transition nun ein systemisches Risikomanagement-Thema ist. Der Fahrplan richtet seinen Planungshorizont an der Mitte der 2030er Jahre aus, mit dem Appell, kritische Finanzsysteme früher zu migrieren – eine Formulierung, die im vorsichtigen Idiom von Zentralbankern eher eine Erwartung als eine Anregung signalisiert.

Zwei Monate zuvor hatten der BIS Innovation Hub und das Eurosystem die Ergebnisse von [Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems") veröffentlicht, einem technischen Experiment, das traditionelle digitale Signaturen durch Post-Quanten-Kryptografie in produktiven Liquiditätstransfers zwischen der Banca d'Italia, der Banque de France, der Deutschen Bundesbank, Nexi-Colt und Swift ersetzt hat. Die zentrale Erkenntnis war ein Erfolg – quantenresistent signierte Transfers durchliefen ein produktives Zahlungssystem von Ende zu Ende. Die Details unter der Schlagzeile sind aufschlussreicher und werden weiter unten betrachtet.

Die Kombination dieser beiden Ereignisse – ein koordinierter G7-Politikrahmen und ein funktionierender Beleg in einem realen Zahlungssystem – hat geliefert, worauf die Fachgemeinde ein Jahrzehnt gewartet hat: eine eindeutige Antwort auf die Frage „Ist das real?". Die Antwort lautet im Mai 2026: ja. Die verbliebene Frage ist eine des Tempos.

## Drei Bedrohungsvektoren, die den Aufsichtsrat beschäftigen sollten

Bevor die Migrationsmechanik diskutiert wird, lohnt es sich, präzise zu benennen, was konkret auf dem Spiel steht. Das Quantenrisiko im Corporate Finance ist nicht über das kryptografische Inventar hinweg einheitlich, und die Aufmerksamkeit des Aufsichtsrats konzentriert sich am besten auf die drei Vektoren mit der schärfsten Exposition.

### 1. Jetzt ernten, später entschlüsseln (HNDL)

Die unmittelbarste Sorge betrifft nicht die Zukunft. Sie betrifft die Gegenwart. Staatliche Akteure und versierte kriminelle Organisationen fangen heute systematisch verschlüsselten Finanzverkehr ab – Überweisungen, SWIFT-Nachrichtenflüsse, M&A-Kommunikation, grenzüberschreitende Settlement-Protokolle, Swap-Verträge und KYC-Dateien – ohne aktuell in der Lage zu sein, sie zu lesen. Ihr Ziel ist klar: jetzt sammeln, später entschlüsseln, sobald ein CRQC existiert. Wie die [Bank für Internationalen Zahlungsausgleich ausdrücklich festhält ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), läuft diese Sammlung bereits.

Für Aufsichtsräte ist die Implikation unbequem, aber präzise: Jede heute unter klassischer asymmetrischer Verschlüsselung übertragene sensible Information, deren Vertraulichkeitsanforderung über die Ankunft eines CRQC hinausreicht, muss bereits als exponiert betrachtet werden. Bei HNDL gibt es keine Benachrichtigung über eine Verletzung. Es gibt keinen Alarm im SIEM. Die Verschlüsselung hält – vorerst –, aber die Daten haben den Perimeter bereits verlassen.

### 2. Risiko langfristiger Sensitivität

Daten im Corporate Finance haben ungewöhnlich lange institutionelle Halbwertszeiten. Strategische M&A-Dokumentation kann ein Jahrzehnt lang marktrelevant bleiben. Kommunikation zu Geschäftsgeheimnissen und Bewertungen geistigen Eigentums können fünfzehn bis zwanzig Jahre lang vertraulich bleiben. Grenzüberschreitende Settlement-Protokolle, Engagements gegenüber zentralen Gegenparteien und Kreditbewertungen von Gegenparteien behalten kommerzielle Sensitivität weit über ihre unmittelbare transaktionale Lebenszeit hinaus.

Die [Mosca-Gleichung ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), ursprünglich von Michele Mosca formuliert und inzwischen in jedes ernstzunehmende Migrationsframework eingebettet, formalisiert das Problem. Wenn **S** die Aufbewahrungsdauer der Daten ist, **M** die Zeit, die erforderlich ist, um die schützenden Systeme zu migrieren, und **Q** die Zeit bis zur Verfügbarkeit eines CRQC, dann gilt:

```
Wenn S + M > Q, sind die Daten bereits exponiert.
```

Bei Daten mit einem Vertraulichkeitshorizont von zwanzig Jahren und einem realistisch fünf bis sieben Jahre dauernden Migrationsprogramm liegt das implizit erwartete Q, auf das ein Aufsichtsrat wettet, bei mindestens 25 Jahren. Eine wachsende Zahl von Expertenbewertungen – die [APAC-Prognosen 2026 von Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), die jährlichen Erhebungen des Global Risk Institute und ein Architektur-Paper vom Februar 2026, das einen CRQC bei rund 100.000 physischen Qubits unter Nutzung von QLDPC-Codes vorschlägt – legen nahe, dass diese Wette unsicher ist.

### 3. Die Verwundbarkeit zentraler Handshakes

Der dritte Vektor ist architektonisch der gewichtigste. Symmetrische Verfahren (AES-256) bleiben vergleichsweise stabil; Grovers Algorithmus halbiert das effektive Sicherheitsniveau, die Verdoppelung der Schlüssellänge stellt jedoch den Sicherheitsabstand wieder her. Die katastrophale Exposition betrifft die asymmetrischen Algorithmen – und genau diese tragen jeden authentifizierten Handshake im Corporate Finance: RSA in der SWIFT-PKI, ECDSA in der TLS-Client/Server-Authentifizierung, ECDH bei der Sitzungs­schlüsselherstellung und ECC-Varianten in der mobilen Client-Authentifizierung, API-Signaturen und Code-Signing-Pipelines.

Ein funktionsfähiger CRQC, der Shors Algorithmus ausführt, schwächt diese Systeme nicht graduell. Er bricht sie. Sobald ein CRQC operativ ist, werden jeder RSA-geschützte Handshake, jede ECDSA-Signatur und jeder Elliptische-Kurven-Schlüsseltausch rekonstruierbar – nicht in Monaten, sondern in Stunden. Der Übergang von „sicher" zu „kompromittiert" ist binär und breitet sich simultan über jedes System aus, das den betroffenen Algorithmus verwendet. Auf dieser Grundlage ruht die aufsichtsrechtliche Dringlichkeit.

## Regulatorische Verschärfung: ein Blick je Jurisdiktion

Das globale Regulierungsbild im Mai 2026 ist kein Flickenteppich von Empfehlungen mehr. Es ist ein koordiniertes Set von Zeitplänen, die in ihrer Strenge variieren, aber zum selben Ziel konvergieren. Eine multinationale Bank, die an den großen Finanzplätzen aktiv ist, ist nun an die jeweils strengste anwendbare Jurisdiktion gebunden – nicht an die nachsichtigste.

### Vereinigte Staaten

Die USA verfolgen die präskriptivste Position für jedes Institut, das föderale Systeme berührt. Die [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") der NSA schreibt ML-KEM-1024 und ML-DSA-87 für Systeme der nationalen Sicherheit vor; neue Systeme müssen ab Januar 2027 PQC einsetzen, die Infrastrukturmigration ist bis 2035 abzuschließen. OMB-Memorandum M-23-02 bindet Bundesbehörden an dieselbe Linie. Für Geschäftsbanken liegt die unmittelbare Exposition in föderalen Beschaffungsketten, NSS-naher Vertragsarbeit und dem indirekten Druck, den NSA-Leitlinien auf den breiteren Markt ausüben.

### Europäische Union

Die EU operiert auf drei Ebenen. Der [Coordinated Implementation Roadmap der Europäischen Kommission ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), ausgearbeitet von der NIS-Kooperationsgruppe im Juni 2025, setzt Etappen für 2026 (nationale Strategien), 2030 (Migration von Hochrisikosystemen) und 2035 (vollständige Transition). Der Cyber Resilience Act wird ab Ende 2027 State-of-the-Art-Sicherheitsupgrades für digitale Produkte vorschreiben. NIS2 stärkt das IKT-Risikomanagement, auch wenn keine der Richtlinien eine ausdrückliche PQC-Anforderung enthält. Nationale Regulatoren sind der Kommission hingegen vorausgeeilt. Das deutsche BSI schreibt hybriden Schlüsseltausch vor und billigt einen konservativen Korb aus ML-KEM, FrodoKEM und Classic McEliece. Die französische ANSSI verlangt Hybrid sowohl für die Schlüsselkapselung als auch für Signaturen. Die niederländische NLNCSA und die norwegischen Behörden haben sich auf ML-KEM-1024 als konservative Basislinie für langlebige Daten verständigt.

### Vereinigtes Königreich

Das britische NCSC hat seine maßgebliche Leitlinie im März 2025 veröffentlicht und im Jahresbericht 2025 bestätigt. Der Drei-Phasen-Plan ist ausdrücklich:

- **Bis 2028** – Identifikation der zu modernisierenden kryptografischen Dienste, Aufbau des Migrationsplans und Erstellung eines vollständigen kryptografischen Inventars.
- **2028 bis 2031** – Umsetzung prioritärer Modernisierungen, insbesondere bei kritischen Systemen und nach außen exponierten Internetprotokollen.
- **2031 bis 2035** – Abschluss der Migration über alle Systeme, Dienste und Produkte hinweg.

Für britische Finanzinstitute steht die [CMORG-PQC-Leitlinie (Cross-Market Operational Resilience Group) ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") neben dem NCSC-Rahmen; sie behandelt Banken als kritische nationale Infrastruktur und betont Lieferantenbereitschaft und Lieferketten-Abstimmung.

### Asien-Pazifik

Die APAC-Haltung ist fragmentierter, bewegt sich aber rasch. Australiens ASD hat global die härteste Position: Klassische Public-Key-Kryptografie darf nach Ende 2030 nicht mehr verwendet werden, keine Hybridempfehlung, ML-KEM-1024 erforderlich (ML-KEM-768 nur bis 2030 akzeptabel). Organisationen sollen bis Ende 2026 über einen ausgearbeiteten Übergangsplan verfügen. Die Monetary Authority of Singapore hat formelle Leitlinien zur Quantum-Readiness veröffentlicht. Japan und Südkorea investieren substanziell, beide verfolgen jedoch nationale Algorithmenpfade (Korea hat NTRU+ und SMAUG-T als KEMs sowie ALMer und HAETAE als Signaturen ausgewählt). Indiens National Quantum Mission, mit einer Mittelzuweisung von 6.003,65 Crore Rupien, weist Bank- und Finanzsysteme ausdrücklich als strategische Priorität aus. Die [APAC-Prognosen 2026 von Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") veranschlagen den Anteil regionaler Unternehmen, die in diesem Jahr in Post-Quanten-Technologien investieren werden, auf über 90 %.

### Die Nettoposition

Für einen Aufsichtsrat lautet die praktische Synthese dieser jurisdiktionalen Positionen klar. Eine multinationale Bank kann sich nicht am Zeitplan eines einzelnen Regulators orientieren; sie muss am jeweils strengsten anwendbaren Standard ausgerichtet werden. Für die meisten großen Institute heißt das: Planungshorizont Ende 2030 für Hochrisikosysteme und Ende 2035 für den langen Auslauf – ASD-exponierte Einheiten zielen auf reines PQC bis 2030, CNSA-exponierte Einheiten auf dasselbe Fenster mit spezifisch ML-KEM-1024 und ML-DSA-87.

## BIS Project Leap: Was die Branche tatsächlich bewiesen hat

Project Leap verdient die Aufmerksamkeit eines Aufsichtsrats nicht, weil es ein Marketing-Meilenstein ist, sondern weil es bislang der belastbarste Ende-zu-Ende-Beweis für Post-Quanten-Kryptografie in einem produktiven Finanzzahlungssystem ist. Die zentrale Schlussfolgerung ist schlicht: Es funktioniert. Die darunterliegenden Details sind dort, wo die operativen Implikationen liegen.

Phase 1, abgeschlossen 2023, etablierte ein quantenresistentes VPN zwischen den IT-Systemen der Banque de France und der Deutschen Bundesbank, über das Zahlungsnachrichten zwischen Paris und Frankfurt unter einem hybriden Verschlüsselungsschema übertragen wurden. Phase 2, abgeschlossen Ende 2025 und [im Dezember veröffentlicht ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), ging deutlich weiter. Das Konsortium ersetzte traditionelle RSA-basierte digitale Signaturen durch Post-Quanten-Signaturen bei der Ausführung von Liquiditätstransfers über TARGET2, das Real-Time-Gross-Settlement-System des Eurosystems. Die Teilnehmer – das BIS Innovation Hub Eurosystem Centre, die Banca d'Italia, die Banque de France, die Deutsche Bundesbank, Nexi-Colt (zuständig für die TARGET2-Konnektivität) und Swift – repräsentieren genau die Institutionen, deren Infrastruktur letztlich migrieren muss.

Der Bericht hebt drei Befunde hervor, die jedes Migrationsprogramm verinnerlichen sollte:

- **Die Verifikationslatenz ist spürbar höher.** Die Verifikation einer Post-Quanten-Signatur dauerte auf derselben Hardware materiell länger als die RSA-basierte Verifikation. Für ein RTGS-System, das auf Subsekunden-Nachrichtenverarbeitung ausgelegt ist, ist das keine Randnotiz, sondern ein Input für die Kapazitätsplanung.
- **Paketgrößen erfordern eine Systemüberarbeitung.** PQC-Signaturen sind eine Größenordnung größer als ECDSA-Pendants (mehr dazu weiter unten). Zahlungssysteme, deren interne Warteschlangen, Monitoring-Werkzeuge und Datenbankschemata für die Größenordnungen der Altnachrichten dimensioniert sind, können die neue Nutzlast ohne Neuentwurf nicht aufnehmen. Project Leap stellte ausdrücklich fest, dass TARGET2 das hybride Modell ohne erhebliche Reengineering-Arbeiten nicht „ohne Weiteres aufnehmen" könne.
- **Hybrid ist die richtige Antwort – aber schwerer.** Klassische und Post-Quanten-Algorithmen parallel zu betreiben, bewahrte Rückwärtskompatibilität und bot Verteidigung in der Tiefe, verdoppelte aber die kryptografische Rechenlast. Das ist der operative Preis dafür, PQC während des Übergangs richtig umzusetzen; er lässt sich durch geschicktes Engineering allein nicht vermeiden.

Für einen CFO, der einen PQC-Business-Case prüft, sind die Project-Leap-Befunde gerade deshalb nützlich, weil sie präzise sind. Die Kosten der Post-Quanten-Migration sind keine einzelne Investitionsposition. Sie sind eine Verifikationslatenz, die in SLA-Verträge hineinwirkt, eine Nachrichtengrößen-Ausdehnung, die Speicher- und Bandbreitenbudgets berührt, und eine Übergangsphase mit duplizierten kryptografischen Operationen, die die Kapazitätsplanung der Rechenressourcen beeinflusst. Nichts davon ist spekulativ. Es wurde in einem produktiven Zentralbanksystem gemessen.

## Das NIST-Toolkit: ML-KEM und ML-DSA im Vergleich

Das technische Herzstück jedes glaubwürdigen nationalen Rahmens ist die im August 2024 veröffentlichte NIST-Suite der Post-Quanten-Standards. Zwei dieser Standards stehen für das Corporate Finance im unmittelbaren Fokus: ML-KEM (FIPS 203) für die Schlüsselkapselung und ML-DSA (FIPS 204) für digitale Signaturen. Sie teilen eine mathematische Grundlage – beide beruhen auf der Härte der Probleme Module Learning With Errors (ML-LWE) und Module Short Integer Solution über strukturierten Gittern –, übernehmen jedoch sehr unterschiedliche Rollen im kryptografischen Inventar, und ihre Performance- und Größenprofile unterscheiden sich materiell.

### ML-KEM (FIPS 203) – Schlüsselkapselung

ML-KEM, abgeleitet aus [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html), ersetzt ECDH und RSA-KEM in Protokollen, in denen zwei Parteien einen gemeinsamen symmetrischen Schlüssel über einen unsicheren Kanal etablieren müssen. Praktisch ist es das, wohin TLS-Handshakes nach dem Ausmustern von RSA und ECDH wandern. NIST definiert drei Parameter-Sets mit steigender Sicherheitsstärke und sinkender Performance: ML-KEM-512 (NIST Kategorie 1), ML-KEM-768 (Kategorie 3) und ML-KEM-1024 (Kategorie 5).

### ML-DSA (FIPS 204) – digitale Signaturen

ML-DSA, abgeleitet aus CRYSTALS-Dilithium, ersetzt RSA- und ECDSA-Signaturen. Es übernimmt Zertifikatssignierung, Code-Signierung, Dokumentensignierung und Authentifizierung. Die drei Parameter-Sets sind ML-DSA-44, ML-DSA-65 und ML-DSA-87 und entsprechen grob den NIST-Kategorien 2, 3 und 5.

### Größen- und Performance-Profil

Für einen CIO, der die Migrationskapazität dimensioniert, sind die Artefaktgrößen die wichtigsten Zahlen. Sie sind Eingaben für Netzwerkkapazitätsplanung, Speicherprognosen und protokollnahe Tests.

| Algorithmus | Öffentlicher Schlüssel | Chiffrat / Signatur | Nächstes klassisches Pendant | Größe vs. Klassisch |
|---|---|---|---|---|
| ML-KEM-512 | 800 Byte | 768 Byte (Chiffrat) | ECDH P-256 (~32 Byte Public Key) | ~25× größer |
| ML-KEM-768 | 1.184 Byte | 1.088 Byte (Chiffrat) | ECDH P-384 | ~25× größer |
| ML-KEM-1024 | 1.568 Byte | 1.568 Byte (Chiffrat) | ECDH P-521 | ~25× größer |
| ML-DSA-44 | 1.312 Byte | ~2.420 Byte (Signatur) | ECDSA P-256 (64-Byte-Sig) | ~38× größer |
| ML-DSA-65 | 1.952 Byte | ~3.293 Byte (Signatur) | ECDSA P-384 | ~50× größer |
| ML-DSA-87 | 2.592 Byte | ~4.595 Byte (Signatur) | ECDSA P-521 | ~70× größer |

*Quelle: Synthese der Spezifikationen [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") und FIPS 204, mit Vergleichsdaten aus unabhängiger Benchmark-Literatur.*

Drei operative Implikationen folgen unmittelbar. **Erstens** ist die Signaturgröße für die meisten Unternehmenseinsätze die bindende Restriktion. Eine ML-DSA-65-Signatur ist rund fünfzigmal so groß wie eine ECDSA-P-256-Signatur, und TLS-Zertifikatsketten, die Zwischen-CAs tragen, wachsen proportional. Kapazitätsarbeiten auf dieser Fläche sind nicht optional – sie sind tragend. **Zweitens** ist ML-KEM rechentechnisch konkurrenzfähig zu ECDH und auf Hardware mit vektorisierter Unterstützung für die zugrunde liegende Gitterarithmetik in einigen Implementierungen materiell schneller. **Drittens** ist die ML-DSA-Verifikation durchgängig schnell (oft schneller als ECDSA-Verifikation), doch das Signieren bei ML-DSA umfasst eine Rejection-Sampling-Schleife, die auf eingeschränkter Hardware mehrere Versuche erfordern kann. Für Signaturdienste mit hohem Durchsatz ist das ein Benchmark, den man messen statt annehmen sollte.

### Parameter-Sets wählen

Die jurisdiktionalen Positionen zur Parameterwahl sind nicht identisch, die Konvergenz ist jedoch klar. ML-KEM-768 und ML-DSA-65 bilden die Untergrenze für Unternehmen – vom britischen NCSC als Basislinie bestätigt und in den meisten europäischen Rahmen akzeptabel. ML-KEM-1024 und ML-DSA-87 sind die konservative Obergrenze – durch NSA CNSA 2.0 für US-Systeme der nationalen Sicherheit vorgeschrieben und vom ASD für australische regulierte Einheiten bis 2030 verlangt. Für Daten mit extrem langer Sensitivität – souveräne Settlement-Protokolle, geistiges Eigentum mit Dekaden-Horizont, Verwahrnachweise für langlaufende Instrumente – sind die höheren Parameter-Sets die vertretbare Voreinstellung.

### Gemeinsame mathematische Grundlage, gemeinsames Risiko

Ein für Aufsichtsräte erwähnenswerter Punkt: Sowohl ML-KEM als auch ML-DSA leiten ihre Sicherheit aus derselben Familie von Gitterproblemen ab. Ein künftiger kryptanalytischer Durchbruch gegen Module-LWE träfe beide Standards gleichzeitig. Genau deshalb empfehlen mehrere nationale Behörden – insbesondere das deutsche BSI und die französische ANSSI –, den gitterbasierten Stack durch hashbasierte Signaturen (SLH-DSA, FIPS 205) für langfristige Signaturen und Code-Signing zu ergänzen. Kryptografische Agilität bedeutet in diesem Sinne nicht nur, RSA durch ML-KEM ersetzen zu können. Es bedeutet, einen PQC-Algorithmus durch einen anderen ersetzen zu können, wenn sich das kryptanalytische Bild verschiebt.

## Ein logischer Migrationspfad: Discovery → Triage → Hybride Bereitstellung

Für einen Aufsichtsrat, der ein mehrjähriges PQC-Programm genehmigt, lautet die operative Frage, wie die Arbeit phasiert werden kann, ohne ein unvertretbares Verfügbarkeitsrisiko einzugehen. Das Muster, das sich aus dem G7-Fahrplan, dem NCSC-Rahmen, BIS Project Leap und den maßgeblichen nationalen Leitlinien herausgebildet hat, konvergiert auf drei Phasen.

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  1. DISCOVERY & CBOM │ → │  2. TRIAGE (MOSCA)   │ → │  3. HYBRIDE          │
│  Kryptografisches    │   │  Risikobasierte      │   │     BEREITSTELLUNG   │
│  Inventar über alle  │   │  Priorisierung nach  │   │  Doppelte Hülle      │
│  Systeme hinweg      │   │  Datenhaltbarkeit    │   │  klassisch + PQC,    │
│                      │   │                      │   │  krypto-agil         │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### Phase 1 – Discovery und Cryptographic Bill of Materials (CBOM)

Migration lässt sich nicht für ein kryptografisches Inventar planen, das nicht kartiert ist – und die meisten Institute verfügen über keine genaue Karte. Die erste Phase ist daher die Erstellung einer Cryptographic Bill of Materials – ein strukturiertes Inventar jeder Instanz asymmetrischer Kryptografie in der Organisation, jeweils versehen mit Algorithmus, Schlüssellänge, Protokollkontext, Datensensitivität und Systemverantwortlichem. Automatisiertes Scannen über Codebasen, Webanwendungen, Container-Images, Datenbankkonfigurationen, Zertifikatsspeicher, HSMs und Lieferantenschnittstellen ist der praktische Mechanismus; die manuelle Erfassung von Altsystemen und proprietären Protokollen ist die unvermeidliche Ergänzung.

Das Ergebnis der Phase 1 ist nicht glamourös, aber das einzige Fundament, auf dem die Phasen 2 und 3 aufsetzen können. Es ist zugleich der Liefergegenstand, nach dem die meisten internen Revisionen und externen Aufsichtsbehörden zuerst fragen werden, sobald PQC-Compliance-Bestätigungen verlangt werden.

### Phase 2 – Risiko-Triage mit der Mosca-Gleichung

Mit der CBOM in der Hand kann das Institut Moscas Rahmenwerk Vermögenswert für Vermögenswert anwenden. Für jede kryptografische Abhängigkeit lautet die Frage: Gilt **S + M > Q**? Übersteigt die Datenhaltbarkeit plus die Migrationszeit die geschätzte Zeit bis zu einem CRQC? Vermögenswerte, bei denen die Ungleichung am schärfsten ausfällt – langlebige sensible Daten auf Infrastruktur, deren Migration Jahre dauert –, rücken an den Anfang der Warteschlange. Vermögenswerte mit kurzer Datenhaltbarkeit oder bereits modernisierter Infrastruktur können später im Programm angeordnet werden.

In dieser Phase wird die Risikobereitschaft des Aufsichtsrats am sichtbarsten. Der Q-Wert, gegen den das Institut plant, ist im Kern eine strategische Wette auf das Tempo des Quantenhardware-Fortschritts. Ein konservatives Q (Mitte der 2030er) erzeugt einen aggressiveren Migrationsplan und eine höhere kurzfristige Capex-Linie. Ein optimistisches Q (nach 2040) erzeugt einen entspannteren Plan und eine höhere Restexposition gegenüber bereits geernteten Daten. Keines ist falsch; beide sollten ausdrückliche Entscheidungen des Aufsichtsrats sein, nicht implizite Vorgaben der Technologiefunktion.

### Phase 3 – Hybride Bereitstellung

Sobald prioritäre Vermögenswerte identifiziert sind, sollte die Bereitstellung dem hybriden Muster folgen, das in Project Leap erprobt wurde und von NCSC, ANSSI, BSI und dem G7-Fahrplan empfohlen wird. Eine hybride Bereitstellung führt einen klassischen und einen Post-Quanten-Algorithmus parallel aus und vereint die Ergebnisse in einer einzigen Hülle. Das Komposit ist sowohl gegen klassische Angriffe (der klassische Algorithmus hält heute) als auch gegen Quantenangriffe (der PQC-Algorithmus hält morgen) sicher. Konkret bedeutet das in der Praxis: X25519 kombiniert mit ML-KEM-768 oder ML-KEM-1024 für die Schlüsselkapselung und ECDSA kombiniert mit ML-DSA für Signaturen, sofern doppelte Signaturen operativ umsetzbar sind.

Der Befund aus Project Leap, dass Hybrid „deutlich, deutlich schwerer" ist als jede der reinen Varianten, ist das ehrliche Gegengewicht zu dieser Empfehlung. Aufsichtsräte sollten mit erhöhtem Bedarf an Rechen- und Speicherkapazität, längeren Handshakes und zusätzlicher Komplexität in den Zertifikatsketten während der Übergangsphase rechnen. Der Vorteil: Hybrid eliminiert die größte einzelne Migrationsrisikoquelle – den abrupten Wechsel von einer kryptografischen Grundlage zur anderen in einer Produktionsumgebung.

## Was das kostet, und warum Nichtstun mehr kostet

Die Analyse von Mastercard, [Anfang 2026 berichtet ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs"), beziffert die globalen PQC-Migrationskosten im Finanzsektor auf 28–42 Milliarden US-Dollar. Innerhalb dieses Aggregats legt die [RedCompass-Labs- und CMORG-Forschung ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") zu tatsächlichen institutionellen Ausgaben nahe, dass Tier-1-Banken 20–30 Millionen US-Dollar jährlich in Vorbereitungsprogramme stecken, mit Implementierungszeiträumen über mehrere Führungs­zyklen. Das sind erhebliche Zahlen. Sie sind jedoch nicht der relevante Vergleich.

Der relevante Vergleich ist der Preis eines einzelnen retrospektiven Entschlüsselungsereignisses. Für ein Institut, dessen geernteter Zahlungsverkehr, dessen M&A-Korrespondenz oder dessen Gegenpartei-Exposure-Daten 2032 für einen Gegner lesbar werden, ist der operative und reputative Schaden nicht durch die Migrations-Capex-Linie begrenzt. Er ist durch den Wert des darunterliegenden Jahrzehnts strategischer Informationen begrenzt – und der ist für jedes systemrelevante Institut materiell größer als jedes plausible Migrationsbudget. Die Rahmung der G7, die kryptografische Transition als systemisches Risikomanagementthema und nicht als Technologie-Upgrade zu behandeln, ist zutreffend, und Aufsichtsräte sollten sie auf dieser Grundlage angehen.

Es gibt eine zweite Kostenlinie, die es wert ist, abgetrennt zu werden. Die Migration zu PQC ist eine Zwangsfunktion für kryptografische Agilität – die architektonische Fähigkeit, kryptografische Algorithmen auszutauschen, ohne die auf ihnen aufsetzenden Systeme neu zu bauen. Die meisten Institute verfügen heute nicht über kryptografische Agilität; ihre RSA- und ECC-Abhängigkeiten sind tief in PKIs, Code-Signing-Ketten, Lieferantenintegrationen und über Jahrzehnte gewachsene Hausprotokolle eingebettet. Die unter dem Druck der PQC-Transition getätigte Agilitätsinvestition ist langlebig. Sie wird auch beim nächsten kryptografischen Übergang wieder beansprucht – sei es ein Nachfolger der gitterbasierten PQC, eine QKD-Überlagerung oder etwas, das noch nicht auf der Standards-Roadmap steht. Richtig behandelt, ist die PQC-Migrations-Capex eine einmalige Investition mit wiederkehrender Optionalität.

## Fazit

Der Fall, die Post-Quanten-Migration 2026 als Aufsichtsrats-Priorität zu behandeln, beruht nicht auf der unmittelbaren Bevorstehung eines CRQC. Schätzungen dazu bleiben tatsächlich unsicher – glaubwürdige wissenschaftliche Einschätzungen veranschlagen die Wahrscheinlichkeit eines CRQC bis 2028 deutlich unter einem Prozent, steigend auf rund fünfzig Prozent bis 2037–2040. Der Fall beruht auf drei anderen Beobachtungen, die nicht unsicher sind.

Erstens: HNDL findet heute statt, und Daten mit einer Vertraulichkeitsanforderung von einem Jahrzehnt oder mehr sind exponiert, unabhängig davon, wann der CRQC eintrifft. Zweitens: Die Migration des kryptografischen Inventars eines großen Finanzinstituts dauert auch bei angemessener Finanzierung und Führungs­aufmerksamkeit fünf bis sieben Jahre – das 2026 begonnene Programm endet damit etwa 2031, was deutlich innerhalb des konservativen Endes der CRQC-Wahrscheinlichkeitsverteilung liegt. Drittens: Die aufsichtsrechtlichen Erwartungen haben sich in den letzten zwölf Monaten materiell verschärft, und die Institute, deren Aufsichtsratsprotokolle für 2026 ein klares PQC-Programm dokumentieren, werden in einer deutlich stärkeren Position sein als jene, die nur eine beobachtende Haltung festhalten.

Institute, die jetzt beginnen, haben den Vorteil der Wahl. Sie können die Arbeit über Führungszyklen hinweg phasieren, sie in breitere Resilienzinitiativen einbetten und die operativen Kosten der hybriden Bereitstellung in normaler Kapitalplanung verarbeiten. Institute, die warten, werden derselben Arbeit unter engeren Fristen, mit weniger Spielraum für Phasenführung und vor dem Hintergrund wachsender Engpässe bei PQC-fähiger Hardware, Expertise und Lieferantenkapazität gegenüberstehen. Die Kosten frühen Handelns sind bekannt; die Kosten späten Handelns sind asymmetrisch in genau jener Weise, die Risikomanagement vermeiden soll.

Zur Einordnung auf dieser Website: Der [Beitrag vom April 2026 zur Verdichtung der Quantenschwellen](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") betrachtete die zugrundeliegende Hardware-Bahn, die [Analyse zu CRYSTALS-Kyber von November 2023](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") behandelte die mathematischen Grundlagen, die nun als ML-KEM standardisiert sind, der [Beitrag zur Quantum Key Distribution von Dezember 2023](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") thematisierte die komplementäre [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html)-Überlagerung, und die [Open-Source-Referenzimplementierung KyberLib](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") liefert eine produktive Rust-Implementierung der zugrunde liegenden Primitive für Institute, die die kryptografische Fläche direkt prüfen wollen. Sich auf die praktischen und technischen Details einzulassen – nicht nur auf die aufsichtsrechtlichen Schlagzeilen – ist die Art, wie Aufsichtsräte glaubwürdige Migrationsprogramme von Compliance-Theater unterscheiden.

## Häufig gestellte Fragen

**Wann wird ein kryptografisch relevanter Quantencomputer tatsächlich existieren?**

Glaubwürdige Schätzungen variieren stark. Anfang 2026 haben öffentliche Quantendemonstrationen etwa 24 bis 28 logische Qubits erreicht, während ein CRQC schätzungsweise rund 6.000 logische Qubits erfordert, gestützt durch 100.000 bis mehrere Millionen physische Qubits, je nach Ansatz der Fehlerkorrektur. Der Expertenkonsens veranschlagt die CRQC-Wahrscheinlichkeit bis 2028 auf weniger als ein Prozent, um 2037–2040 auf rund fünfzig Prozent, bei erheblicher Streuung der Prognosen. Jüngste Reduktionen theoretischer Ressourcenschätzungen – von 20 Millionen Qubits vor wenigen Jahren auf weniger als eine Million in Gidneys Arbeit von 2025 und auf rund 100.000 im QLDPC-Architekturpaper vom Februar 2026 – haben den Planungshorizont verkürzt. Für Aufsichtsräte ist die angemessene Planungsannahme: Mitte der 2030er Jahre für Hochrisikosysteme, Ende der 2030er als konservativer Mittelpunkt und früher, sofern die HNDL-Exposition das bindende Anliegen ist.

**Warum hybride Bereitstellung statt reiner Post-Quanten-Bereitstellung?**

Drei Gründe. Erstens haben ML-KEM und ML-DSA, obwohl sorgfältig geprüft, kürzere kryptanalytische Historien als RSA und ECC. Ein Hybrid bleibt sicher, solange eine Komponente hält; ein reines PQC-Schema ist exponiert, falls das Gitterproblem unerwartet geschwächt wird. Zweitens wahrt Hybrid die Rückwärtskompatibilität mit Gegenparteien, die noch nicht migriert sind – kritisch in einer mehrjährigen Branchentransition. Drittens empfiehlt mit Ausnahme des Australian Signals Directorate jede maßgebliche Behörde ausdrücklich Hybrid für die Übergangsphase: NCSC, ANSSI, BSI, NLNCSA und der G7-Rahmen unterstützen den Doppelhüllen-Ansatz. Der Preis, wie Project Leap quantifiziert hat, ist ein materiell höherer Rechen- und Speicher-Overhead. Das ist der Preis der Optionalität.

**Brauchen wir sowohl ML-KEM als auch ML-DSA, oder können wir wählen?**

Beide. ML-KEM und ML-DSA übernehmen unterschiedliche kryptografische Rollen. ML-KEM ersetzt die Schlüsseletablierungs-Primitive in TLS, VPNs, mobiler Authentifizierung und ähnlichen Protokollen, in denen zwei Parteien einen gemeinsamen symmetrischen Schlüssel aushandeln müssen. ML-DSA ersetzt die digitalen Signatur-Primitive in PKI-Zertifikaten, Code-Signing, Dokumentensignierung, SWIFT-ähnlichem authentifiziertem Nachrichtenverkehr und Identitätsaussagen. Das kryptografische Inventar eines Instituts nutzt beide Primitivtypen an unterschiedlichen Stellen; die Migration muss beide adressieren. Die deutlich größere Signaturgröße von ML-DSA (50–70× ECDSA) ist operativ in der Regel die anspruchsvollere Komponente; die Netzwerk- und Speicherplanung für ML-DSA dominiert die meisten Migrationskapazitätsbewertungen.

**Wie misst man den Fortschritt in einem Programm dieser Größe?**

Drei Kennzahlen sind praktikabel und decken sich mit den maßgeblichen Regulierungsrahmen. **Abdeckung der CBOM** – welcher Anteil der asymmetrischen kryptografischen Instanzen des Instituts inventarisiert, klassifiziert und mit Migrationspriorität versehen wurde. **Migrations­abdeckung der Hochrisiko-Assets** – welcher Anteil der Vermögenswerte, bei denen Moscas Bedingung S + M > Q zutrifft, auf hybride PQC umgestellt wurde. **Abdeckung der kryptografischen Agilität** – welcher Anteil der kryptografisch abhängigen Systeme Algorithmen ohne Code-Änderungen, allein per Konfiguration, austauschen kann. Der G7-CEG-Fahrplan, der NCSC-Drei-Phasen-Rahmen und der koordinierte EU-Fahrplan decken sich im Wesentlichen mit diesen drei Maßzahlen, auch wenn die Terminologie unterschiedlich ist.

**Was kostet es, ein weiteres Jahr zu warten?**

Nicht null, und nicht symmetrisch. Ein Jahr Wartezeit verwirkt ein Jahr HNDL-Schutz für langlebige Daten – Daten, deren Vertraulichkeitsanforderung bis 2040 reicht, sind ein Jahr länger exponiert als nötig. Es verkürzt das Migrationsfenster gegenüber festen regulatorischen Fristen (ASD 2030, NSA-CNSA-2.0-Meilensteine, EU-Ziel 2030 für kritische Systeme), was sich in höherem Lieferrisiko und geringerer Phasenflexibilität niederschlägt. Es exponiert das Institut gegenüber bereits sichtbaren Angebots-Engpässen bei Lieferanten und Talenten, die sich verschärfen werden, sobald die größten Akteure der Branche von Planung zu Umsetzung übergehen. Die Kosten sind in einem einzelnen Jahr nicht katastrophal, aber sie kumulieren, und die regulatorische Umgebung konvergiert zu einer Lage, in der Aufsichtsräte die Verzögerung erklären müssen statt die Ausgaben.

## Quellen

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
