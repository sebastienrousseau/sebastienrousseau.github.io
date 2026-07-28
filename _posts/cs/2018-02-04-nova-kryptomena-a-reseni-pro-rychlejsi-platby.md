---
title: "Představení nové kryptoměny a řešení pro rychlejší platby"
seo_title: "Nová kryptoměna a řešení pro rychlejší platby"
subtitle: "Nová kryptoměna a řešení rychlejších plateb pro finance nové generace."
description: "Na začátku roku 2018 platforma EXTC zkoumala rychlejší přeshraniční platby prostřednictvím chytrých kontraktů Ethereum ERC-223. Byl to raný nákres toho, co později vybudovaly decentralizované finance."
excerpt: "Platforma Express Transaction Credits (EXTC) byla experimentem z počátku roku 2018 v oblasti programovatelných plateb na Ethereu. Využívala chytré kontrakty ERC-223 k umožnění okamžitých přeshraničních převodů a atomických platebních toků, tedy myšlenek, které decentralizované finance později škálovaly."
author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
name: "Sebastien Rousseau"
banner_alt: "Vypnutý notebook na hnědém dřevěném stole"
banner: "https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
image_alt: "Černobílý portrét Sebastiena Rousseaua"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
logo_alt: "Logo Sebastiena Rousseaua"
cdn: "https://cloudcdn.pro/clients"
date: "Feb 04, 2018"
language: "cs"
locale: "cs_CZ"
hreflang: "cs"
keywords: "EXTC, ERC-223, chytré kontrakty Ethereum, rychlejší platby, kryptoměna, blockchainové platby, platební token, decentralizované finance, ERC-20, přeshraniční platby"
tags: "EXTC, ERC-223, Ethereum, chytré kontrakty, kryptoměna, blockchain, rychlejší platby, decentralizované finance, platební token, přeshraniční platby, ISO 20022, postkvantová kryptografie, AI, tokenizované vklady, stablecoiny"
id: "https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html"
permalink: "https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html"
url: "https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html"
measurementID: "G-169G4ET5HQ"
theme-color: "0, 67, 165"
last_reviewed: "2026-05-11"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/rss.xml"
item_title: "Představení nové kryptoměny a řešení pro rychlejší platby"
item_description: "Na začátku roku 2018 platforma EXTC zkoumala rychlejší přeshraniční platby prostřednictvím chytrých kontraktů Ethereum ERC-223. Raný nákres toho, co později vybudovalo DeFi."
item_guid: "https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/rss.xml"
item_link: "https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/rss.xml"
item_pub_date: "Sun, 04 Feb 2018 06:06:06 +0000"
last_build_date: "Sun, 04 Feb 2018 06:06:06 +0000"
pub_date: "Sun, 04 Feb 2018 06:06:06 +0000"

# Twitter Card - The Twitter Card front matter (YAML).
twitter_creator: "@wwdseb"
twitter_description: "Na začátku roku 2018 platforma EXTC zkoumala rychlejší přeshraniční platby prostřednictvím chytrých kontraktů Ethereum ERC-223. Raný nákres decentralizovaných financí."
twitter_image_alt: "Logo Sebastiena Rousseaua"
twitter_site: "@wwdseb"
twitter_title: "Představení nové kryptoměny a řešení pro rychlejší platby"
twitter_url: "https://sebastienrousseau.com"

thanks: "Děkujeme za přečtení!"
---


![Velmi vysoká budova plná otvorů](https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp).class=\"img-fluid clearfix\"

> **Shrnutí pro vedení / klíčové body**
>
> - **Základní hypotéza.** Chytré kontrakty Etherea by mohly u přeshraničních plateb nahradit štafetový závod korespondenčního bankovnictví, zúčtovat je v řádu sekund místo dnů a odstranit vrstvu poplatků ve výši 3 až 7 % ([Světová banka, 2018](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data "World Bank Remittance Prices")).
> - **Konkrétní přínos ERC-223.** Standard odstranil chybu tichého ztracení tokenů v ERC-20 tím, že po chytrých kontraktech vyžadoval zpřístupnění funkce `tokenFallback`. Neúspěšné převody se tak vrátí zpět, místo aby nevratně spálily tokeny ([Ethereum EIPs](https://eips.ethereum.org/EIPS/eip-20 "EIP-20: Token Standard")).
> - **Platební primitiva EXTC.** Návrh tokenu podporoval jednotlivé atomické převody, časově spouštěné trvalé příkazy, firemní výplaty s vícenásobným podpisem a okamžité mikroúvěry kryté zástavou. To vše bez zúčtovací instituce.
> - **Co experiment odhalil.** Technický návrh byl konzistentní, ale hlavní síť Etherea v roce 2018 zpracovávala zhruba 15 transakcí za sekundu. Objem plateb ve velkém měřítku vyžadoval řešení vrstvy 2, která ještě nebyla připravená pro produkční nasazení.
> - **Odkaz.** Architektonické myšlenky EXTC, tedy programovatelné peníze, atomické zúčtování a logika tokenu se zabudovanou compliance, se znovu objevily v pozdějších protokolech DeFi, návrzích CBDC a rámcích tokenizovaných vkladů.

---

## Problém: přeshraniční platby v roce 2018

Mezinárodní platby byly na začátku roku 2018 svou podstatou pomalé, drahé a neprůhledné. Retailový převod ze Spojeného království do jihovýchodní Asie obvykle procházel dvěma až čtyřmi korespondenčními bankami, z nichž každá si účtovala poplatek a přidávala den do zúčtovacího řetězce. Databáze Světové banky Remittance Prices Worldwide zaznamenala v prvním čtvrtletí 2018 celosvětové průměrné náklady 6,9 % za převod částky 200 USD.

Kryptoměny už prokázaly, že digitální hotovost mezi rovnocennými uzly je technicky proveditelná. Bitcoin zúčtovával transakce po celém světě zhruba za deset minut a programovatelná vrstva Etherea přidala chytré kontrakty, tedy samočinně se vykonávající kód, který dokáže zakódovat platební pravidla přímo do samotného převodu. Prostor pro návrh, do něhož EXTC vstoupilo, byl daný rozdílem mezi tím, co bylo technicky možné na blockchainu, a tím, co dodávalo tradiční korespondenční bankovnictví.

## Technický základ: ERC-20 a jeho slabina

Standard ERC-20, formalizovaný v návrhu Ethereum Improvement Proposal 20, definoval kanonické rozhraní pro zastupitelné tokeny: `balanceOf`, `transfer`, `transferFrom`, `approve` a `allowance`. Na začátku roku 2018 byl ERC-20 dominantním standardem tokenů, se stovkami tokenů nasazenými v hlavní síti.

ERC-20 měl však strukturální problém. Když se tokeny posílaly přímo na adresu chytrého kontraktu pomocí standardní funkce `transfer`, kontrakt neměl jak příchozí převod rozpoznat ani na něj reagovat. Takto poslané tokeny zůstaly natrvalo uvězněné. Komunita Etherea odhadovala, že do poloviny roku 2018 se tímto způsobem ztratily tokeny ERC-20 v hodnotě milionů dolarů.

ERC-223, který navrhl Dexaran v systému sledování problémů Etherea na GitHubu, to řešil tak, že přijímajícím kontraktům přidal požadavek na funkci `tokenFallback(address _from, uint _value, bytes _data)`. Pokud přijímající kontrakt funkci `tokenFallback` neimplementoval, převod se vrátil zpět a tokeny se vrátily odesílateli. Díky tomu byly převody ERC-223 atomické: buď kontrakt tokeny přijal a vykonal svou logiku, nebo transakce čistě selhala.

## Návrh tokenu EXTC

Token Express Transaction Credits byl navržen kolem pěti základních vlastností:

- **Název, symbol a desetinná místa.** Standardní identifikační pole ERC-223, s 18 desetinnými místy pro přesnost pod úrovní centu.
- **Celková nabídka.** Pevně stanovená v okamžiku vytvoření (mint), což z EXTC činilo deflační aktivum, protože ztracené nebo nevyzvednuté tokeny nebylo možné znovu vydat.
- **Zůstatek a převod.** Standardní funkce pro čtení a zápis, rozšířené o požadavek `tokenFallback` ze standardu ERC-223.
- **Podpora vícenásobného podpisu.** Firemní výplaty vyžadovaly před provedením spolupodpis z několika autorizovaných adres, což poskytovalo auditní stopu bez centralizované zúčtovací instituce.
- **Časově uzamčené převody.** Primitivum trvalého příkazu umožňovalo EXTC naplánovat budoucí platby. Šlo o schopnost, k níž tradiční bankovní převody potřebovaly externí pokyn.

## Platební primitiva, na která platforma cílila

Architektura EXTC byla navržena tak, aby nahradila čtyři konkrétní platební pracovní postupy, které tradiční systémy zvládaly neefektivně:

**Jednotlivé atomické platby**: jednorázový převod, který se zúčtoval v jediné transakci Etherea, obvykle do 15 až 30 sekund v hlavní síti roku 2018.

**Časově založené trvalé příkazy**: opakované převody zakódované jako časově uzamčená volání chytrých kontraktů, které odstranily potřebu, aby banka přijímala a znovu prováděla periodické pokyny.

**Hromadné firemní výplaty**: dávkové platby více příjemcům v jedné transakci, kdy každý jednotlivý převod vyžadoval autorizaci vícenásobným podpisem, což snižovalo náklady a riziko protistrany.

**Okamžité úvěry kryté zástavou**: dlužníci uzamkli tokeny EXTC jako zástavu v chytrém kontraktu; kontrakt uvolnil výnos z úvěru automaticky po přijetí, bez úvěrové komise a prodlev spojených s upisováním.

## Co experiment odhalil

Návrh EXTC byl technicky konzistentní. Základ ERC-223 vyřešil nejzávažnější bezpečnostní slabinu dominantního standardu tokenů a platební primitiva se přímo mapovala na reálné pracovní postupy, které korespondenční bankovnictví zvládalo neefektivně.

Praktickým omezením byla propustnost Etherea. V prvním čtvrtletí 2018 dosahovala hlavní síť průměrně 15 transakcí za sekundu s limitem plynu (gas) přibližně 8 milionů na blok. Platební síť zpracovávající byť jen malý zlomek celosvětového objemu remitencí, kdy Světová banka odhadovala, že v roce 2017 posílalo peníze domů 270 milionů migrantů, by hlavní síť zahltila během několika minut.

Škálovací řešení vrstvy 2, zejména stavové kanály a rané verze toho, co se stalo technologií rollup, byla v roce 2018 předmětem aktivního výzkumu, ale nebyla připravená pro produkci. Síť Lightning Network se právě spustila v hlavní síti Bitcoinu v lednu 2018 s významnými výhradami. Technické předpoklady k tomu, aby platební síť postavená na blockchainu fungovala v měřítku korespondenčních bank, ještě neexistovaly.

## Myšlenky, které přežily

Několik architektonických konceptů z EXTC a ze soudobých projektů platebních tokenů potvrdil následný vývoj:

**Programovatelné peníze**, tedy kódování platebních pravidel přímo do logiky převodu, se staly ústředním prvkem úvěrových protokolů DeFi, jako jsou Compound a Aave, spuštěných v letech 2018 a 2020.

**Atomické zúčtování bez zúčtovacích institucí**, tedy vlastnost, kdy převod buď zcela uspěje, nebo se vrátí zpět, je dnes požadavkem na návrh v rámcích tokenizovaných vkladů a v architekturách velkoobchodních CBDC, které zkoumají centrální banky včetně Bank of England a Evropské centrální banky.

**Tokeny se zabudovanou compliance**, tedy omezení převodů a ohlašovací povinnosti zakódované přímo v kontraktu tokenu, se objevují v regulovaných standardech tokenů, jako je ERC-1400 (tokeny cenných papírů), a v návrzích compliance vrstvy pro Project Agorá a podobné tokenizační experimenty více centrálních bank.

Experiment EXTC nedosáhl produkčního měřítka, ale otázky, které kladl, tedy otázky o programovatelném zúčtování, atomických převodech a samovynucujících se platebních pravidlech, byly pro rok 2018 těmi správnými otázkami. Infrastruktura potřebná k jejich zodpovězení dozrávala dalších pět let.

## Často kladené otázky

**Co byl ERC-223 a proč jej EXTC použilo místo ERC-20?**

Tokeny ERC-20 poslané přímo na adresy chytrých kontraktů se tiše ztrácely, protože kontrakty neměly jak příchozí převod rozpoznat. ERC-223 to napravil tím, že po přijímajících kontraktech vyžadoval implementaci funkce `tokenFallback`; pokud funkce chyběla, převod se vrátil zpět, místo aby tokeny spálil. EXTC přijalo ERC-223, aby byly všechny převody na blockchainu atomické a bezpečné.

**Proč rané projekty platebních tokenů neškálovaly natolik, aby nahradily korespondenční bankovnictví?**

Hlavní síť Etherea v roce 2018 zpracovávala zhruba 15 transakcí za sekundu. Samotné celosvětové objemy remitencí, bez financování obchodu a firemních plateb, by vyžadovaly desítky tisíc transakcí za sekundu. Škálovací infrastruktura vrstvy 2 potřebná k dosažení takové propustnosti nebyla připravená pro produkci až do let 2021 až 2023.

**Co se stalo s myšlenkami, které za EXTC stály?**

Základní koncepty, tedy programovatelná platební pravidla, atomické zúčtování a logika tokenu se zabudovanou compliance, převzaly protokoly DeFi, regulované standardy tokenů cenných papírů (ERC-1400) a výzkum digitálních měn centrálních bank. Rámce tokenizovaných vkladů, které dnes komerční banky pilotují, přímo navazují na návrhové otázky, jež jako první položily rané experimenty s platebními tokeny, jako bylo EXTC.

**Jak si návrh EXTC z roku 2018 stojí oproti návrhům tokenizovaných vkladů z roku 2026?**

Model zúčtování je podobný: tokeny představující peněžní pohledávky, převáděné atomicky na distribuované účetní knize. Klíčové rozdíly jsou tyto: (1) tokenizované vklady z roku 2026 jsou závazky komerčních bank, nikoli tokeny na doručitele; (2) fungují na povolených nebo hybridních účetních knihách s regulačním dohledem, nikoli ve veřejné hlavní síti; (3) compliance a ověření totožnosti se vynucují na úrovni protokolu, nikoli se ponechávají na účastnících.

## Reference

- Ethereum Foundation, (2018). [EIP-20: standard tokenu ⧉](https://eips.ethereum.org/EIPS/eip-20 "EIP-20 Token Standard").
- Dexaran, Ethereum GitHub, (2017). [Návrh standardu tokenu ERC-223 ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223 discussion").
- Světová banka, (2018). [Remittance Prices Worldwide, 1. čtvrtletí 2018 ⧉](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data "World Bank Remittance Prices").
- Buterin, V., (2014). [Ethereum: chytré kontrakty a decentralizovaná aplikační platforma nové generace ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").
