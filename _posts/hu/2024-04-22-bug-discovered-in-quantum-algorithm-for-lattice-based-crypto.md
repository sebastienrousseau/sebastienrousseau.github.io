---
title: "Kvantum rács-kriptográfia: hiba Chen LWE-támadásában"
tags: "post-quantum cryptography, NIST, quantum algorithms, Lattice-Based Cryptography, LWE Problem, quantum computing, Cryptographic Security, Quantum Resistance, Cryptography Research, ISO 20022, AI, Rust"
subtitle: "A szakértői értékelés hibát tár fel Chen úttörő munkájában"
description: "Egy hiba Yilei Chen kvantumos LWE-algoritmusában átmenetileg haladékot ad a rács-alapú kriptográfiának. Mit jelent ez a CRYSTALS-Kyber, Dilithium és a PQC-ütemterv szempontjából."
date: "Apr 22, 2024"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "A MidJourney segítségével generált kép: digitális csomópontok hálózata piros és kék árnyalatokban."
keywords: "poszt-kvantum kriptográfia, NIST, PQC-szabványosítás, Yilei Chen, kvantumalgoritmus, rács-alapú kriptográfia, LWE-probléma, CRYSTALS-KYBER, CRYSTALS-Dilithium, kvantumálló kriptográfia"
---

## A kvantum-rejtvény: a NIST poszt-kvantum kriptográfiai szabványosításának újraértékelése Yilei Chen algoritmusának fényében

A [rács-alapú kriptográfia kvantumalgoritmusainak kihívásairól][00] szóló legutóbbi cikkem nyomán késztetést érzek, hogy frissítést adjak a [Yilei Chen kutatásában ⧉][01] bekövetkezett legújabb fejleményekről.

Váratlan fordulatként Yilei Chen, a Tsinghua Egyetem Interdiszciplináris Információtudományi Intézetének (IIIS) adjunktusa arról számolt be, hogy kollégái, Hongxun Wu és Thomas Vidick egymástól függetlenül hibát fedeztek fel a Learning with Errors (LWE) probléma megoldására tervezett polinomiális idejű kvantumalgoritmusában.

Ez a hiba működésképtelenné teszi az algoritmust, és Chen elismerte, hogy megközelítése nem állja meg a helyét úgy, ahogyan azt eredetileg állította.

## A hiba Chen kvantumalgoritmusában

A hibát Chen algoritmusának 9. lépésében találták meg, és ő maga kijelentette, hogy nem tudja, hogyan javítsa ki. Ez a felfedezés megkönnyebbülést jelent a kriptográfiai közösség számára, mivel megerősíti, hogy az LWE-probléma, a poszt-kvantum kriptográfiai védelmi módszerek kritikus eleme, továbbra is biztonságos marad.

Chen tanulmánya más összetett rácsproblémákat is vizsgált, például a döntési legrövidebb vektor problémát (GapSVP) és a legrövidebb független vektor problémát (SIVP), polinomiális közelítési tényezőkön belül. Bár az algoritmusában lévő hiba nem érinti közvetlenül ezeket a problémákat, mégis kérdéseket vet fel a rács-alapú kriptográfia kvantumalgoritmusainak megbízhatóságával kapcsolatban.

[Nigel Smart oldala ⧉][02] szerint azonban a javasolt LWE elleni kvantumos támadás hibás, és nem veszélyezteti az olyan rács-kriptográfiai sémákat, mint a [Kyber ⧉][04], a [Dilithium ⧉][05], a [BGV ⧉][06] vagy a [TFHE ⧉][07].

## Következmények a NIST poszt-kvantum kriptográfiai szabványosítási folyamatára

Chen kutatása közvetve aggályokat és kételyeket vetett fel a [NIST poszt-kvantum kriptográfiai (PQC) szabványosítási folyamatával ⧉][03] és a kvantumálló kriptográfiai algoritmusok kiválasztásával kapcsolatban.

A [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) és a CRYSTALS-Dilithium sémák, amelyek a NIST PQC szabványosítási folyamatának döntőse között szerepelnek, példák olyan rács-alapú kriptográfiai sémákra, amelyeket szigorúan teszteltek és értékeltek kvantumellenállás szempontjából. Ugyanakkor elengedhetetlen e sémák további tesztelése és finomítása, hogy biztosítható legyen hosszú távú biztonságuk és életképességük.

A NIST-nek, a kriptográfiai közösségnek és a vállalatoknak éberen kell maradniuk, és tovább kell vizsgálniuk a poszt-kvantum kriptográfia alternatív matematikai alapjait, hogy a kvantumálló biztonsághoz robusztus és sokszínű lehetőségek álljanak rendelkezésre.

## A poszt-kvantum kriptográfia jövője

A Chen algoritmusában talált hiba felfedezése aláhúzza a szakértői értékelés kritikus szerepét a tudományos folyamatban. Egyúttal rávilágít az azonnali értékelés, visszajelzés és vita szükségességére is.

A kvantumkorszak elkezdődött, és a kvantumálló kriptográfiai módszerek kifejlesztésének igénye globális léptékű együttműködési intézkedéseket kíván, hogy biztosítható legyen digitális infrastruktúránk biztonsága a fejlődő kvantumszámítási képességek és a kvantumfölényért folyó verseny közepette.

A NIST PQC szabványosítási folyamata jelentős lépés ebbe az irányba, de ez csak a kezdet. A Chen algoritmusában lévő hiba éles emlékeztető az előttünk álló kihívásokra és bizonytalanságokra, ugyanakkor cselekvésre való felhívásként is szolgál a kriptográfiai közösség számára, hogy fokozza erőfeszítéseit, és feszegesse a lehetséges határait.

Ez lenyűgöző fejlemény a poszt-kvantum kriptográfia területén, és érdekes lesz látni, hogyan alakul a NIST PQC szabványosítási folyamata ennek az új információnak a hatására.

## Összegzés

A Yilei Chen LWE-probléma megoldására szolgáló kvantumalgoritmusában felfedezett hiba a szigorú szakértői értékelés és az együttműködés fontosságát bizonyítja a kvantumálló kriptográfia fejlesztésében.

Bár a hiba átmeneti megkönnyebbülést nyújt a rács-alapú kriptográfiai sémák biztonsága szempontjából, egyúttal emlékeztet arra is, hogy a poszt-kvantum kriptográfia területén folyamatos kutatásra és fejlesztésre van szükség.

Ahogy a NIST folytatja PQC szabványosítási folyamatát, a kriptográfiai közösségnek proaktívnak és alkalmazkodónak kell maradnia, új ötleteket és megközelítéseket felkarolva, hogy biztosítsa digitális világunk hosszú távú biztonságát a fejlődő kvantumszámítási képességek közepette.

## Hivatkozások

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
