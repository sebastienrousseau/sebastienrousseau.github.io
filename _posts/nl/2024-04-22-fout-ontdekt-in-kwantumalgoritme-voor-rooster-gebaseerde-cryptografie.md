---
title: "Fout ontdekt in kwantumalgoritme voor rooster-gebaseerde cryptografie"
subtitle: "De rooster-gebaseerde cryptografie is voorlopig veilig — maar de les is duidelijk"
description: "In Yilei Chens kwantumalgoritme voor het oplossen van LWE is een fout gevonden, die rooster-gebaseerde cryptografie tijdelijk veilig stelt."
date: "April 22, 2024"
language: "nl-NL"
locale: "nl_NL"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Visualisatie van een correctie in een kwantumalgoritme"
keywords: "Yilei Chen, kwantumalgoritme, LWE, rooster-gebaseerde cryptografie, post-kwantum"
---
## Het kwantum-Rätsel: Neubewertung de NIST-post-kwantumcryptografie-standaardisierung in Lichte van Yilei Chens Algorithmus

Im Anschluss aan meinen jüngsten Artikel over de [uitdagingen quantenbasierter Algorithmen voor de rooster-gebaseerde cryptografie][00] sehe ich mich veranlasst, een update tot de nieuwesten ontwikkelingen ongeveer um [Yilei Chens onderzoek ⧉][01] tot geben.

In een unerwarteten Wendung berichtete Yilei Chen, Assistenzprofessor am Institute for Interdisciplinary Information Science (IIIS) de Universität Tsinghua, dat zijne Kolleggen Hongxun Wu en Thomas Vidick onafhankelijk voneinander een Fehler in zijn polynomialzeitigen kwantumalgoritme tot oplossing des Learning-with-Errors-probleems (LWE) ontdekt hebben.

Deze Fehler macht de Algorithmus unbrauchbar, en Chen heeft eingeräumt, dat zijn aanpak niet hält, was ursprünglich behauptet werd.

## De Fehler in Chens kwantumalgoritme

De Fehler werd in stap 9 van Chens Algorithmus gefunden, en hij heeft erklärt, dat hij niet weiß, zoals hij ihn beheben kan. Deze Entdeckung is een Erleichterung voor de cryptografische Gemeinschaft, da ze bestätigt, dat het LWE-probleem – een kritische Komponente de beschermingverfahren in de post-kwantumcryptografie – nog steeds sicher bleibt.

Chens Arbeit untersuchte bovendien weitere komplexe Gitterprobleme, ongeveer het decisional shortest vector problem (GapSVP) en het shortest independent vector problem (SIVP), innerhalb polynomialer Approximationsfaktoren. Auch indien de Fehler in zijn Algorithmus deze probleeme niet unmittelbar betrifft, wirft hij vraagn tot Robustheit quantenbasierter Algorithmen tegen de rooster-gebaseerde cryptografie op.

Doch laut [de Seite van Nigel Smart ⧉][02] is de vorgeschlagene kwantumangriff op LWE fehlerhaft en kompromittiert keine rooster-gebaseerde cryptografieverfahren zoals [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06] of [TFHE ⧉][07].

## impact op de NIST-standaardisierungsprozess voor post-kwantumcryptografie

Chens onderzoek warf indirekt zorgen en Zweifel am [NIST-standaardisierungsprozess voor post-kwantumcryptografie (PQC) ⧉][03] en aan de Auswahl kwantumresistente cryptografischer Algorithmen op.

De procedure [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) en CRYSTALS-Dilithium, de tot de Finalisten in NIST-PQC-standaardisierungsprozess gehören, zijn voorbeelden voor rooster-gebaseerde cryptografische procedure, de rigoros op haar kwantumresistenz getestet en bewertet werden. Es is echter doorslaggevend, deze procedure nog steeds tot prüfen en tot verfeinern, um haar langetermijn-e beveiliging en Tragfähigkeit tot waarborgen.

NIST, de cryptografische Gemeinschaft en ondernemingen moeten wachsam bleiben en nog steeds oudernative mathematische Gongeveerlagen voor de post-kwantumcryptografie erforschen, daarmee een belastbare en vielfältige Auswahl aan Optionen voor kwantumresistente beveiliging reedsteht.

## De toekomst de post-kwantumcryptografie

De Entdeckung des Fehlers in Chens Algorithmus untpasreicht de centrale Rolle de Peer-Review in wissenschaftlichen proces. U verduidelijkt bovendien de noodzaak unmittelbarer Begoedachtung, Rückmeldung en Debatte.

De kwantum-Ära heeft begonnen, en de noodzaak, kwantumresistente cryptografische procedure tot ontwikkelen, vereist kooperative maatregeln op wereldwijder Ebene, um de beveiliging onze digitaale Infrastruktur angesichts de zunehmenden Leistungsfähigkeit des kwantumcomputings en des Wettlaufs um de kwantumüberleggenheit tot waarborgen.

De NIST-PQC-standaardisierungsprozess is een belangrijker stap in deze Richtung, maar hij is pas de begin. De Fehler in Chens Algorithmus is een eindringliche Erinnerung aan de kommenden uitdagingen en Unsicherheiten, dient maar tegelijk als Aufruf aan de cryptografische Gemeinschaft, haar Anstrengungen tot verdoppeln en de Grenzen des Möglichen weiter tot verschieben.

Dies is een faszinooitrende ontwikkeling in domein de post-kwantumcryptografie, en es wordt spannend tot beobachten zijn, zoals sich de NIST-PQC-standaardisierungsprozess als Reaktion op deze nieuwen inzichten weiterontwikkeld.

## Fazit

De in Yilei Chens kwantumalgoritme tot oplossing des LWE-probleems ontdekte Fehler is een Beleg voor de Bedeutung rigoroser Peer-Review en samenwerking bij de ontwikkeling kwantumresistente cryptografie.

Auch indien de Fehler de beveiliging rooster-gebaseerde cryptografischer procedure een vorübergehende Entlastung vercreëert, erinnert hij tegelijk aan de fortterwijlen Bedarf aan onderzoek en ontwikkeling in domein de post-kwantumcryptografie.

Während NIST zijn PQC-standaardisierungsprozess fortzet, moet de cryptografische Gemeinschaft proaktiv en anpassungsfähig bleiben, nieuwe Ideen en Ansätze aufgrijpen en so de langetermijn-e beveiliging onze digitaale wereld angesichts de zunehmenden Leistungsfähigkeit des kwantumcomputings waarborgen.

## Quellen

- Sebastien Rousseau, (2024). [Quantum Algorithm Challenges Lattice-Based Cryptography][00].
- Chen, Y. (2024). [Quantum Algorithms for Lattice probleems: A New Era in Cryptography ⧉][01]. Journal of Quantum Computing and Cryptography, 7(4), 112-135.
- Regev, O. (2005). [On lattices, learning with errors, random linear codes, and cryptography. ⧉][02] In Proceedings of the 37th Annual ACM Symposium on Theory of Computing (pp. 84-93).
- Kuperberg, G. (2005). [A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉][03] SIAM Journal on Computing, 35(1), 170-188.

[00]: https://sebastienrousseau.com/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography/index.html "Challenges in Quantum Algorithms for Lattice-Based Cryptography"
[01]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice probleems: A New Era in Cryptography"
[02]: https://nigelsmart.github.io/LWE.html "Learning with Errors"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization "Post-Quantum Cryptography standaardization"
[04]: https://pq-crystals.org/kyber/ "Kyber"
[05]: https://pq-crystals.org/dilithium/ "Dilithium"
[06]: https://www.inferati.com/blog/fhe-schemes-bgv "BGV"
[07]: https://tfhe.github.io/tfhe/ "TFHE"
