---
title: "Quantensichere Zahlungen: Warum die Branche jetzt handeln muss"
subtitle: "Post-Quanten-Kryptografie ist eine gegenwärtige Infrastrukturentscheidung, keine zukünftige. Das EPAA-Whitepaper legt das strukturelle Risiko und den dringenden Migrationsbedarf dar."
description: "Quantencomputing bedroht die Kryptografie der Zahlungssysteme. Das EPAA-Whitepaper beschreibt das strukturelle Risiko und begründet die dringende Notwendigkeit einer PQC-Migration."
date: "September 01, 2025"
language: "de"
locale: "de_DE"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Quantencomputing-Leiterplatte in blauem Licht"
keywords: "quantensichere Zahlungen, Post-Quanten-Kryptografie, SEPA, SWIFT gpi, ISO 20022, Sicherheit im Finanzdienstleistungssektor, EPAA, Harvest-Now Decrypt-Later, kryptografische Agilität, Sebastien Rousseau"
---

## Die Quantenbedrohung für Zahlungssysteme

Moderne Zahlungsinfrastrukturen stützen sich auf Public-Key-Kryptografie – RSA, ECC und Diffie-Hellman –, um Transaktionen zu authentifizieren, Karteninhaberdaten zu schützen und die Nachrichtenübermittlung zwischen Finanzinstituten abzusichern. Diese Algorithmen bilden das Fundament von SWIFT, SEPA, Echtzeit-Brutto-Settlement-Systemen sowie praktisch jedem heute betriebenen Kartensystem.

Quantencomputer, die Shors Algorithmus ausführen, werden in der Lage sein, diese kryptografischen Primitive zu brechen. Auch wenn fehlertolerante Quantenmaschinen in der erforderlichen Größenordnung noch nicht existieren, macht die Entwicklung der Hardware – belegt durch IBM, Google und andere – dies zu einer Frage des Engineering-Zeitplans und nicht der Theorie. Das National Institute of Standards and Technology (NIST) hat als Reaktion bereits seinen ersten Satz an Post-Quanten-Kryptografiestandards (FIPS 203, 204 und 205) finalisiert.

## Das Risiko „Jetzt ernten, später entschlüsseln“

Die Bedrohung beschränkt sich nicht auf einen künftigen Zeitpunkt, an dem Quantencomputer eine ausreichende Leistungsfähigkeit erreichen. Staatliche Akteure und versierte Angreifer fangen bereits heute verschlüsselte Daten ab und speichern sie mit der Absicht, sie zu entschlüsseln, sobald entsprechende Quantenressourcen verfügbar sind. Diese Strategie des „Harvest-Now Decrypt-Later" (HNDL) bedeutet, dass alle Zahlungsdaten mit langfristiger Sensitivität – aufsichtsrechtliche Aufzeichnungen, Compliance-Archive, vertragliche Verpflichtungen – bereits jetzt gefährdet sind.

Finanzaufsichtsbehörden beginnen zu reagieren. Die Monetary Authority of Singapore (MAS) hat Leitlinien zur Quantenbereitschaft veröffentlicht. Die Australian Prudential Regulation Authority (APRA) hat das kryptografische Risiko in ihrem Rahmenwerk zur technologischen Resilienz hervorgehoben. Der Digital Operational Resilience Act (DORA) der Europäischen Union schreibt ein IKT-Risikomanagement vor, das aufkommende Bedrohungen, einschließlich Quantencomputing, berücksichtigen muss.

## Auswirkungen auf alle Zahlungsschienen

Die Implikationen erstrecken sich über die gesamte Breite der Zahlungsinfrastruktur:

**SWIFT-Nachrichtenverkehr:** Die Nachrichtenformate MT und MX stützen sich auf TLS und digitale Signaturen für Integrität und Authentifizierung. Eine kompromittierte Schlüsselinfrastruktur würde das Vertrauensmodell untergraben, das weltweit über 11.000 Institute miteinander verbindet.

**SEPA und Instant Payments:** Das SEPA-Instant-Credit-Transfer-Schema des European Payments Council verarbeitet unwiderrufliche Transaktionen in unter zehn Sekunden. Eine kryptografische Kompromittierung bei dieser Geschwindigkeit lässt kein Zeitfenster für manuelles Eingreifen oder manuelle Verifikation.

**Echtzeit-Zahlungssysteme:** Faster Payments (UK), FedNow (US) und NPP (Australien) teilen sämtlich dieselbe Abhängigkeit von klassischen kryptografischen Primitiven zur Nachrichtenauthentifizierung und Teilnehmerverifizierung.

**Compliance und langlebige Daten:** Zahlungsdatensätze, die zu aufsichtsrechtlichen Zwecken aufbewahrt werden – häufig für fünf bis zehn Jahre oder länger vorgeschrieben – werden die Sicherheitsgarantien der Kryptografie, die sie zum Zeitpunkt ihrer Erzeugung schützte, überdauern. Migrationsprogramme für [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) müssen die kryptografische Haltbarkeit der erzeugten Daten berücksichtigen.

**Blockchain und Distributed-Ledger-Technologie:** Plattformen für digitale Vermögenswerte und tokenisierte Zahlungsinstrumente, die auf Elliptische-Kurven-Kryptografie setzen, sehen sich einer direkten und gut verstandenen Bedrohung durch Quantenalgorithmen gegenüber.

## Was Organisationen jetzt tun müssen

Der Übergang zu quantensicherer Kryptografie ist keine einmalige Aktualisierung, sondern ein mehrjähriges Programm, das strukturierte Vorbereitung erfordert:

**Kryptografisches Inventar:** Organisationen müssen jedes System, jedes Protokoll und jeden Datenspeicher katalogisieren, der von klassischer Public-Key-Kryptografie abhängt. Dazu gehören TLS-Zertifikate, API-Authentifizierung, HSM-Konfigurationen, Schlüsselverwaltungssysteme und Verschlüsselung ruhender Daten.

**Einführung von Post-Quanten-Algorithmen:** NIST hat ML-KEM (FIPS 203) für die Schlüsselverkapselung und ML-DSA (FIPS 204) für digitale Signaturen standardisiert. Organisationen sollten beginnen, diese Algorithmen in Nicht-Produktivumgebungen zu testen und Migrationsfahrpläne für kritische Systeme zu entwickeln.

**Kryptografische Agilität:** Systeme müssen so konzipiert – oder refaktoriert – werden, dass kryptografische Algorithmen ohne vollständige Neuentwicklung der Anwendungen ausgetauscht werden können. Dieses Prinzip gilt gleichermaßen für Zahlungs-Gateways, Messaging-Middleware und kundennahe APIs.

**Hybride Ansätze:** Während der Übergangsphase bieten hybride kryptografische Verfahren, die klassische und Post-Quanten-Algorithmen kombinieren, eine gestaffelte Verteidigung. Dieser Ansatz wahrt die Rückwärtskompatibilität und führt zugleich Quantenresistenz ein.

## EPAA-Arbeitsgruppe und Branchenzusammenarbeit

Die Emerging Payments Association Asia (EPAA) hat ihre Quantum Safe Cryptography Working Group eingerichtet, um diese Herausforderungen durch koordiniertes Handeln der Branche zu adressieren. Die Arbeitsgruppe bringt Teilnehmer aus dem gesamten Zahlungsökosystem zusammen, darunter IBM, HSBC, KPMG, JPMorgan Chase und PayPal.

In Workshops in Sydney, Hongkong und Singapur hat die Arbeitsgruppe einen gemeinsamen Rahmen zur Bewertung des Quantenrisikos in Zahlungssystemen und zur Identifizierung praktikabler Migrationspfade entwickelt. Das daraus hervorgegangene Whitepaper – [Quantum-Safe Payments: Why the Payments Industry Must Act Now][epaa] – stellt eine Konsensposition zur Dringlichkeit und zum Umfang der Herausforderung dar.

Die Analyse der Arbeitsgruppe kommt zu dem Schluss, dass die Quantenbereitschaft eine gegenwärtige Infrastrukturentscheidung ist, keine zukünftige. Organisationen, die zögern, riskieren, regulatorische Erwartungen nicht mehr erfüllen, langlebige Daten nicht mehr schützen oder die Interoperabilität mit bereits migrierten Partnern nicht mehr aufrechterhalten zu können.

## Über den Autor

Sebastien Rousseau ist Senior Digital Product Manager bei der HSBC Bank plc, wo er die Corporate-Payments-API-Produkte innerhalb der Commercial & Investment Bank von HSBC verantwortet. Er hat zur EPAA Quantum Safe Cryptography Working Group beigetragen und forscht zur Anwendung von Post-Quanten-Kryptografie im Finanzdienstleistungssektor. [Mehr über Sebastien erfahren ❯][00]

## Verwandte Artikel

- [[Quantum Key Distribution](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html): Sicherheit im Bankwesen revolutionieren][rel1]
- [[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html): Der Schutzalgorithmus im Quantenzeitalter][rel2]

[00]: /about/index.html "Über Sebastien Rousseau"
[epaa]: https://emergingpaymentsasia.org/wp-content/uploads/2025/09/Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf "EPAA Quantum-Safe Payments Whitepaper"
[rel1]: /2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking"
[rel2]: /2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age"
