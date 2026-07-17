---
title: "KyberLib: CRYSTALS-Kyber i Rust för postkvantum"
subtitle: "KyberLib, en robust Rust-implementering av CRYSTALS-Kyber för kvanteran."
description: "En robust och kvantsäker kryptografisk implementering av algoritmen CRYSTALS-Kyber, som skyddar dina data mot kvanthot och kryptoanalytiska attacker."
date: "November 28, 2023"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg"
banner_alt: "Säker kommunikation i kvanteran med KyberLib"
keywords: "KyberLib, Rust CRYSTALS-Kyber, postkvantkryptografi, gitterbaserad kryptografi, kvantresistent nyckelutbyte, NIST FIPS 203, Sebastien Rousseau, KEM, betalningsautentisering, PQC-bibliotek"
---

[![Säker kommunikation i kvanteran med KyberLib](https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg).class=\"img-fluid clearfix\"][07]

`KyberLib` är ett Rust-baserat bibliotek som skyddar dina data mot det potentiella hotet från kvantdatorer. Biblioteket bygger på **algoritmen [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)** och erbjuder utmärkt säkerhet, effektivitet och flexibilitet, med enkel integrering på en rad plattformar, inklusive `no-std`-miljöer.

![divider][divider].class=\"m-10 w-100\"

## Skydda dina data i kvantåldern

Kvantdatorernas framväxt har medfört ett betydande hot mot konventionella kryptografiska säkerhetsmekanismer. För att möta denna utmaning utvecklas fältet kvantsäker kryptografi (Quantum-Safe Cryptography, QSC) i snabb takt.

I spetsen för denna omvälvande utveckling står National Institute of Standards and Technology (NIST), som leder standardiseringen av QSC-algoritmer.

Under 2023 valde NIST ut fyra innovativa algoritmer:

- [**[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)** ⧉][01] (mekanism för nyckelinkapsling)
- [**CRYSTALS-Dilithium** ⧉][02] (digitala signaturer)
- [**FALCON** ⧉][03] (lättviktiga digitala signaturer)
- [**SPHINCS+** ⧉][04] (hashbaserade digitala signaturer)

Dessa banbrytande algoritmer vilar på skilda matematiska principer, däribland gitterbaserad kryptografi, hashbaserad kryptografi och kodbaserad kryptografi, med målet att ge ett robust försvar mot kvantattacker.

## En närmare titt på gitterbaserad kryptografi

Gitterbaserad kryptografi (Lattice-Based Cryptography, LBC) framträder som en av de främsta kandidaterna inom QSC och erbjuder en lovande postkvantkryptografisk (PQC) lösning. LBC är mångsidig, med tillämpningar som spänner från nyckelinkapslingsmekanismer (KEM) och digitala signaturer till krypteringssystem med öppen nyckel, alla förankrade i matematiska gitter.

Gitter är ett grundläggande begrepp inom matematiken som funnit tillämpningar inom en rad områden, däribland kryptografi. Enkelt uttryckt är ett gitter en regelbunden uppsättning punkter i rummet som bildar en rutnätsliknande struktur. Punkterna är förbundna med linjer och bildar ett nätverk av sammanlänkade celler. Punkternas specifika placering och avstånden mellan dem definierar gittrets unika egenskaper.

### 3D-representation av ett gitter med basvektorer

Detta diagram visar en tredimensionell gitterstruktur genererad av tre basvektorer:

- `b1 = [1, 0, 0]` i rött,
- `b2 = [0, 1, 0]` i grönt, och
- `b3 = [0, 0, 1]` i blått.

Varje punkt i gittret bildas genom att dessa basvektorer kombineras i olika heltalsproportioner, vilket skapar ett rutnätsmönster som sträcker sig i alla tre rumsdimensioner. Visualiseringen fångar essensen av ett tredimensionellt gitter, ett begrepp som används flitigt inom fysik och matematik för att representera den regelbundna, återkommande placeringen av punkter i rummet.

![3D-representation av ett gitter med basvektorer][06].class=\"img-fluid mx-auto d-block\"

Inom kryptografin används gitter som grund för vissa kryptografiska algoritmer. Gitterbaserad kryptografi (LBC) utnyttjar gittrens matematiska egenskaper för att skapa säkra kryptografiska system som står emot attacker från kvantdatorer. Kvantdatorer utgör ett betydande hot mot konventionell kryptografi, eftersom de effektivt kan knäcka algoritmer som bygger på faktorisering av stora tal eller på lösning av diskreta logaritmproblem.

[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) exemplifierar styrkorna hos LBC och ger robust motståndskraft mot kvantattacker i kombination med utmärkt effektivitet och nyckelstorlek. Stödet för flera plattformar och kompatibiliteten med befintlig kryptografi gör den till ett pålitligt alternativ för datasäkerhet i kvanteran.

De aktuella specifikationerna för [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) är följande:

- **Kyber512**: ger en säkerhetsnivå motsvarande 128-bitars AES-kryptering och skyddar känsliga data med branschstandardiserat skydd.
- **Kyber768**: ger en säkerhetsnivå motsvarande 256-bitars AES-kryptering och säkerställer konfidentialiteten för mycket känslig information.
- **Kyber1024**: ger en säkerhetsnivå som överstiger 256-bitars AES-kryptering och erbjuder robust skydd mot kvantattacker samt värnar dataintegriteten långt in i framtiden.

### Jämförelse av säkerhetsnivåer mellan klassiska och kvantresistenta algoritmer

Detta stapeldiagram illustrerar de relativa säkerhetsnivåerna hos klassiska kryptografiska algoritmer som RSA-2048 och Elliptic Curve Digital Signature Algorithm (ECDSA), jämförda med specifikationerna för de kvantresistenta varianterna av algoritmen [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) (Kyber512, Kyber768 och Kyber1024).

Även om diagrammet erbjuder en visuell jämförelse är det viktigt att notera att säkerhetsnivåerna inte är direkt jämförbara, eftersom de vilar på olika matematiska principer.

Diagrammet ger dock en användbar referenspunkt för att förstå säkerhetsnivåerna hos kvantresistenta algoritmer.

![Gitterbaserad kryptografi][05].class=\"img-fluid mx-auto d-block\"

![divider][divider].class=\"m-10 w-100\"

## KyberLib: ett Rust-bibliotek för kvantresistent kryptografi

KyberLib utnyttjar kraften i [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) för att leverera förbättrad minnessäkerhet och robust säkerhet på systemnivå. Biblioteket stöder flera specifikationer av [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) (Kyber512, Kyber768, Kyber1024) och erbjuder därmed ett spann av säkerhetsnivåer anpassade efter dina specifika behov. Dess `no_std`-kompatibilitet gör den till ett idealiskt val för inbyggda system, medan dess kompatibilitet med WebAssembly (WASM) underlättar sömlös integrering i webbapplikationer.

![divider][divider].class=\"m-10 w-100\"

## Skydda webbapplikationer med kvantresistent kryptografi

KyberLib är utformat för ett minimalt minnesavtryck och lämpar sig därför väl för inbyggda och resursbegränsade system, utan att säkerheten äventyras. Den Rust-baserade implementeringen drar nytta av språkets säkerhetsegenskaper och förstärker det skydd som algoritmen [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) erbjuder.

Dessutom ökar KyberLibs WebAssembly-kompatibilitet dess användbarhet i webbapplikationer, vilket garanterar att biblioteket förblir ett viktigt verktyg inom kryptografins dynamiska område.

[Kom igång med KyberLib nu! ⧉][00] KyberLib är enkelt att installera, kostnadsfritt för både privat och kommersiellt bruk, och din självklara lösning för kvantresistent kryptografi.

[00]: https://kyberlib.com/getting-started/index.html "Kom igång"
[01]: https://pq-crystals.org/kyber/ "Kyber: en CCA-säker modulgitterbaserad KEM"
[02]: https://pq-crystals.org/dilithium/ "Dilithium: ett CCA-säkert gitterbaserat signaturschema"
[03]: https://falcon-sign.info/ "FALCON: ett postkvantsignaturschema"
[04]: https://sphincs.org/ "SPHINCS+: ett tillståndslöst hashbaserat signaturschema"
[05]: https://cloudcdn.pro/stocks/diagrams/kyber-vs-classical.svg "Jämförelse av säkerhetsnivåer mellan klassiska och kvantresistenta algoritmer"
[06]: https://cloudcdn.pro/stocks/diagrams/3D-lattice-graph.svg "3D-representation av ett gitter med basvektorer"
[07]: https://kyberlib.com/ "Integritet och säkerhet i en kvantvärld"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Avdelare"
