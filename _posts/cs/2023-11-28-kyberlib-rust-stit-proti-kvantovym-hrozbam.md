---
title: "KyberLib: Rust CRYSTALS-Kyber pro postkvantovou kryptografii"
subtitle: "KyberLib, robustní implementace CRYSTALS-Kyber v jazyce Rust pro kvantovou éru"
description: "Robustní a kvantově odolná kryptografická implementace algoritmu CRYSTALS-Kyber, která chrání vaše data před kvantovými hrozbami a kryptoanalytickými útoky."
date: "November 28, 2023"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg"
banner_alt: "Zabezpečená komunikace v kvantové éře s knihovnou KyberLib"
keywords: "KyberLib, Rust CRYSTALS-Kyber, postkvantová kryptografie, mřížková kryptografie, kvantově odolná výměna klíčů, NIST FIPS 203, Sebastien Rousseau, KEM, autentizace plateb, knihovna PQC"
---


[![Zabezpečená komunikace v kvantové éře s knihovnou KyberLib](https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg).class=\"img-fluid clearfix\"][07]

`KyberLib` je knihovna v jazyce Rust, která chrání vaše data před potenciální hrozbou kvantových výpočtů. Staví na **algoritmu [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)** a poskytuje vysokou míru zabezpečení, efektivity a všestrannosti se snadnou integrací do různých platforem včetně prostředí `no-std`.

![divider][divider].class=\"m-10 w-100\"

## Zabezpečení dat v kvantové éře

Nástup kvantových výpočtů představuje významnou hrozbu pro konvenční kryptografická bezpečnostní opatření. V reakci na tuto výzvu se rychle rozvíjí obor kvantově odolné kryptografie (QSC).

V čele tohoto vývoje stojí National Institute of Standards and Technology (NIST), který vede standardizaci algoritmů QSC.

V roce 2023 zařadil NIST do užšího výběru čtyři inovativní algoritmy:

- [**[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)** ⧉][01] (mechanismus zapouzdření klíče)
- [**CRYSTALS-Dilithium** ⧉][02] (digitální podpisy)
- [**FALCON** ⧉][03] (lehké digitální podpisy)
- [**SPHINCS+** ⧉][04] (digitální podpisy založené na hashích)

Tyto algoritmy stojí na různých matematických principech, včetně mřížkové kryptografie, kryptografie založené na hashích a kryptografie založené na kódech, s cílem poskytnout robustní obranu proti kvantovým útokům.

## Zkoumání mřížkové kryptografie

Mřížková kryptografie (LBC, Lattice-Based Cryptography) se stává jedním z hlavních směrů QSC a nabízí slibné řešení postkvantové kryptografie (PQC). LBC je všestranná a její využití sahá od mechanismů zapouzdření klíčů (KEM) přes digitální podpisy až po schémata šifrování s veřejným klíčem, která vycházejí z matematických mřížek.

Mřížky jsou základním matematickým pojmem, který našel uplatnění v řadě oborů včetně kryptografie. Zjednodušeně řečeno je mřížka pravidelné uspořádání bodů v prostoru, jež tvoří strukturu podobnou mřížové síti. Tyto body jsou propojeny čarami a vytvářejí síť vzájemně propojených buněk. Konkrétní rozmístění bodů a jejich vzájemné rozestupy definují jedinečné vlastnosti dané mřížky.

### Trojrozměrné znázornění mřížky s bázovými vektory

Tento graf znázorňuje trojrozměrnou mřížkovou strukturu vytvořenou třemi bázovými vektory:

- `b1 = [1, 0, 0]` červeně,
- `b2 = [0, 1, 0]` zeleně a
- `b3 = [0, 0, 1]` modře.

Každý bod mřížky vzniká kombinací těchto bázových vektorů v různých celočíselných poměrech, čímž vzniká vzor podobný mřížové síti, který se rozprostírá do všech tří prostorových rozměrů. Vizualizace zachycuje podstatu trojrozměrné mřížky, pojmu široce používaného ve fyzice a matematice pro znázornění pravidelného, opakujícího se rozmístění bodů v prostoru.

![Trojrozměrné znázornění mřížky s bázovými vektory][06].class=\"img-fluid mx-auto d-block\"

V kryptografii slouží mřížky jako základ některých kryptografických algoritmů. Mřížková kryptografie (LBC) využívá matematické vlastnosti mřížek k vytvoření bezpečných kryptografických schémat odolných vůči útokům kvantových počítačů. Kvantové počítače představují významnou hrozbu pro konvenční kryptografii, protože dokážou efektivně prolomit algoritmy, které se opírají o faktorizaci velkých čísel nebo o řešení problémů diskrétního logaritmu.

[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) je dobrým příkladem předností LBC: poskytuje robustní odolnost proti kvantovým útokům spolu s vysokou efektivitou a příznivou velikostí klíče. Podpora více platforem a kompatibilita s kryptografií z něj činí spolehlivou volbu pro zabezpečení dat v kvantové éře.

Aktuální specifikace [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) jsou následující:

- **Kyber512**: poskytuje úroveň zabezpečení odpovídající 128bitovému šifrování AES a chrání citlivá data ochranou na úrovni odvětvového standardu.
- **Kyber768**: poskytuje úroveň zabezpečení odpovídající 256bitovému šifrování AES a zajišťuje důvěrnost vysoce citlivých informací.
- **Kyber1024**: poskytuje úroveň zabezpečení přesahující 256bitové šifrování AES, nabízí robustní ochranu proti kvantovým útokům a chrání integritu dat i do vzdálené budoucnosti.

### Porovnání úrovní zabezpečení klasických a kvantově odolných algoritmů

Tento sloupcový graf znázorňuje relativní úrovně zabezpečení klasických kryptografických algoritmů, jako jsou RSA-2048 a Elliptic Curve Digital Signature Algorithm (ECDSA), v porovnání se specifikacemi kvantově odolných variant algoritmu [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) (Kyber512, Kyber768 a Kyber1024).

Graf sice nabízí vizuální porovnání, je však důležité zdůraznit, že úrovně zabezpečení nelze přímo srovnávat, protože vycházejí z odlišných matematických principů.

Graf nicméně poskytuje užitečný referenční bod pro pochopení úrovní zabezpečení kvantově odolných algoritmů.

![Mřížková kryptografie][05].class=\"img-fluid mx-auto d-block\"

![divider][divider].class=\"m-10 w-100\"

## KyberLib: knihovna v jazyce Rust pro kvantově odolnou kryptografii

KyberLib využívá [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) k dosažení lepší paměťové bezpečnosti a robustního zabezpečení na úrovni systému. Podporuje více specifikací [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) (Kyber512, Kyber768, Kyber1024) a nabízí škálu úrovní zabezpečení podle konkrétních potřeb. Díky souladu s `no_std` je vhodnou volbou pro vestavěné systémy a její kompatibilita s WebAssembly (WASM) usnadňuje bezproblémovou integraci do webových aplikací.

![divider][divider].class=\"m-10 w-100\"

## Ochrana webových aplikací kvantově odolnou kryptografií

KyberLib je navržena pro minimální paměťovou náročnost, a je proto vhodná pro vestavěné systémy a systémy s omezenými prostředky bez ústupků v zabezpečení. Její implementace v jazyce Rust těží z bezpečnostních vlastností tohoto jazyka a posiluje zabezpečení, které poskytuje algoritmus [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html).

Kompatibilita KyberLib s WebAssembly navíc zvyšuje její užitečnost ve webových aplikacích a zajišťuje, že zůstává důležitým nástrojem v dynamicky se vyvíjející kryptografii.

[Začněte s KyberLib ještě dnes. ⧉][00] Snadno se instaluje, je zdarma pro osobní i komerční použití a představuje spolehlivé řešení pro kvantově odolnou kryptografii.

[00]: https://kyberlib.com/getting-started/index.html "Začínáme"
[01]: https://pq-crystals.org/kyber/ "Kyber: modul-mřížkový KEM zabezpečený proti CCA"
[02]: https://pq-crystals.org/dilithium/ "Dilithium: mřížkové podpisové schéma zabezpečené proti CCA"
[03]: https://falcon-sign.info/ "FALCON: postkvantové podpisové schéma"
[04]: https://sphincs.org/ "SPHINCS+: bezstavové podpisové schéma založené na hashích"
[05]: https://cloudcdn.pro/stocks/diagrams/kyber-vs-classical.svg "Porovnání úrovní zabezpečení klasických a kvantově odolných algoritmů"
[06]: https://cloudcdn.pro/stocks/diagrams/3D-lattice-graph.svg "Trojrozměrné znázornění mřížky s bázovými vektory"
[07]: https://kyberlib.com/ "Soukromí a bezpečnost v kvantovém světě"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Oddělovač"
