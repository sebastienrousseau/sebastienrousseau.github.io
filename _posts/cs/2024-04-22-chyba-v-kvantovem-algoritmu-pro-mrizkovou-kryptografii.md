---
title: "Kvantová mřížková kryptografie: chyba v Chenově útoku na LWE"
subtitle: "Odborná recenze odhalila chybu v Chenově průlomové práci"
description: "Chyba v kvantovém algoritmu LWE Yileie Chena dočasně poskytuje odklad mřížkové kryptografii. Co to znamená pro CRYSTALS-Kyber, Dilithium a plán PQC."
date: "April 22, 2024"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Obrázek vygenerovaný pomocí MidJourney - síť digitálních uzlů v červených a modrých odstínech."
keywords: "postkvantová kryptografie, NIST, standardizace PQC, Yilei Chen, kvantový algoritmus, mřížková kryptografie, problém LWE, CRYSTALS-KYBER, CRYSTALS-Dilithium, kvantově odolná kryptografie"
---


> **TL;DR.** Chyba v kvantovém algoritmu LWE Yileie Chena dočasně poskytuje odklad mřížkové kryptografii. Co to znamená pro CRYSTALS-Kyber, Dilithium a plán PQC.

**Klíčové body**

- **Kvantové dilema: přehodnocení standardizace postkvantové kryptografie NIST ve světle algoritmu Yileie Chena.** Navazuji na svůj nedávný článek o výzvách kvantových algoritmů pro mřížkovou kryptografii a předkládám aktualizaci k nejnovějšímu vývoji ve výzkumu Yileie Chena.
- **Chyba v Chenově kvantovém algoritmu.** Chyba byla nalezena v kroku 9 Chenova algoritmu a autor uvedl, že neví, jak ji opravit.
- **Důsledky pro proces standardizace postkvantové kryptografie NIST.** Chenův výzkum nepřímo vyvolal obavy a pochybnosti o procesu standardizace postkvantové kryptografie (PQC) NIST a o výběru kvantově odolných kryptografických algoritmů.
- **Budoucnost postkvantové kryptografie.** Objev chyby v Chenově algoritmu zdůrazňuje zásadní roli odborné recenze ve vědeckém procesu.

## Kvantové dilema: přehodnocení standardizace postkvantové kryptografie NIST ve světle algoritmu Yileie Chena

Navazuji na svůj nedávný článek o [výzvách kvantových algoritmů pro mřížkovou kryptografii][00] a považuji za nutné poskytnout aktualizaci k nejnovějšímu vývoji ve [výzkumu Yileie Chena ⧉][01].

Nečekaným vývojem oznámil Yilei Chen, odborný asistent na Institute for Interdisciplinary Information Science (IIIS) univerzity Tsinghua, že jeho kolegové Hongxun Wu a Thomas Vidick nezávisle na sobě objevili chybu v jeho kvantovém algoritmu s polynomiálním časem, který byl navržen k řešení problému Learning with Errors (LWE).

Tato chyba činí algoritmus nefunkčním a Chen připustil, že jeho přístup neobstojí tak, jak původně tvrdil.

## Chyba v Chenově kvantovém algoritmu

Chyba byla nalezena v kroku 9 Chenova algoritmu a autor uvedl, že neví, jak ji opravit. Tento objev je pro kryptografickou komunitu úlevou, protože potvrzuje, že problém LWE, zásadní součást ochranných metod postkvantové kryptografie, zůstává bezpečný.

Chenova práce zkoumala i další složité mřížkové problémy, jako je decisional shortest vector problem (GapSVP) a shortest independent vector problem (SIVP), v rámci polynomiálních aproximačních faktorů. Ačkoli chyba v jeho algoritmu tyto problémy přímo neovlivňuje, vyvolává otázky ohledně robustnosti kvantových algoritmů pro mřížkovou kryptografii.

Podle [stránky Nigela Smarta ⧉][02] je však navrhovaný kvantový útok na LWE chybný a neohrožuje mřížková kryptografická schémata jako [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06] nebo [TFHE ⧉][07].

## Důsledky pro proces standardizace postkvantové kryptografie NIST

Chenův výzkum nepřímo vyvolal obavy a pochybnosti o [procesu standardizace postkvantové kryptografie (PQC) NIST ⧉][03] a o výběru kvantově odolných kryptografických algoritmů.

Schémata [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) a CRYSTALS-Dilithium, která patří mezi finalisty procesu standardizace NIST PQC, jsou příklady mřížkových kryptografických schémat, jež byla důkladně testována a hodnocena z hlediska kvantové odolnosti. Je však zásadní tato schémata dále testovat a zdokonalovat, aby byla zajištěna jejich dlouhodobá bezpečnost a životaschopnost.

NIST, kryptografická komunita i firmy musí zůstat ostražití a nadále zkoumat alternativní matematické základy postkvantové kryptografie, aby byla k dispozici robustní a rozmanitá sada možností pro kvantově odolnou bezpečnost.

## Budoucnost postkvantové kryptografie

Objev chyby v Chenově algoritmu zdůrazňuje zásadní roli odborné recenze ve vědeckém procesu. Poukazuje také na potřebu okamžité recenze, zpětné vazby a diskuse.

Kvantová éra začala a potřeba vyvíjet kvantově odolné kryptografické metody vyžaduje koordinovaná opatření na celosvětové úrovni, aby byla zajištěna bezpečnost naší digitální infrastruktury tváří v tvář rostoucím možnostem kvantových počítačů a závodu o kvantovou nadřazenost.

Proces standardizace NIST PQC je významným krokem tímto směrem, ale je teprve začátkem. Chyba v Chenově algoritmu je ostrým připomenutím výzev a nejistot, které nás čekají, zároveň však slouží jako výzva k akci, aby kryptografická komunita zdvojnásobila své úsilí a posunula hranice možného.

Jde o pozoruhodný vývoj v oblasti postkvantové kryptografie a bude zajímavé sledovat, jak se proces standardizace NIST PQC v reakci na tyto nové informace vyvine.

## Závěr

Chyba objevená v kvantovém algoritmu Yileie Chena pro řešení problému LWE dokládá důležitost důkladné odborné recenze a spolupráce při vývoji kvantově odolné kryptografie.

Ačkoli chyba poskytuje dočasnou úlevu bezpečnosti mřížkových kryptografických schémat, zároveň připomíná trvalou potřebu výzkumu a vývoje v oblasti postkvantové kryptografie.

Zatímco NIST pokračuje v procesu standardizace PQC, kryptografická komunita musí zůstat proaktivní a přizpůsobivá a přijímat nové myšlenky a přístupy, aby byla zajištěna dlouhodobá bezpečnost našeho digitálního světa tváří v tvář rostoucím možnostem kvantových počítačů.

## Reference

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
