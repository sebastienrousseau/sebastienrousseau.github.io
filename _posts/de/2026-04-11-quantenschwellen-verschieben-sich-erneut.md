---
title: "Quantenschwellen verschieben sich erneut"
subtitle: "Ein neuer Aufsatz legt nahe, dass Shors Algorithmus auf nur 10.000 Qubits laufen könnte. Die Schwelle für kryptografisch relevantes Quantencomputing fällt schneller als allgemein angenommen."
description: "Ein neuer Aufsatz legt nahe, dass Shors Algorithmus auf nur 10.000 Qubits laufen könnte. Die Schwelle für kryptografisch relevantes Quantencomputing fällt schneller als allgemein angenommen."
date: "April 11, 2026"
language: "de"
locale: "de_DE"
banner: "https://cloudcdn.pro/stocks/images/leo_visions-Q_y8ZzhQ2_s-unsplash.webp"
banner_alt: "Diagramm der Qubit-Schwelle für Shors Algorithmus. Quantencomputing-Leiterplatte mit blauen Lichtmustern"
keywords: "Shors Algorithmus, Qubits, Quantencomputing, ECC, RSA-2048, rekonfigurierbare neutrale Atome, Fehlerkorrekturcodes, CRYSTALS-Kyber, CRYSTALS-Dilithium, PQC, Post-Quanten-Kryptografie"
---

## Quantenschwellen verschieben sich erneut

Ein neuer Aufsatz legt nahe, dass Shors Algorithmus auf nur 10.000 Qubits laufen könnte. Die Schwelle für kryptografisch relevantes Quantencomputing fällt schneller als allgemein angenommen.

> **Wesentliche Erkenntnisse**
>
> - Ein neuer Aufsatz schlägt vor, dass Shors Algorithmus auf nur **10.000 physischen Qubits** ausführbar sein könnte – rund hundertmal weniger als bisherige Konsensschätzungen.
> - Die Reduktion wird durch drei konvergierende Fortschritte getragen: hochrate-Quantenfehlerkorrekturcodes, rekonfigurierbare Anordnungen neutraler Atome und erhöhte Parallelität.
> - Die Bedrohung ist nicht einheitlich. **Elliptische-Kurven-Kryptografie (ECC)** ist bei geringeren Qubit-Zahlen anfälliger; RSA-2048 erfordert in vergleichbaren Größenordnungen deutlich längere Laufzeiten.
> - Es handelt sich um eine **theoretische Projektion**, nicht um eine funktionierende Demonstration. Eine erhebliche Engineering-Lücke bleibt zwischen aktueller Hardware und fehlertolerantem Betrieb in dieser Größenordnung.
> - Post-Quanten-Kryptografiestandards sind bereits finalisiert. Die Priorität liegt nun darauf, **die Migration zu beschleunigen** – nicht darauf, auf das Erscheinen eines Quantensystems zu warten.

## Eine vertraute Annahme, nun unter Druck

Im vergangenen Jahrzehnt folgten Diskussionen um Quantencomputing und Kryptografie einem vertrauten Bogen. Quantenmaschinen galten als theoretisch leistungsfähig, jedoch im großen Maßstab als unpraktikabel. Moderne kryptografische Systeme zu brechen hätte Millionen physischer Qubits erfordert, und der Zeithorizont blieb komfortabel fern. Diese Annahme steht inzwischen ernsthaft unter Druck.

Ein jüngst erschienener Aufsatz, [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/pdf/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (PDF)"), schlägt etwas Folgenreicheres vor als einen einzelnen Durchbruch. Er legt nahe, dass die Schwelle für kryptografisch relevantes Quantencomputing eine Größenordnung niedriger liegen könnte als bislang angenommen. Nicht Millionen Qubits, sondern Zehntausende. Die Unterscheidung ist bedeutsam, und die damit angedeutete Richtung lässt sich schwer ignorieren.

## Die Konvergenz hinter der Verschiebung: Fehlerkorrektur, Architektur und Parallelität

Das Ergebnis entsteht nicht aus einer einzelnen Entdeckung. Es spiegelt eine Konvergenz von Verbesserungen über mehrere Schichten des Quantencomputing-Stacks wider, die zusammengenommen die Grenze des Machbaren verschieben.

Die erste Verbesserung betrifft die Fehlerkorrektur. Klassische Ansätze erforderten hohe Overheads – häufig Hunderte physische Qubits, um ein einzelnes logisches Qubit darzustellen. Der Aufsatz stützt sich stattdessen auf hochrate-Quantenfehlerkorrekturcodes, die diesen Overhead deutlich reduzieren ([Emergent Mind ⧉](https://www.emergentmind.com/papers/2603.28627 "Shor's Algorithm with 10000 Atomic Qubits")). Die zweite betrifft die Architektur. Das System basiert auf rekonfigurierbaren Anordnungen neutraler Atome, die während der Berechnung neu angeordnet werden können, um flexiblere Konnektivität und effizientere Ausführung zu ermöglichen ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")). Die dritte ist Parallelität: Mehr Qubits erlauben es, mehr Operationen gleichzeitig auszuführen und so die Gesamtlaufzeit zu verkürzen.

Keiner dieser Gedanken ist isoliert neu. In Kombination jedoch definieren sie neu, was zuvor als harte Grenze galt.

## Von Millionen zu Zehntausenden: Was die Zahlen wirklich bedeuten

Jahrelang lag die Konsensschätzung für die Ausführung von Shors Algorithmus in kryptografischen Größenordnungen bei Millionen physischer Qubits. Die neue Analyse legt nahe, dass diese Zahl unter bestimmten Annahmen auf rund 10.000 sinken könnte ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")). Diese Zahl ist jedoch nicht das vollständige Bild.

Am unteren Ende dieses Bereichs bleiben die Laufzeiten lang. Die Faktorisierung von RSA-2048 mit der minimalen Qubit-Zahl könnte weiterhin Jahre kontinuierlichen Betriebs erfordern. Schnellere Ausführung verlangt mehr Qubits – potenziell Zehntausende. Die Beziehung zwischen Qubit-Zahl und Laufzeit ist nicht linear, und der Aufsatz präsentiert dies sorgfältig als Spektrum statt als feste Schwelle. Was sich verändert, ist die Richtung: Die Hürde ist nicht mehr rein theoretisch. Sie ist nun eine Frage des Engineerings.

### Alte Annahmen gegen neue Realitäten

| Dimension | Alte Annahme | Neue Realität |
|---|---|---|
| Erforderliche physische Qubits (Shors Algorithmus) | ~1.000.000+ | ~10.000–26.000 |
| Zeit zum Brechen von RSA-2048 (bei minimaler Qubit-Zahl) | In diesem Jahrzehnt nicht machbar | Jahre (bei 10.000 Qubits); schneller mit mehr |
| Zeit zum Brechen von ECC-256 | In diesem Jahrzehnt nicht machbar | Tage (geschätzt bei ~26.000 Qubits) |
| Dominantes Hardware-Paradigma | Supraleitende Qubits | Rekonfigurierbare Anordnungen neutraler Atome |
| Fehlerkorrektur-Overhead | Hunderte physische Qubits je logischem Qubit | Deutlich reduziert durch hochrate-Codes |
| Natur der Hürde | Theoretisch | Engineering |
| Migrationsdringlichkeit | Langfristige Planung | Aktive Umsetzung jetzt erforderlich |

*Quelle: Analyse auf Basis von [arXiv:2603.28627 ⧉](https://arxiv.org/abs/2603.28627) und früherer Literatur.*

## Zeit, Skalierung und die ungleiche Verwundbarkeit kryptografischer Systeme

Einer der bedeutendsten Beiträge des Aufsatzes ist die Nuance, die er in Bezug auf Zeit einführt. Quantenvorteil erscheint nicht auf einen Schlag. Er existiert entlang eines Spektrums, das durch die Größe des Systems und die Art des kryptografischen Ziels bestimmt wird.

Mit rund 26.000 Qubits schätzen die Autoren, dass das Brechen der Elliptische-Kurven-Kryptografie unter günstigen Bedingungen Tage dauern könnte ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")). Für RSA-2048 sind die Zeitskalen erheblich länger. Diese Asymmetrie ist wichtig. Sie legt nahe, dass unterschiedliche kryptografische Systeme zu unterschiedlichen Zeitpunkten verwundbar werden können – nicht gleichzeitig – und dass der Übergang zu Post-Quanten-Standards wahrscheinlich kein einzelnes Ereignis mit einer einzigen Frist sein wird.

Dieses Muster steht im Einklang mit der breiteren Berichterstattung. Analysen der letzten Monate legen nahe, dass Quantensysteme, die weit verbreitete Verschlüsselung herausfordern könnten, vor Ende des Jahrzehnts entstehen könnten ([Nature ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption")). Regierungen und Normungsgremien planen bereits Übergänge zur Post-Quanten-Kryptografie, mit Umsetzungsfristen, die bis in die 2030er Jahre reichen ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")). Die Diskussion ist vom „Ob" zum „Wann" übergegangen.

## Die verbleibende Engineering-Lücke

Es ist wichtig, präzise zu benennen, was dieser Aufsatz darstellt. Er ist eine Projektion, keine Demonstration. Die vorgeschlagenen Systeme hängen von Annahmen über Fehlerraten, Hardwarestabilität und Skalierungsverhalten ab, die in der erforderlichen Größenordnung noch nicht validiert wurden. Aktuelle Experimente operieren auf der Ebene von Hunderten bis wenigen Tausend Qubits – nicht Zehntausenden, die über längere Zeiträume fehlertolerant arbeiten ([Phys.org ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits")).

Eine erhebliche Engineering-Lücke bleibt bestehen. Der Weg von einem überzeugenden theoretischen Modell zu einem funktionierenden System, das in dieser Größenordnung dauerhaft fehlertolerant arbeitet, beinhaltet Herausforderungen, die noch nicht vollständig verstanden, geschweige denn gelöst sind. Was sich verändert hat, ist nicht die Nähe einer funktionierenden Maschine, sondern die Glaubwürdigkeit des Ziels. Die Lücke verengt sich, und die Richtung des Fortschritts ist konsistent.

## Warum der sich verdichtende Zeithorizont jetzt Aufmerksamkeit verlangt

Die Bedeutung dieser Arbeit liegt nicht darin, dass Kryptografie kurzfristig gebrochen wird. Sie liegt darin, dass sich der Zeithorizont auf eine Weise verdichtet, die heute zu treffende Entscheidungen beeinflusst. Sicherheitssysteme werden mit langen Lebenszyklen im Blick konzipiert. Heute verschlüsselte Daten müssen unter Umständen jahrzehntelang vertraulich bleiben. Infrastrukturentscheidungen, die in diesem Jahr getroffen werden, lassen sich in einem Fünfjahresfenster nur schwer revidieren. Treffen Quantenfähigkeiten früher ein als erwartet, werden diese Annahmen fragil.

Aus diesem Grund wird Post-Quanten-Kryptografie bereits in kritischen Sektoren ausgerollt. Nicht weil die Bedrohung unmittelbar wäre, sondern weil der Übergang Zeit braucht und die Kosten einer Verzögerung asymmetrisch sind. Es gibt ein wiederkehrendes Muster in der Geschichte des Computings: Fortschritt erscheint langsam, bis er es plötzlich nicht mehr ist. Was als theoretische Verbesserung beginnt, wird zur praktischen Restriktion, und was einst als fern abgetan wurde, wird zu etwas, das einzuplanen ist. Quantencomputing könnte exakt diese Bahn nehmen – nicht durch einen einzelnen dramatischen Durchbruch, sondern durch stetige Reduktionen bei Kosten, Komplexität und Maßstab.

## Was das je Branche bedeutet: ein praktischer Leitfaden

Die Implikationen dieser Forschung sind branchenübergreifend nicht einheitlich. Die angemessene Reaktion hängt von der Art der gefährdeten kryptografischen Vermögenswerte ab, von der Sensitivität und Langlebigkeit der betroffenen Daten und vom Tempo, in dem sich regulatorische Erwartungen bewegen.

### Finanzdienstleistungen und FinTech

Finanzinstitute stehen vor einem zusammengesetzten Risiko: Sie halten langlebige sensible Daten, betreiben Infrastrukturen mit langsamen Erneuerungszyklen und unterliegen einer zunehmenden aufsichtsrechtlichen Prüfung in Bezug auf kryptografische Resilienz. ECC wird in TLS-Verbindungen, mobiler Authentifizierung und digitalen Signaturen über alle Zahlungsschienen hinweg breit eingesetzt – jene kryptografische Kategorie, die der Aufsatz als bei geringeren Qubit-Zahlen am anfälligsten identifiziert. Institute, die noch keine kryptografische Bestandsaufnahme begonnen oder einen Post-Quanten-Migrationsplan initiiert haben, sollten diesen Aufsatz als Anstoß zur Beschleunigung verstehen, nicht als Grund zur Panik. [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) und CRYSTALS-Dilithium, beide inzwischen von NIST standardisiert, sind die geeigneten Migrationsziele für Schlüsselverkapselung beziehungsweise digitale Signaturen.

### Öffentlicher Sektor und Verteidigung

Staatliche Akteure haben die stärkste Motivation – und in vielen Fällen die Ressourcen –, die Quantenhardware-Entwicklung über das öffentlich Bekannte hinaus zu beschleunigen. Regierungen, die sensible Kommunikation, nachrichtendienstliche Daten oder Schlüssel kritischer Infrastrukturen verwalten, müssen davon ausgehen, dass Gegner bereits verschlüsselte Daten für eine spätere Entschlüsselung sammeln – eine Strategie, die gemeinhin als „Harvest now, decrypt later" bezeichnet wird. Für Organisationen des öffentlichen Sektors wird die Einhaltung nationaler Quantum-Readiness-Vorgaben zunehmend unumgänglich, und das Zeitfenster für eine proaktive Migration verengt sich.

### Gesundheitswesen und kritische Infrastrukturen

Patientenakten, Steuerungssysteme von Versorgern und Industrienetze teilen eine gemeinsame Verwundbarkeit: Daten und Systeme mit sehr langen operativen Lebenszyklen, geschützt durch kryptografische Standards, die für ein vorquantisches Bedrohungsmodell konzipiert wurden. Eine heute verschlüsselte medizinische Aufzeichnung muss möglicherweise fünfzig Jahre lang privat bleiben. Ein in diesem Jahr zertifiziertes Steuerungssystem kann zwei Jahrzehnte im Einsatz bleiben. Für diese Sektoren ist der sich verdichtende Zeithorizont keine abstrakte Sorge. Er ist eine direkte Herausforderung der grundlegenden Annahmen hinter den heutigen Sicherheitsarchitekturen.

## Fazit

Der wichtigste Aspekt dieses Aufsatzes ist nicht die konkrete Qubit-Zahl, die er nennt. Es ist die Richtung, die sie impliziert. Die Frage ist nicht mehr, ob Quantencomputer die moderne Kryptografie herausfordern können. Sie lautet, wie schnell die erforderlichen Systeme gebaut werden können – und ob die Organisationen, die auf den heutigen Standards aufsetzen, schnell genug reagieren.

Vorerst bleiben die Antworten ungewiss. Doch der Spielraum, die Frage aufzuschieben, verengt sich, und die Kosten des Wartens wachsen mit jeder glaubhaften Senkung der theoretischen Schwelle. Die kryptografische Gemeinschaft, Sicherheitsverantwortliche und die auf sie angewiesenen Branchen täten gut daran, diesen Aufsatz nicht als Anlass zur Beunruhigung zu betrachten, sondern als ernsthaften Anstoß, bereits laufende Übergänge zu beschleunigen.

## Häufig gestellte Fragen

**Können 10.000 Qubits RSA-Verschlüsselung wirklich brechen?**

Theoretisch ja – mit wichtigen Einschränkungen. Während frühere Schätzungen Millionen physischer Qubits forderten, legt neue Forschung zu hochrate-Fehlerkorrekturcodes und rekonfigurierbaren Anordnungen neutraler Atome nahe, dass die Schwelle deutlich niedriger liegt. Bei 10.000 Qubits bleibt die geschätzte Laufzeit für die Faktorisierung von RSA-2048 jedoch extrem lang – potenziell Jahre kontinuierlichen Betriebs. Schnellere Angriffe verlangen mehr Qubits, wahrscheinlich im Bereich von Zehntausenden. Der Aufsatz stellt eine Projektion auf Basis modellierter Annahmen dar, keine Demonstration auf einem funktionierenden System.

**Welche Verschlüsselung ist durch Quantencomputing am stärksten gefährdet?**

Elliptische-Kurven-Kryptografie (ECC) ist bei geringeren Qubit-Zahlen im Allgemeinen anfälliger als RSA-2048. Der Aufsatz schätzt, dass das Brechen von ECC unter günstigen Bedingungen Tage dauern könnte – bei rund 26.000 rekonfigurierbaren Qubits. RSA-2048 erfordert bei vergleichbaren Qubit-Zahlen deutlich längere Laufzeiten. Diese Asymmetrie bedeutet, dass ECC-abhängige Systeme – verbreitet in TLS, mobiler Authentifizierung und Blockchain – auf einem kürzeren Zeithorizont gefährdet sein können als RSA-basierte Infrastrukturen.

**Was ist ein rekonfigurierbares Qubit aus neutralen Atomen?**

Qubits aus neutralen Atomen sind einzelne Atome – typischerweise Rubidium oder Cäsium –, die mittels Laserlicht in einer Vakuumkammer eingefangen und manipuliert werden. „Rekonfigurierbar" bedeutet, dass die Anordnung der Atome während der Berechnung dynamisch verändert werden kann, was eine effizientere Ausführung komplexer Quantenschaltkreise ermöglicht. Diese Flexibilität reduziert die Anzahl physischer Qubits, die für fehlertolerante logische Operationen erforderlich sind, und ist ein wesentlicher Grund, weshalb der neue Aufsatz niedrigere Qubit-Schätzungen erreicht als frühere Arbeiten auf Basis supraleitender Qubit-Architekturen.

**Was ist Post-Quanten-Kryptografie, und warum wird sie jetzt eingeführt?**

Post-Quanten-Kryptografie (PQC) bezeichnet kryptografische Algorithmen, die sowohl gegen klassische als auch gegen Quantencomputer als sicher gelten. NIST hat 2024 seinen ersten PQC-Standardsatz finalisiert, darunter [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) für die Schlüsselverkapselung und CRYSTALS-Dilithium für digitale Signaturen. Die Einführung beginnt jetzt – weit bevor Quantencomputer eine unmittelbare Bedrohung darstellen –, weil kryptografische Übergänge langsam verlaufen. Eingebettete Standards in der globalen Infrastruktur auszutauschen, dauert in der Regel ein Jahrzehnt oder länger, und heute verschlüsselte Daten müssen unter Umständen lange nach der Reifung der Quantenfähigkeiten vertraulich bleiben.

**Wie viele Qubits hat der heute leistungsfähigste Quantencomputer?**

Anfang 2026 arbeiten führende Quantensysteme im Bereich von Hunderten bis wenigen Tausend physischen Qubits. Entscheidend ist, dass die meisten noch nicht fehlertolerant sind – sie operieren unterhalb der für anhaltende, zuverlässige logische Berechnungen erforderlichen Fehlerkorrekturschwellen. Die Lücke zwischen heutiger Hardware und den im neuen Aufsatz beschriebenen Zehntausenden hochwertiger, fehlertoleranter logischer Qubits bleibt erheblich, auch wenn sich das Fortschrittstempo über die Plattformen Supraleitung, neutrale Atome und Ionenfallen beschleunigt.

## Quellen

- Sebastien Rousseau, (2025). [Quantum-Safe Payments: Why the Payments Industry Must Act Now](https://sebastienrousseau.com/2025-09-01-quantum-safe-payments-epaa/index.html "Quantum-Safe Payments: Why the Payments Industry Must Act Now").
- Sebastien Rousseau, (2023). [Quantum Key Distribution: Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Anonymous, (2026). [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits"). arXiv preprint arXiv:2603.28627.
- Castelvecchi, D. (2026). [Quantum-computing breakthroughs pose risks to encryption ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption"). Nature.
- Phys.org, (2026). [Useful quantum computers could be built with as few as 10,000 qubits ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits"). Phys.org.
