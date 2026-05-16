---
title: "Het grootboek beveiligen: post-kwantummigratie in corporate finance"
subtitle: "Hoe corporate finance zich voorbereidt op het post-kwantumtijdperk"
description: "Een blauwdruk voor de post-kwantummigratie van het corporate-finance-grootboek — krypto-agility, audit en governance."
date: "May 14, 2026"
language: "nl-NL"
locale: "nl_NL"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Visualisatie van een beveiligd corporate-finance-grootboek"
keywords: "Corporate finance, post-kwantum, migratie, grootboek, cryptografie, banking"
---
Het kwantumrisico heeft sich van een onderzoeksnieuwgier tot een aktiven aufsichtsrechtlichen Mandat ontwikkeld. Mit de in januari 2026 veröffentlichten G7-Fahrplan, mittlerweile geklärten tijdpadenn voor EU, Vereinigtes Königreich en Australien en BIS Project Leap, het de Machbarkeit in een realen betaalsysteem nachgewiesen heeft, stelt sich toezichtsräten niet meer de vraag, ob gemigreerd wordt, sondern ob de migratie abgeschlossen worden kan, bevor de cryptografische Houdbarkeit heutiger Daten abläuft.

---

> **Wesentliche inzichten**
>
> - **2026 is het jaar, in de sich de aufsichtsrechtliche Houdung verfestigt heeft.** De januari-Fahrplan de G7 Cyber Expert Group, de koordinooitrte tijdpad de NIS-Kooperationsgruppe de EU en de Drei-Phasen-plan des britischen NCSC hebben de Diskussion vom Bewusstsein tot Umsetzung geführt. Het Australian Signals Directorate geht nog weiter en zet 2030 als harte Frist voor klassische asymmetrische cryptografie.
> - **De Exposition is asymmetrisch.** RSA, ECC en Diffie–Hellman zijn het unmittelbare probleem – de asymmetrischen Algorithmen, de SWIFT-Handshakes, TLS, PAI, Code-Signing en de Authentifizierung de Clearingnetze tragen. Symmetrische versleuteling (AES-256) bleibt stabil, sofern de sleutellängen gewahrt worden. De Fokus des toezichtsgremiums moet op de asymmetrischen Fläche liegen.
> - **„Jetzt ernten, später entschlüsseln" is kein toekomstsszenario.** Gegner fangen heute financieelprotokolle, settlement-Daten, M&A-Material en grensoverschrijdende overboekingsdaten ab en speichern ze, met de erklärten Absicht, ze tot entschlüsseln, sobald een cryptografisch relevanter kwantumcomputers (CRQC) existiert. Für Daten met een Vertraulichkeitsanforderung van 10–20 jaaren is dit risico reeds realisiert.
> - **De sector verfügt nun over een belastbaren Referenzpunkt.** [BIS Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), veröffentlicht in december 2025, heeft in produktiven liquiditeitstransfers over TARGET2 succesvol traditionele digitaale Signaturen door post-kwantumcryptografie erzet – en de konkreten Engineering-kosten (Verifikationslatenz, Paketgröße) sichtbar gemacht, met denen ieder migratiesprogramm rechnen moet.
> - **De NIST-Suite is de wereldwijde Anker.** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism standaard") en FIPS 204 (ML-DSA) worden van iedere grooten Jurisdiktion referenziert, ook dort, wo nationale Positionen bij Parameter-Sets en Hybridanforderungen abweichen. toezichtsräte zouden moeten ML-KEM-768/ML-DSA-65 als Untergrenze en ML-KEM-1024/ML-DSA-87 als konservative Basislinooit voor langlebige Daten ansehen.
> - **Hybrid is de einzige glaubwürdige Pfad.** Reine Umstellungen worden van keiner maßgeblichen instantie empfohlen. De Parallelbetrieb klassischer en kwantumresistente procedure is het Bereitstellungsmuster, het NCSC, ANSSI, BSI bestätigen en het Project Leap erprobt heeft. Es is schwerer als iedere de Alternativen, maar het Einzige, het tegelijk de heutige Kompatibilität en de morgige dreiging adressiert.

---

## Het jaar, in de de aufsichtsrechtliche Houdung verfestigt werd

Für een Großteil des vergangenen jaarzehnts lebte de post-kwantumcryptografie in een komfortablen Ecke de Langfrist-routekaart. kwantumcomputers waren beeindruckend, maar fern; de de RSA- en Elliptische-Kurven-Mathematik zugongeveere liegenden Annahmen gouden als stabiles Substrat; en de migratiesdebatte blieb weitgehend Spezialarbeitskreisen vorbehouden. Deze Position lässt sich niet länger houden.

Im januari 2026 heeft de [G7 Cyber Expert Group haar bisher folgenreichste Erklärung veröffentlicht ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement on Advancing a Coordinated routekaart for the Transition to Post-Quantum Cryptography in the Financial Sector"), onder de Co-Vorsitz des US-financieelministeriums en de bank of England. Het Dokument is keine regelgeving, heeft maar meer Gewicht als übliche Leitlinooitn: Es bringt de gezamenlijke Houdung de financieelministerien, centrale banken en toezichthouders de G7-Jurisdiktionen tot Ausdruck, dat de cryptografische Transition nun een systemisches risicomanagement-Thema is. De Fahrplan richtet zijn planungshorizont aan de Mitte de 2030er jaare uit, met de Appell, kritische financieelsysteme früher tot migrieren – een Formulierung, de in vorsichtigen Idiom van centrale bankern eher een Erwartung als een Anregung signalisiert.

Zwei maande zuvor hadden de BIS innovatie Hub en het Eurosystem de resultaten van [Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems") veröffentlicht, een technischen Experiment, het traditionele digitaale Signaturen door post-kwantumcryptografie in produktiven liquiditeitstransfers tussen de Banca d'Italia, de Banque de France, de Deutschen Bundesbank, Nexi-Colt en Swift erzet heeft. De centrale inzicht was een Erfolg – kwantumresistent signooitrte Transfers durchliefen een produktives betaalsysteem van einde tot einde. De Details onder de Schlagzeile zijn aufschlussreicher en worden weiter unten betrachtet.

De Kombination deze beiden Ereignisse – een koordinooitrter G7-beleidrahmen en een funktionooitrender Beleg in een realen betaalsysteem – heeft gelevert, worauf de Fachgemeinde een jaarzehnt gewartet heeft: een eindeutige antwoord op de vraag „Ist het real?". De antwoord lautet in mei 2026: ja. De verbliebene vraag is een des Tempos.

## Drei dreigingsvektoren, de de toezichtsrat beschäftigen zouden moeten

Bevor de migratiesmechanik diskutiert wordt, lohnt es sich, präzise tot benennen, was konkret op de Spiel steht. Het kwantumrisico in Corporate Finance is niet over het cryptografische inventaris hinweg einheitlich, en de Aufmerksamkeit des toezichtsrats konzentriert sich am besten op de drei Vektoren met de schärfsten Exposition.

### 1. Jetzt ernten, später entschlüsseln (HNDL)

De unmittelbarste Sorge betrifft niet de toekomst. U betrifft de Gegenwart. Staatliche actoren en versierte kriminelle Organisationen fangen heute systematisch versleutelden financieelverkehr ab – overboekingen, SWIFT-berichtenflüsse, M&A-Kommunikation, grensoverschrijdende settlement-Protokolle, Swap-Verträge en KYC-Dateien – zonder actueel in de Lage tot zijn, ze tot lesen. uw Ziel is duidelijk: jetzt sammeln, später entschlüsseln, sobald een CRQC existiert. Wie de [bank voor Internationalen betalingsausgleich ausdrücklich festhält ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), läuft deze Sammlung reeds.

Für toezichtsräte is de Implikation unbequem, maar präzise: Jede heute onder klassischer asymmetrischer versleuteling übertragene sensible Information, deren Vertraulichkeitsanforderung over de Ankunft een CRQC uitreicht, moet reeds als exponooitrt betrachtet worden. Bei HNDL gibt es keine Benachrichtigung over een Verletzung. Es gibt keinen Alarm in SIEM. De versleuteling hält – vorpas –, maar de Daten hebben de Perimeter reeds verlassen.

### 2. risico langetermijn-hij Sensitivität

Daten in Corporate Finance hebben ungewöhnlich lange institutionelle Halbwertszeiten. Strategische M&A-Dokumentation kan een jaarzehnt lang marktrelevant bleiben. Kommunikation tot Geschäftsgeheimnissen en beoordelingen geistigen Eigentums kunnen fünfzehn bis zwanzig jaare lang vertraulich bleiben. Grenzüberschreitende settlement-Protokolle, Engagements gegenüber centralen Gegenparteien en Kreditbewertungen van Gegenparteien behouden kommerzielle Sensitivität weit over haar unmittelbare transaktionale Lebenszeit uit.

De [Mosca-Gleichung ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A banker's Guide to Quantum Safe Cryptography — Part 3"), ursprünglich van Michele Mosca formuliert en inmiddels in ieder ernstzunehmende migratiesframework eingebettet, formalisiert het probleem. Wenn **S** de Aufbewahrungsdauer de Daten is, **M** de Zeit, de vereist is, um de beschermenden systeeme tot migrieren, en **Q** de Zeit bis tot beschikbaarheid een CRQC, dan gilt:

```
Wenn S + M > Q, zijn de Daten reeds exponooitrt.
```

Bei Daten met een Vertraulichkeitshorizont van zwanzig jaaren en een realistisch fünf bis sieben jaare dauernden migratiesprogramm liegt het implizit erwartete Q, op het een toezichtsrat wettet, bij minstens 25 jaaren. Een wachsende Zahl van Expertenbewertungen – de [APAC-Prognosen 2026 van Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), de jährlichen Erhebungen des Global Risk Institute en een Architektur-Paper vom februari 2026, het een CRQC bij ongeveer 100.000 physischen Qubits onder gebruik van QLDPC-Codes vorschlägt – leggen nahe, dat deze Wette unsicher is.

### 3. De Verwundbarkeit centraler Handshakes

De dritte Vektor is architektonisch de gebelangrijkste. Symmetrische procedure (AES-256) bleiben vergleichsweise stabil; Grovers Algorithmus halbiert het effektive beveiligingsniveau, de Verdoppelung de sleutellänge stelt echter de beveiligingsabstand wieder her. De katastrophale Exposition betrifft de asymmetrischen Algorithmen – en nauwkeurig deze tragen iedere authentifizierten Handshake in Corporate Finance: RSA in de SWIFT-PAI, ECDSA in de TLS-Client/Server-Authentifizierung, ECDH bij de Sitzungs­schlüsselhpasellung en ECC-Varianten in de mobilen Client-Authentifizierung, API-Signaturen en Code-Signing-Pipelines.

Een funktionsfähiger CRQC, de Shors Algorithmus ausführt, schwächt deze systeeme niet graduell. Hij bricht ze. Sobald een CRQC operativ is, worden iedere RSA-beschermde Handshake, iedere ECDSA-Signatur en iedere Elliptische-Kurven-sleuteltausch rekonstruierbar – niet in maanden, sondern in uren. De Übergang van „sicher" tot „kompromittiert" is binär en breitet sich simultan over ieder systeem uit, het de betroffenen Algorithmus gebruikt. Auf deze Gongeveerlage ruht de aufsichtsrechtliche Dringlichkeit.

## Regulatorische Verschärfung: een Blick je Jurisdiktion

Het wereldwijde regelgevingsbild in mei 2026 is kein Flickenteppich van aanbevelingen meer. Es is een koordinooitrtes Set van tijdpadenn, de in haar Strenge variieren, maar tot selben Ziel konvergieren. Een multinationale bank, de aan de grooten financieelplätzen aktiv is, is nun aan de jeweils strengste anwendbare Jurisdiktion gebunden – niet aan de nachsichtigste.

### Vereinigte Staaten

De USA vplaatsvinden de präskriptivste Position voor ieder Institut, het föderale systeeme berührt. De [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") de NSA schreibt ML-KEM-1024 en ML-DSA-87 voor systeeme de nationalen beveiliging vóór; nieuwe systeeme moeten ab januari 2027 PQC einzetten, de Infrastrukturmigration is bis 2035 abzuschließen. OMB-Memorandum M-23-02 bindet Bundesbehörden aan dieselbe Linooit. Für Geschäftsbanken liegt de unmittelbare Exposition in föderalen Beschaffungsketten, NSS-naher Vertragsarbeit en de indirekten Druck, de NSA-Leitlinooitn op de breiteren markt ausüben.

### Europäische Union

De EU operiert op drei Ebenen. De [Coordinated Implementation routekaart de Europäischen Kommission ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC routekaarts and Transition Guidance"), ausgearbeitet van de NIS-Kooperationsgruppe in juni 2025, zet Etappen voor 2026 (nationale strategien), 2030 (migratie van Hochrisikosystemen) en 2035 (vollvoortdurende Transition). De Cyber Resilience Act wordt ab einde 2027 State-of-the-Art-beveiligingsupgrades voor digitaale producten vorschreiben. NIS2 stärkt het IKT-risicomanagement, ook indien keine de Richtlinooitn een ausdrückliche PQC-Anforderung enthält. Nationale Regulatoren zijn de Kommission daarentegen vorausgeeilt. Het deutsche BSI schreibt hybriden sleuteltausch vóór en billigt een konservativen Korb uit ML-KEM, FrodoKEM en Classic McEliece. De französische ANSSI verlangt Hybrid zowel voor de sleutelencapsulatie als voor Signaturen. De nooitderländische NLNCSA en de norwegischen instanties hebben sich op ML-KEM-1024 als konservative Basislinooit voor langlebige Daten vpasändigt.

### Vereinigtes Königreich

Het britische NCSC heeft zijne maßgebliche Leitlinooit in maart 2025 veröffentlicht en in jaaresbericht 2025 bestätigt. De Drei-Phasen-plan is ausdrücklich:

- **Bis 2028** – Identifikation de tot modernisierenden cryptografischen dienste, Aufbau des migratiesplans en Erstellung een vollvoortdurenden cryptografischen inventariss.
- **2028 bis 2031** – Umsetzung prioritärer Modernisierungen, insbesondere bij kritischen systeemen en na außen exponooitrten Internetprotokollen.
- **2031 bis 2035** – Abschluss de migratie over alle systeeme, dienste en producten hinweg.

Für britische financieelinstitute steht de [CMORG-PQC-Leitlinooit (Cross-Market Operational Resilience Group) ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") neben de NCSC-Rahmen; ze behandelt banken als kritische nationale Infrastruktur en betont Lieferantenreedschaft en Lieferketten-Abstimmung.

### Asien-Pazifik

De APAC-Houdung is fragmentierter, bewegt sich maar rasch. Australiens ASD heeft wereldwijd de härteste Position: Klassische Public-Key-cryptografie darf na einde 2030 niet meer gebruikt worden, keine Hybridempfehlung, ML-KEM-1024 vereist (ML-KEM-768 alleen bis 2030 akzeptabel). Organisationen sollen bis einde 2026 over een ausgearbeiteten Übergangsplan verfügen. De Monetary Authority of Singapore heeft formelle Leitlinooitn tot Quantum-Readiness veröffentlicht. Japan en Südkorea investieren substanziell, beide vplaatsvinden echter nationale Algorithmenpfade (Korea heeft NTRU+ en SMAUG-T als KEMs sowie ALMer en HAETAE als Signaturen ausgewählt). Indiens National Quantum Mission, met een Mittelzuweisung van 6.003,65 Crore Rupien, weist bank- en financieelsysteme ausdrücklich als strategische Priorität uit. De [APAC-Prognosen 2026 van Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") veranschlagen de Anteil regionaler ondernemingen, de in deze jaar in post-kwantum-Technologien investieren worden, op over 90 %.

### De Nettoposition

Für een toezichtsrat lautet de praktische Synthese deze jurisdiktionalen Positionen duidelijk. Een multinationale bank kan sich niet am tijdpad een einzelnen Regulators orientieren; ze moet am jeweils strengsten anwendbaren standaard ausgerichtet worden. Für de meisten grooten Institute heißt het: planungshorizont einde 2030 voor Hochrisikosysteme en einde 2035 voor de langen Auslauf – ASD-exponooitrte Einheiten zielen op reines PQC bis 2030, CNSA-exponooitrte Einheiten op dasselbe Fenster met spezifisch ML-KEM-1024 en ML-DSA-87.

## BIS Project Leap: Was de sector tatsächlich bewiesen heeft

Project Leap verdient de Aufmerksamkeit een toezichtsrats niet, omdat es een Marketing-Meilenstein is, sondern omdat es bislang de belastbarste einde-tot-einde-Beweis voor post-kwantumcryptografie in een produktiven financieelzahlungssystem is. De centrale Schlussfolgerung is schlicht: Es funktionooitrt. De darunterliegenden Details zijn dort, wo de operativen Implikationen liegen.

Phase 1, abgeschlossen 2023, etablierte een kwantumresistentes VPN tussen de IT-systeemen de Banque de France en de Deutschen Bundesbank, over het betaalberichten tussen Paris en Frankfurt onder een hybriden versleutelingsschema übertragen werden. Phase 2, abgeschlossen einde 2025 en [in december veröffentlicht ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), ging duidelijk weiter. Het Konsortium erzete traditionele RSA-basierte digitaale Signaturen door post-kwantum-Signaturen bij de Ausführung van liquiditeitstransfers over TARGET2, het Real-Time-Gross-settlement-systeem des Eurosystems. De deelnemers – het BIS innovatie Hub Eurosystem Centre, de Banca d'Italia, de Banque de France, de Deutsche Bundesbank, Nexi-Colt (zuvoortdurend voor de TARGET2-Konnektivität) en Swift – repräsentieren nauwkeurig de Institutionen, deren Infrastruktur letztlich migrieren moet.

De Bericht hebt drei Befunde hervor, de ieder migratiesprogramm verinnerlichen zou moeten:

- **De Verifikationslatenz is spürbar hoger.** De Verifikation een post-kwantum-Signatur dauerte op derselben Hardware materiell länger als de RSA-basierte Verifikation. Für een RTGS-systeem, het op Subseklanten-berichtenverarbeitung ausgelegd is, is het keine Randnotiz, sondern een Input voor de Kapazitätsplanung.
- **Paketgrößen vereisen een systeemüberarbeitung.** PQC-Signaturen zijn een groottenordnung größer als ECDSA-Pendants (meer dazu weiter unten). betaalsysteeme, deren interne Warteschlangen, Monitoring-tools en Datenbankschemata voor de groottenordnungen de Altnachrichten dimensionooitrt zijn, kunnen de nieuwe Nutzlast zonder Neuentwurf niet aufnehmen. Project Leap stelte ausdrücklich fest, dat TARGET2 het hybride model zonder erhebliche Reengineering-Arbeiten niet „zonder Weiteres aufnehmen" könne.
- **Hybrid is de richtige antwoord – maar schwerer.** Klassische en post-kwantum-Algorithmen parallel tot bedrijven, bewahrte Rückwärtskompatibilität en bot Verteidigung in de diepte, verdoppelte maar de cryptografische Rechenlast. Het is de operative prijs daarvoor, PQC terwijl des Übergangs richtig umzuzetten; hij lässt sich door geschicktes Engineering allein niet vermeiden.

Für een CFO, de een PQC-Business-Case prüft, zijn de Project-Leap-Befunde gerade daarom nützlich, omdat ze präzise zijn. De kosten de post-kwantummigratie zijn keine einzelne investeringsposition. U zijn een Verifikationslatenz, de in SLA-Verträge hineinwirkt, een berichtengrößen-Ausdehnung, de Speicher- en Bandbreitenbudgets berührt, en een Übergangsphase met duplizierten cryptografischen Operationen, de de Kapazitätsplanung de Rechenressourcen beeinflusst. Nichts daarvan is spekulativ. Es werd in een produktiven centrale banksystem gemessen.

## Het NIST-Toolkit: ML-KEM en ML-DSA in Vergleich

Het technische Herzstück ieder glaubwürdigen nationalen Rahmens is de in August 2024 veröffentlichte NIST-Suite de post-kwantum-standaards. Zwei deze standaards stehen voor het Corporate Finance in unmittelbaren Fokus: ML-KEM (FIPS 203) voor de sleutelencapsulatie en ML-DSA (FIPS 204) voor digitaale Signaturen. U delen een mathematische Gongeveerlage – beide beruhen op de Härte de probleeme Module Learning With Errors (ML-LWE) en Module Short Integer Solution over strukturierten Gittern –, übernehmen echter zeer unterschiedliche Rollen in cryptografischen inventaris, en haar Performance- en groottenprofile unterscheiden sich materiell.

### ML-KEM (FIPS 203) – sleutelencapsulatie

ML-KEM, abgeleitet uit [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html), erzet ECDH en RSA-KEM in Protokollen, in denen zwei Parteien een gezamenlijken symmetrischen sleutel over een unsicheren Kanal etablieren moeten. Praktisch is es het, wohin TLS-Handshakes na de Ausmustern van RSA en ECDH wandern. NIST definooitrt drei Parameter-Sets met steigender beveiligingsstärke en sinkender Performance: ML-KEM-512 (NIST Kategorie 1), ML-KEM-768 (Kategorie 3) en ML-KEM-1024 (Kategorie 5).

### ML-DSA (FIPS 204) – digitaale Signaturen

ML-DSA, abgeleitet uit CRYSTALS-Dilithium, erzet RSA- en ECDSA-Signaturen. Es übernimmt Zertifikatssignooitrung, Code-Signooitrung, Dokumentensignooitrung en Authentifizierung. De drei Parameter-Sets zijn ML-DSA-44, ML-DSA-65 en ML-DSA-87 en entsprechen grob de NIST-Kategorien 2, 3 en 5.

### grootten- en Performance-Profil

Für een CIO, de de migratieskapazität dimensionooitrt, zijn de Artefaktgrößen de belangrijksten Zahlen. U zijn Eingaben voor netwerkkapazitätsplanung, Speicherprognosen en protokollnahe Tests.

| Algorithmus | Öffentlicher sleutel | Chiffrat / Signatur | Nächstes klassisches Pendant | grootte vs. Klassisch |
|---|---|---|---|---|
| ML-KEM-512 | 800 Byte | 768 Byte (Chiffrat) | ECDH P-256 (~32 Byte Public Key) | ~25× größer |
| ML-KEM-768 | 1.184 Byte | 1.088 Byte (Chiffrat) | ECDH P-384 | ~25× größer |
| ML-KEM-1024 | 1.568 Byte | 1.568 Byte (Chiffrat) | ECDH P-521 | ~25× größer |
| ML-DSA-44 | 1.312 Byte | ~2.420 Byte (Signatur) | ECDSA P-256 (64-Byte-Sig) | ~38× größer |
| ML-DSA-65 | 1.952 Byte | ~3.293 Byte (Signatur) | ECDSA P-384 | ~50× größer |
| ML-DSA-87 | 2.592 Byte | ~4.595 Byte (Signatur) | ECDSA P-521 | ~70× größer |

*Quelle: Synthese de Spezifikationen [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism standaard") en FIPS 204, met Vergleichsdaten uit onafhankelijker Benchmark-Literatur.*

Drei operative Implikationen folgen unmittelbar. **Erstens** is de Signaturgröße voor de meisten ondernemingenseinsätze de bindende Restriktion. Een ML-DSA-65-Signatur is ongeveer fünfzigmal so groot zoals een ECDSA-P-256-Signatur, en TLS-Zertifikatsketten, de Zwischen-CAs tragen, wachsen proportional. Kapazitätsarbeiten op deze Fläche zijn niet optional – ze zijn tragend. **Zweitens** is ML-KEM rechentechnisch konkurrenzfähig tot ECDH en op Hardware met vektorisierter Untpasützung voor de zugongeveere liegende Gitterarithmetik in einigen Implementierungen materiell sneler. **Drittens** is de ML-DSA-Verifikation durchgängig snel (vaak sneler als ECDSA-Verifikation), toch het Signooitren bij ML-DSA umfasst een Rejection-Sampling-Schleife, de op eingeschränkter Hardware mehrere Versuche vereisen kan. Für Signaturdienste met hogem Durchsatz is het een Benchmark, de man messen statt annehmen zou moeten.

### Parameter-Sets wählen

De jurisdiktionalen Positionen tot Parameterwahl zijn niet identisch, de Konvergenz is echter duidelijk. ML-KEM-768 en ML-DSA-65 vormen de Untergrenze voor ondernemingen – vom britischen NCSC als Basislinooit bestätigt en in de meisten Europeesen Rahmen akzeptabel. ML-KEM-1024 en ML-DSA-87 zijn de konservative Obergrenze – door NSA CNSA 2.0 voor US-systeeme de nationalen beveiliging vorgeschrieben en vom ASD voor australische regulierte Einheiten bis 2030 verlangt. Für Daten met extrem langer Sensitivität – souveräne settlement-Protokolle, geistiges Eigentum met Dekaden-Horizont, Verwahrnachweise voor langlaufende Instrumente – zijn de hogeren Parameter-Sets de vertretbare Voreinstellung.

### Gemeinsame mathematische Gongeveerlage, gezamenlijkes risico

Een voor toezichtsräte erwähnenswerter Punkt: Sowohl ML-KEM als ML-DSA leiten haar beveiliging uit derselben familie van Gitterproblemen ab. Een künftiger kryptanalytischer Durchbruch tegen Module-LWE träfe beide standaards gleichzeitig. Genau daarom empfehlen mehrere nationale instanties – insbesondere het deutsche BSI en de französische ANSSI –, de rooster-gebaseerde Stack door hashbasierte Signaturen (SLH-DSA, FIPS 205) voor langetermijn-e Signaturen en Code-Signing tot ergänzen. Kryptografische Agilität bedeutet in deze Sinne niet alleen, RSA door ML-KEM erzetten tot kunnen. Es bedeutet, een PQC-Algorithmus door een anderen erzetten tot kunnen, indien sich het kryptanalytische Bild verschiebt.

## Een logischer migratiespfad: Discovery → Triage → Hybride Bereitstellung

Für een toezichtsrat, de een mehrjähriges PQC-Programm genehmigt, lautet de operative vraag, zoals de Arbeit phasiert worden kan, zonder een unvertretbares beschikbaarheidsrisiko einzugehen. Het Muster, het sich uit de G7-Fahrplan, de NCSC-Rahmen, BIS Project Leap en de maßgeblichen nationalen Leitlinooitn herausgevormt heeft, konvergiert op drei Phasen.

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  1. DISCOVERY & CBOM │ → │  2. TRIAGE (MOSCA)   │ → │  3. HYBRIDE          │
│  Kryptografisches    │   │  risicobasierte      │   │     BEREITSTELLUNG   │
│  inventaris over alle  │   │  Priorisierung na  │   │  Doppelte Hülle      │
│  systeeme hinweg      │   │  Datenhoudbarkeit    │   │  klassisch + PQC,    │
│                      │   │                      │   │  krypto-agil         │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### Phase 1 – Discovery en Cryptographic Bill of Materials (CBOM)

migratie lässt sich niet voor een cryptografisches inventaris planen, het niet kartiert is – en de meisten Institute verfügen over keine nauwkeurige Karte. De pase Phase is daarom de Erstellung een Cryptographic Bill of Materials – een strukturiertes inventaris iedere instantie asymmetrischer cryptografie in de Organisation, jeweils versehen met Algorithmus, sleutellänge, Protokollkontext, Datensensitivität en systeemverantwortlichem. Automatisiertes Scannen over Codebasen, Webanwendungen, Container-Images, Datenbankkonfigurationen, Zertifikatsspeicher, HSMs en Lieferantenschnittstellen is de praktische Mechanismus; de manuelle Erfassung van Altsystemen en proprietären Protokollen is de unvermeidliche Ergänzung.

Het resultaat de Phase 1 is niet glamourös, maar het einzige Fundament, op de de Phasen 2 en 3 aufzetten kunnen. Es is tegelijk de Liefergegenstand, na de de meisten internen Revisionen en externen toezichthouders zupas fragen worden, sobald PQC-Compliance-Bestätigungen verlangt worden.

### Phase 2 – risico-Triage met de Mosca-Gleichung

Mit de CBOM in de Hand kan het Institut Moscas Rahmenwerk actief voor actief anwenden. Für iedere cryptografische Abhängigkeit lautet de vraag: Gilt **S + M > Q**? Übpaseigt de Datenhoudbarkeit plus de migratieszeit de geschätzte Zeit bis tot een CRQC? activa, bij denen de Ungleichung am schärfsten ausfällt – langlebige sensible Daten op Infrastruktur, deren migratie jaare dauert –, rücken aan de begin de Warteschlange. activa met kurzer Datenhoudbarkeit of reeds modernisierter Infrastruktur kunnen später in Programm angeordnet worden.

In deze Phase wordt de risicoreedschaft des toezichtsrats am sichtbarsten. De Q-waarde, tegen de het Institut plant, is in Kern een strategische Wette op het Tempo des kwantumhardware-Fortschritts. Een konservatives Q (Mitte de 2030er) erzeugt een aggressiveren migratiesplan en een hogere kortetermijn-e Capex-Linooit. Een optimistisches Q (na 2040) erzeugt een entspannteren plan en een hogere Restexposition gegenüber reeds geernteten Daten. Keines is falsch; beide zouden moeten ausdrückliche beslissingen des toezichtsrats zijn, niet implizite Vorgaben de Technologiefunktion.

### Phase 3 – Hybride Bereitstellung

Sobald prioritäre activa identifiziert zijn, zou moeten de Bereitstellung de hybriden Muster folgen, het in Project Leap erprobt werd en van NCSC, ANSSI, BSI en de G7-Fahrplan empfohlen wordt. Een hybride Bereitstellung führt een klassischen en een post-kwantum-Algorithmus parallel uit en vereint de resultaten in een einzigen Hülle. Het Komposit is zowel tegen klassische Angriffe (de klassische Algorithmus hält heute) als tegen kwantumangriffe (de PQC-Algorithmus hält morgen) sicher. Konkret bedeutet het in de praktijk: X25519 kombinooitrt met ML-KEM-768 of ML-KEM-1024 voor de sleutelencapsulatie en ECDSA kombinooitrt met ML-DSA voor Signaturen, sofern doppelte Signaturen operativ umsetzbar zijn.

De Befund uit Project Leap, dat Hybrid „duidelijk, duidelijk schwerer" is als iedere de reinen Varianten, is het ehrliche Gegengewicht tot deze aanbeveling. toezichtsräte zouden moeten met erhöhtem Bedarf aan Rechen- en Speicherkapazität, längeren Handshakes en zusätzlicher Komplexität in de Zertifikatsketten terwijl de Übergangsphase rechnen. De voordeel: Hybrid eliminooitrt de größte einzelne migratiesrisikoquelle – de abrupten Wechsel van een cryptografischen Gongeveerlage tot anderen in een productionsumgebung.

## Was het kostet, en warum Nichtstun meer kostet

De Analyse van Mastercard, [begin 2026 berichtet ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your bank's 2030 Expiry — QNu Labs"), beziffert de wereldwijden PQC-migratieskosten in financieelsektor op 28–42 miljarden US-Dollar. Innerhalb dit Aggregats legt de [RedCompass-Labs- en CMORG-onderzoek ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") tot tatsächlichen institutionellen Ausgaben nahe, dat Tier-1-banken 20–30 miljoenen US-Dollar jährlich in Vorbereitungsprogramme stecken, met Implementierungszeiträumen over mehrere Führungs­zyklen. Het zijn erhebliche Zahlen. U zijn echter niet de relevante Vergleich.

De relevante Vergleich is de prijs een einzelnen retrospektiven ontsleutelingsereignisses. Für een Institut, dessen geernteter betalingsverkeer, dessen M&A-Korrespondenz of dessen Gegenpartei-Exposure-Daten 2032 voor een Gegner lesbar worden, is de operative en reputative Schaden niet door de migraties-Capex-Linooit begrenzt. Hij is door de waarde des darunterliegenden jaarzehnts strategischer Informationen begrenzt – en de is voor ieder systemrelevante Institut materiell größer als ieder plausible migratiesbudget. De Rahmung de G7, de cryptografische Transition als systemisches risicomanagementthema en niet als Technologie-Upgrade tot behandeln, is zutreffend, en toezichtsräte zouden moeten ze op deze Gongeveerlage angehen.

Es gibt een zweite kostenlinooit, de es wert is, abgetrennt tot worden. De migratie tot PQC is een Zwangsfunktion voor cryptografische Agilität – de architektonische Fähigkeit, cryptografische Algorithmen auszutauschen, zonder de op ihnen aufzettenden systeeme nieuw tot bouwen. De meisten Institute verfügen heute niet over cryptografische Agilität; haar RSA- en ECC-Abhängigkeiten zijn tief in PAIs, Code-Signing-Ketten, Lieferantenintegrationen en over jaarzehnte gewachsene Hausprotokolle eingebettet. De onder de Druck de PQC-Transition getätigte Agilitätsinvestition is langlebig. U wordt ook bij nächsten cryptografischen Übergang wieder beansprucht – sei es een Nachfolger de rooster-gebaseerde PQC, een QKD-Überlagerung of ongeveers, het nog niet op de standaards-routekaart steht. Richtig behandelt, is de PQC-migraties-Capex een einmalige investering met wiederkehrender Optionalität.

## Fazit

De Fall, de post-kwantummigratie 2026 als toezichtsrats-Priorität tot behandeln, beruht niet op de unmittelbaren Bevorstehung een CRQC. Schätzungen dazu bleiben tatsächlich unsicher – glaubwürdige wissenschaftliche Einschätzungen veranschlagen de Wahrscheinlichkeit een CRQC bis 2028 duidelijk onder een Prozent, steigend op ongeveer fünfzig Prozent bis 2037–2040. De Fall beruht op drei anderen Beobachtungen, de niet unsicher zijn.

Erstens: HNDL findet heute statt, en Daten met een Vertraulichkeitsanforderung van een jaarzehnt of meer zijn exponooitrt, onafhankelijk daarvan, wann de CRQC eintrifft. Zweitens: De migratie des cryptografischen inventariss een grooten financieelinstituts dauert ook bij angemessener financieelierung en Führungs­aufmerksamkeit fünf bis sieben jaare – het 2026 begonnene Programm endet daarmee ongeveer 2031, was duidelijk innerhalb des konservativen eindes de CRQC-Wahrscheinlichkeitsverteilung liegt. Drittens: De aufsichtsrechtlichen Erwartungen hebben sich in de letzten zwölf maanden materiell verschärft, en de Institute, deren toezichtsratsprotokolle voor 2026 een duidelijkes PQC-Programm dokumentieren, worden in een duidelijk stärkeren Position zijn als jene, de alleen een beobachtende Houdung festhouden.

Institute, de jetzt beginnen, hebben de voordeel de Wahl. U kunnen de Arbeit over Führungszyklen hinweg phasieren, ze in breitere Resilienzinitiativen einbetten en de operativen kosten de hybriden Bereitstellung in normaler Kapitalplanung verarbeiten. Institute, de warten, worden derselben Arbeit onder engeren Fristen, met minder Spielraum voor Phasenführung en vóór de achtergrond wachsender knelpunten bij PQC-fähiger Hardware, Expertise en Lieferantenkapazität gegenübpasehen. De kosten frühen Handelns zijn bekannt; de kosten späten Handelns zijn asymmetrisch in nauwkeurig jener Weise, de risicomanagement vermeiden zou.

Zur Einordnung op deze Website: De [Beitrag vom April 2026 tot Verdichtung de kwantumdrempels](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") betrachtete de zugongeveereliegende Hardware-Bahn, de [Analyse tot CRYSTALS-Kyber van November 2023](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") behandelte de mathematischen Gongeveerlagen, de nun als ML-KEM gestandaardiseerd zijn, de [Beitrag tot Quantum Key Distribution van december 2023](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution revolutionising Security in banking") thematisierte de komplementäre [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html)-Überlagerung, en de [open source-Referenzimplementierung KyberLib](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") levert een produktive Rust-Implementierung de zugongeveere liegenden Primitive voor Institute, de de cryptografische Fläche direkt prüfen wollen. Sich op de praktischen en technischen Details einzulassen – niet alleen op de aufsichtsrechtlichen Schlagzeilen – is de Art, zoals toezichtsräte glaubwürdige migratiesprogramme van Compliance-Theater unterscheiden.

## Veelgestelde vragen

**Wann wordt een cryptografisch relevanter kwantumcomputers tatsächlich existieren?**

Glaubwürdige Schätzungen variieren stark. begin 2026 hebben öffentliche kwantumdemonstrationen ongeveer 24 bis 28 logische Qubits erreicht, terwijl een CRQC schätzungsweise ongeveer 6.000 logische Qubits vereist, gestützt door 100.000 bis mehrere miljoenen physische Qubits, je na aanpak de Fehlerkorrektur. De Expertenkonsens veranschlagt de CRQC-Wahrscheinlichkeit bis 2028 op minder als een Prozent, um 2037–2040 op ongeveer fünfzig Prozent, bij erheblicher Streuung de Prognosen. Jüngste Reduktionen theoretischer Ressourcenschätzungen – van 20 miljoenen Qubits vóór wenigen jaaren op minder als een miljoen in Gidneys Arbeit van 2025 en op ongeveer 100.000 in QLDPC-Architekturpaper vom februari 2026 – hebben de planungshorizont verkürzt. Für toezichtsräte is de angemessene planungsannahme: Mitte de 2030er jaare voor Hochrisikosysteme, einde de 2030er als konservativer Mittelpunkt en früher, sofern de HNDL-Exposition het bindende Anliegen is.

**Warum hybride Bereitstellung statt reiner post-kwantum-Bereitstellung?**

Drei Gründe. Erstens hebben ML-KEM en ML-DSA, obwohl sorgfältig geprüft, kürzere kryptanalytische Historien als RSA en ECC. Een Hybrid bleibt sicher, solange een Komponente hält; een reines PQC-Schema is exponooitrt, falls het Gitterproblem unerwartet geschwächt wordt. Zweitens wahrt Hybrid de Rückwärtskompatibilität met Gegenparteien, de nog niet gemigreerd zijn – kritisch in een mehrjährigen sectorntransition. Drittens empfiehlt met Ausnahme des Australian Signals Directorate iedere maßgebliche instantie ausdrücklich Hybrid voor de Übergangsphase: NCSC, ANSSI, BSI, NLNCSA en de G7-Rahmen untpasützen de Doppelhüllen-aanpak. De prijs, zoals Project Leap quantifiziert heeft, is een materiell hogerer Rechen- en Speicher-Overhead. Het is de prijs de Optionalität.

**Brauchen we zowel ML-KEM als ML-DSA, of kunnen we wählen?**

Beide. ML-KEM en ML-DSA übernehmen unterschiedliche cryptografische Rollen. ML-KEM erzet de sleuteletablierungs-Primitive in TLS, VPNs, mobiler Authentifizierung en vergelijkbaaren Protokollen, in denen zwei Parteien een gezamenlijken symmetrischen sleutel aushandeln moeten. ML-DSA erzet de digitaale Signatur-Primitive in PAI-Zertifikaten, Code-Signing, Dokumentensignooitrung, SWIFT-vergelijkbaarem authentifiziertem berichtenverkehr en Identitätsaussagen. Het cryptografische inventaris een Instituts benut beide Primitivtypen aan unterschiedlichen Stellen; de migratie moet beide adressieren. De duidelijk größere Signaturgröße van ML-DSA (50–70× ECDSA) is operativ in de Regel de anspruchsvollere Komponente; de netwerk- en Speicherplanung voor ML-DSA dominooitrt de meisten migratieskapazitätsbewertungen.

**Wie misst man de Fortschritt in een Programm deze grootte?**

Drei Kennzahlen zijn praktikabel en decken sich met de maßgeblichen regelgevingskader. **Abdeckung de CBOM** – welcher Anteil de asymmetrischen cryptografischen instanties des Instituts inventarisiert, klassifiziert en met migratiespriorität versehen werd. **migraties­abdeckung de Hochrisiko-Assets** – welcher Anteil de activa, bij denen Moscas voorwaarde S + M > Q zutrifft, op hybride PQC umgestelt werd. **Abdeckung de cryptografischen Agilität** – welcher Anteil de cryptografisch abhängigen systeeme Algorithmen zonder Code-Änderungen, allein per Konfiguration, austauschen kan. De G7-CEG-Fahrplan, de NCSC-Drei-Phasen-Rahmen en de koordinooitrte EU-Fahrplan decken sich in Wesentlichen met deze drei Maßzahlen, ook indien de Terminologie unterschiedlich is.

**Was kostet es, een weiteres jaar tot warten?**

Nicht null, en niet symmetrisch. Een jaar Wartezeit verwirkt een jaar HNDL-bescherming voor langlebige Daten – Daten, deren Vertraulichkeitsanforderung bis 2040 reicht, zijn een jaar länger exponooitrt als nötig. Es verkürzt het migratiesfenster gegenüber festen regelgevenden Fristen (ASD 2030, NSA-CNSA-2.0-Meilensteine, EU-Ziel 2030 voor kritische systeeme), was sich in hogerem Lieferrisiko en geringerer Phasenflexibilität nooitderschlägt. Es exponooitrt het Institut gegenüber reeds sichtbaren Angebots-knelpuntenn bij Lieferanten en Talenten, de sich verschärfen worden, sobald de größten actoren de sector van planung tot Umsetzung übergehen. De kosten zijn in een einzelnen jaar niet katastrophal, maar ze kumulieren, en de regelgevende Umgebung konvergiert tot een Lage, in de toezichtsräte de vertraging erklären moeten statt de Ausgaben.

## Quellen

- Sebastien Rousseau, (2026). [Quantum Thresholds Are Moving Again](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Sebastien Rousseau, (2023). [Quantum Key Distribution revolutionising Security in banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution revolutionising Security in banking").
- Sebastien Rousseau, (2023). [KyberLib: A Rust-Powered Shield Against Quantum Threats](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats").
- G7 Cyber Expert Group, (2026). [Advancing a Coordinated routekaart for the Transition to Post-Quantum Cryptography in the Financial Sector ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement, januariy 2026"). GOV.UK.
- bank for International settlements, (2025). [Project Leap Phase 2: Quantum-Proofing Payment systeems ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"). BIS.
- bank for International settlements, (2025). [Project Leap: Quantum-Proofing the Financial systeem ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"). BIS.
- NIST, (2024). [FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism standaard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism standaard"). NIST.
- UK NCSC, (2025). [Timelines for migratie to Post-Quantum Cryptography ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines "Timelines for migration to post-quantum cryptography — NCSC"). UK National Cyber Security Centre.
- CMORG, (2025). [Guidance for Post-Quantum Cryptography ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"). Cross-Market Operational Resilience Group.
- Post-Quantum Cryptography Coalition, (2025). [International PQC Requirements ⧉](https://pqcc.org/internationaal-pqc-requirements/ "International PQC Requirements — Post-Quantum Cryptography Coalition"). PQCC.
- PQShield, (2025). [PQC routekaarts and Transition Guidance ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC routekaarts and Transition Guidance"). PQShield.
- banking.Vision, (2026). [The Year of Quantum Computing: 2026 ⧉](https://banking.vision/en/the-year-of-quantum-computing/ "The Year of Quantum Computing 2026"). banking.Vision / msg for banking.
- The Quantum Insider, (2026). [How to Prep For Post-Quantum Cryptography: G7 Releases routekaart ⧉](https://thequantuminsider.com/2026/01/15/how-to-prep-for-post-quantum-crytography-g7-releases-roadmap-to-help-financial-sector-navigate-transition-to-quantum-era/ "How to Prep For Post-Quantum Cryptography — The Quantum Insider"). The Quantum Insider.
- Quantum Computing Report, (2026). [Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates ⧉](https://quantumcomputingreport.com/shor-qldpc-codes-and-the-compression-of-rsa-2048-resource-estimates-part-i/ "Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates"). Quantum Computing Report.
- Cryptomathic, (2025). [A banker's Guide to Quantum Safe Cryptography — routekaart to PQC migratie for Financial Institutions ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A banker's Guide to Quantum Safe Cryptography"). Cryptomathic.
- Forrester, (2025). [2026 Asia Pacific Predictions: Quantum Security ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"). Forrester Research.
- The Asian banker, (2025). [Building Resilience for a Quantum-Ready Financial systeem ⧉](https://www.theasianbanker.com/updates-and-articles/building-resilience-for-a-quantum-ready-financial-system "Building resilience for a quantum-ready financial system"). The Asian banker.
