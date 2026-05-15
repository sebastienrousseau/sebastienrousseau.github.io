---
title: "Gitterbasierte Kryptografie: Fehler in Chens LWE-Angriff"
subtitle: "Peer-Review deckt Schwachstelle in Chens bahnbrechender Arbeit auf"
description: "Ein Fehler in Yilei Chens quantenbasiertem LWE-Algorithmus verschafft der gitterbasierten Kryptografie eine vorübergehende Atempause. Was dies für CRYSTALS-Kyber, Dilithium und den PQC-Fahrplan bedeutet."
date: "April 22, 2024"
language: "de"
locale: "de_DE"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Mit MidJourney generiertes Bild – ein Netzwerk digitaler Knoten in roten und blauen Farbtönen."
keywords: "Post-Quanten-Kryptografie, NIST, PQC-Standardisierung, Yilei Chen, Quantenalgorithmus, gitterbasierte Kryptografie, LWE-Problem, CRYSTALS-KYBER, CRYSTALS-Dilithium, quantenresistente Kryptografie"
---

## Das Quanten-Rätsel: Neubewertung der NIST-Post-Quanten-Kryptografie-Standardisierung im Lichte von Yilei Chens Algorithmus

Im Anschluss an meinen jüngsten Artikel über die [Herausforderungen quantenbasierter Algorithmen für die gitterbasierte Kryptografie][00] sehe ich mich veranlasst, eine Aktualisierung zu den neuesten Entwicklungen rund um [Yilei Chens Forschung ⧉][01] zu geben.

In einer unerwarteten Wendung berichtete Yilei Chen, Assistenzprofessor am Institute for Interdisciplinary Information Science (IIIS) der Universität Tsinghua, dass seine Kollegen Hongxun Wu und Thomas Vidick unabhängig voneinander einen Fehler in seinem polynomialzeitigen Quantenalgorithmus zur Lösung des Learning-with-Errors-Problems (LWE) entdeckt haben.

Dieser Fehler macht den Algorithmus unbrauchbar, und Chen hat eingeräumt, dass sein Ansatz nicht hält, was ursprünglich behauptet wurde.

## Der Fehler in Chens Quantenalgorithmus

Der Fehler wurde in Schritt 9 von Chens Algorithmus gefunden, und er hat erklärt, dass er nicht weiß, wie er ihn beheben kann. Diese Entdeckung ist eine Erleichterung für die kryptografische Gemeinschaft, da sie bestätigt, dass das LWE-Problem – eine kritische Komponente der Schutzverfahren in der Post-Quanten-Kryptografie – weiterhin sicher bleibt.

Chens Arbeit untersuchte zudem weitere komplexe Gitterprobleme, etwa das decisional shortest vector problem (GapSVP) und das shortest independent vector problem (SIVP), innerhalb polynomialer Approximationsfaktoren. Auch wenn der Fehler in seinem Algorithmus diese Probleme nicht unmittelbar betrifft, wirft er Fragen zur Robustheit quantenbasierter Algorithmen gegen die gitterbasierte Kryptografie auf.

Doch laut [der Seite von Nigel Smart ⧉][02] ist der vorgeschlagene Quantenangriff auf LWE fehlerhaft und kompromittiert keine gitterbasierten Kryptografieverfahren wie [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06] oder [TFHE ⧉][07].

## Auswirkungen auf den NIST-Standardisierungsprozess für Post-Quanten-Kryptografie

Chens Forschung warf indirekt Bedenken und Zweifel am [NIST-Standardisierungsprozess für Post-Quanten-Kryptografie (PQC) ⧉][03] und an der Auswahl quantenresistenter kryptografischer Algorithmen auf.

Die Verfahren [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) und CRYSTALS-Dilithium, die zu den Finalisten im NIST-PQC-Standardisierungsprozess gehören, sind Beispiele für gitterbasierte kryptografische Verfahren, die rigoros auf ihre Quantenresistenz getestet und bewertet wurden. Es ist jedoch entscheidend, diese Verfahren weiterhin zu prüfen und zu verfeinern, um ihre langfristige Sicherheit und Tragfähigkeit zu gewährleisten.

NIST, die kryptografische Gemeinschaft und Unternehmen müssen wachsam bleiben und weiterhin alternative mathematische Grundlagen für die Post-Quanten-Kryptografie erforschen, damit eine belastbare und vielfältige Auswahl an Optionen für quantenresistente Sicherheit bereitsteht.

## Die Zukunft der Post-Quanten-Kryptografie

Die Entdeckung des Fehlers in Chens Algorithmus unterstreicht die zentrale Rolle der Peer-Review im wissenschaftlichen Prozess. Sie verdeutlicht zudem die Notwendigkeit unmittelbarer Begutachtung, Rückmeldung und Debatte.

Die Quanten-Ära hat begonnen, und die Notwendigkeit, quantenresistente kryptografische Verfahren zu entwickeln, erfordert kooperative Maßnahmen auf globaler Ebene, um die Sicherheit unserer digitalen Infrastruktur angesichts der zunehmenden Leistungsfähigkeit des Quantencomputings und des Wettlaufs um die Quantenüberlegenheit zu gewährleisten.

Der NIST-PQC-Standardisierungsprozess ist ein wichtiger Schritt in diese Richtung, aber er ist erst der Anfang. Der Fehler in Chens Algorithmus ist eine eindringliche Erinnerung an die kommenden Herausforderungen und Unsicherheiten, dient aber zugleich als Aufruf an die kryptografische Gemeinschaft, ihre Anstrengungen zu verdoppeln und die Grenzen des Möglichen weiter zu verschieben.

Dies ist eine faszinierende Entwicklung im Bereich der Post-Quanten-Kryptografie, und es wird spannend zu beobachten sein, wie sich der NIST-PQC-Standardisierungsprozess als Reaktion auf diese neuen Erkenntnisse weiterentwickelt.

## Fazit

Der in Yilei Chens Quantenalgorithmus zur Lösung des LWE-Problems entdeckte Fehler ist ein Beleg für die Bedeutung rigoroser Peer-Review und Zusammenarbeit bei der Entwicklung quantenresistenter Kryptografie.

Auch wenn der Fehler der Sicherheit gitterbasierter kryptografischer Verfahren eine vorübergehende Entlastung verschafft, erinnert er zugleich an den fortwährenden Bedarf an Forschung und Entwicklung im Bereich der Post-Quanten-Kryptografie.

Während NIST seinen PQC-Standardisierungsprozess fortsetzt, muss die kryptografische Gemeinschaft proaktiv und anpassungsfähig bleiben, neue Ideen und Ansätze aufgreifen und so die langfristige Sicherheit unserer digitalen Welt angesichts der zunehmenden Leistungsfähigkeit des Quantencomputings gewährleisten.

## Quellen

- Sebastien Rousseau, (2024). [Quantum Algorithm Challenges Lattice-Based Cryptography][00].
- Chen, Y. (2024). [Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉][01]. Journal of Quantum Computing and Cryptography, 7(4), 112-135.
- Regev, O. (2005). [On lattices, learning with errors, random linear codes, and cryptography. ⧉][02] In Proceedings of the 37th Annual ACM Symposium on Theory of Computing (pp. 84-93).
- Kuperberg, G. (2005). [A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉][03] SIAM Journal on Computing, 35(1), 170-188.

[00]: https://sebastienrousseau.com/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography/index.html "Challenges in Quantum Algorithms for Lattice-Based Cryptography"
[01]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[02]: https://nigelsmart.github.io/LWE.html "Learning with Errors"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization "Post-Quantum Cryptography Standardization"
[04]: https://pq-crystals.org/kyber/ "Kyber"
[05]: https://pq-crystals.org/dilithium/ "Dilithium"
[06]: https://www.inferati.com/blog/fhe-schemes-bgv "BGV"
[07]: https://tfhe.github.io/tfhe/ "TFHE"
