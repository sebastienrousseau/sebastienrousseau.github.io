---
title: "Kvantově odolné platby: proč musí odvětví jednat hned"
subtitle: "Kvantově odolná připravenost je rozhodnutí o současné infrastruktuře, nikoli o budoucí. Bílá kniha EPAA popisuje strukturální riziko a naléhavou potřebu migrace."
description: "Kvantové počítače ohrožují kryptografii platebních systémů. Bílá kniha EPAA popisuje strukturální riziko a naléhavé důvody pro migraci na postkvantovou kryptografii."
date: "September 01, 2025"
language: "cs"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Deska plošných spojů kvantového počítače v modrém světle"
keywords: "kvantově odolné platby, postkvantová kryptografie, SEPA, SWIFT gpi, ISO 20022, bezpečnost finančních služeb, EPAA, harvest-now decrypt-later, kryptografická agilita, Sebastien Rousseau"
---

## Kvantová hrozba pro platební systémy

Moderní platební infrastruktura se opírá o kryptografii veřejného klíče, tedy o RSA, ECC a Diffie-Hellman, aby ověřovala transakce, chránila data držitelů karet a zabezpečovala výměnu zpráv mezi finančními institucemi. Tyto algoritmy tvoří základ SWIFT, SEPA, systémů hrubého zúčtování v reálném čase a prakticky každého kartového schématu, které je dnes v provozu.

Kvantové počítače s Shorovým algoritmem dokážou tyto kryptografické primitivy prolomit. Kvantové stroje odolné vůči chybám sice zatím neexistují v potřebném měřítku, ale vývoj hardwaru, jak jej předvedly IBM, Google a další, činí z této otázky spíše inženýrský harmonogram než teorii. Národní institut pro standardy a technologie (NIST) na to již reagoval dokončením první sady postkvantových kryptografických standardů (FIPS 203, 204 a 205).

## Riziko „sklidit teď, dešifrovat později“

Hrozba se neomezuje na budoucí okamžik, kdy kvantové počítače dosáhnou dostatečného výkonu. Státní aktéři a sofistikovaní protivníci již dnes zachytávají a ukládají šifrovaná data se záměrem dešifrovat je, jakmile budou kvantové prostředky k dispozici. Tato strategie „sklidit teď, dešifrovat později“ (harvest-now decrypt-later, HNDL) znamená, že jakákoli platební data s dlouhodobou citlivostí, tedy regulatorní záznamy, archivy pro compliance a smluvní závazky, jsou již ohrožena.

Finanční regulátoři začali reagovat. Singapurský měnový úřad (Monetary Authority of Singapore, MAS) vydal pokyny ke kvantové připravenosti. Australský úřad pro obezřetnostní regulaci (Australian Prudential Regulation Authority, APRA) označil kryptografické riziko ve svém rámci technologické odolnosti. Nařízení Evropské unie o digitální provozní odolnosti (Digital Operational Resilience Act, DORA) vyžaduje řízení rizik ICT, které musí zohledňovat vznikající hrozby včetně kvantových počítačů.

## Dopad napříč platebními okruhy

Důsledky pokrývají celou šíři platební infrastruktury:

**Zprávy SWIFT:** Formáty zpráv MT a MX se pro integritu a autentizaci spoléhají na TLS a digitální podpisy. Narušená infrastruktura klíčů by podkopala model důvěry, který celosvětově propojuje více než 11 000 institucí.

**SEPA a okamžité platby:** Schéma SEPA Instant Credit Transfer od European Payments Council zpracovává neodvolatelné transakce za méně než deset sekund. Narušení kryptografie při této rychlosti neponechává žádný prostor pro lidský zásah ani ruční ověření.

**Platební systémy v reálném čase:** Faster Payments (UK), FedNow (US) a NPP (Austrálie) mají všechny stejnou závislost na klasických kryptografických primitivech pro autentizaci zpráv a ověřování účastníků.

**Compliance a data s dlouhou životností:** Platební záznamy uchovávané pro regulatorní účely, často povinně po dobu pěti až deseti let či déle, přežijí bezpečnostní záruky kryptografie, která je chránila v okamžiku vzniku. Migrační programy [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) musí zohlednit kryptografickou trvanlivost dat, která produkují.

**Blockchain a technologie distribuované účetní knihy:** Platformy digitálních aktiv a tokenizované platební nástroje, které závisejí na kryptografii eliptických křivek, čelí přímé a dobře pochopené hrozbě ze strany kvantových algoritmů.

## Co musí organizace udělat hned

Přechod na kvantově odolnou kryptografii není jednorázová aktualizace, ale víceletý program vyžadující strukturovanou přípravu:

**Kryptografická inventarizace:** Organizace musí zkatalogizovat každý systém, protokol a úložiště dat, které závisí na klasické kryptografii veřejného klíče. To zahrnuje certifikáty TLS, autentizaci API, konfigurace HSM, systémy správy klíčů a šifrování dat v klidu.

**Zavedení postkvantových algoritmů:** NIST standardizoval ML-KEM (FIPS 203) pro zapouzdření klíčů a ML-DSA (FIPS 204) pro digitální podpisy. Organizace by měly začít tyto algoritmy testovat v neprodukčních prostředích a vypracovat migrační plány pro kritické systémy.

**Kryptografická agilita:** Systémy musí být navrženy, nebo přepracovány, tak, aby bylo možné kryptografické algoritmy vyměnit bez nutnosti kompletního přepracování aplikací. Tato zásada platí stejnou měrou pro platební brány, middleware pro výměnu zpráv i pro API určená klientům.

**Hybridní přístupy:** Během přechodného období poskytují hybridní kryptografická schémata, která kombinují klasické a postkvantové algoritmy, obranu do hloubky. Tento přístup zachovává zpětnou kompatibilitu a zároveň zavádí kvantovou odolnost.

## Pracovní skupina EPAA a spolupráce v odvětví

Emerging Payments Association Asia (EPAA) zřídila svou pracovní skupinu Quantum Safe Cryptography Working Group, aby těmto výzvám čelila koordinovaným postupem v odvětví. Pracovní skupina sdružuje účastníky z celého platebního ekosystému, mimo jiné IBM, HSBC, KPMG, JPMorgan Chase a PayPal.

Na workshopech v Sydney, Hongkongu a Singapuru vypracovala pracovní skupina společný rámec pro posuzování kvantového rizika v platebních systémech a pro určení praktických cest migrace. Výsledná bílá kniha [Quantum-Safe Payments: Why the Payments Industry Must Act Now][epaa] představuje konsenzuální postoj k naléhavosti a rozsahu této výzvy.

Analýza pracovní skupiny dochází k závěru, že kvantově odolná připravenost je rozhodnutí o současné infrastruktuře, nikoli o budoucí. Organizace, které otálejí, riskují, že nebudou schopny naplnit regulatorní očekávání, ochránit data s dlouhou životností ani udržet interoperabilitu s partnery, kteří již migraci provedli.

## O autorovi

Sebastien Rousseau je Senior Digital Product Manager v HSBC Bank plc, kde vede produkty API pro firemní platby v rámci Commercial & Investment Bank banky HSBC. Přispěl do pracovní skupiny EPAA Quantum Safe Cryptography Working Group a zabývá se výzkumem uplatnění postkvantové kryptografie ve finančních službách. [Více o Sebastienovi ❯][00]

## Související články

- [[Kvantová distribuce klíčů](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html): revoluce bankovní bezpečnosti][rel1]
- [[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html): ochranný algoritmus v kvantové éře][rel2]

[00]: /about/index.html "O Sebastienovi Rousseauovi"
[epaa]: https://emergingpaymentsasia.org/wp-content/uploads/2025/09/Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf "Bílá kniha EPAA Quantum-Safe Payments"
[rel1]: /2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Kvantová distribuce klíčů: revoluce bankovní bezpečnosti"
[rel2]: /2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: ochranný algoritmus v kvantové éře"
