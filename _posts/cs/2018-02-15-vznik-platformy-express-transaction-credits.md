---
title: "Vznik platformy Express Transaction Credits"
subtitle: "Návrh platformy Express Transaction Credits s chytrými kontrakty ERC-223."
description: "Technický rozbor toho, jak byla v roce 2018 platforma EXTC postavena na Ethereum ERC-223: architektura tokenu, výplaty s vícenásobným podpisem, časově uzamčené převody a okamžité úvěry kryté zástavou."
date: "February 15, 2018"
language: "cs-CZ"
locale: "cs_CZ"
hreflang: "cs"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Obří bílé sloupy"
keywords: "platforma EXTC, ERC-223, chytré kontrakty Ethereum, architektura tokenu, vícenásobný podpis, časově uzamčený převod, blockchainové platby, úvěry kryté zástavou, decentralizované finance, kryptoměny 2018"
---


![Obří bílé sloupy](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

> **Shrnutí pro vedení / klíčové body**
>
> - **Základní problém.** ERC-20, dominantní standard tokenů Etherea v roce 2018, měl strukturální vadu: tokeny převedené přímo na adresu chytrého kontraktu byly tiše zničeny, pokud kontrakt postrádal obslužnou funkci. Jakákoli platební platforma postavená na ERC-20 toto riziko zdědila ([Ethereum EIPs](https://eips.ethereum.org/EIPS/eip-20 "EIP-20: Token Standard")).
> - **ERC-223 jako náprava.** ERC-223 vyžadoval, aby přijímající kontrakty implementovaly funkci `tokenFallback(address, uint, bytes)`. Pokud chyběla, převod se atomicky vrátil zpět. Žádné tokeny nebylo možné tiše ztratit ([Ethereum EIPs GitHub](https://github.com/ethereum/EIPs/issues/223 "ERC-223 Token Standard Proposal")).
> - **Pět kontraktových primitiv EXTC.** Identita tokenu (název, symbol, přesnost na 18 desetinných míst), pevná nabídka, převod odpovídající ERC-223, firemní výplaty s vícenásobným podpisem a trvalé příkazy časově uzamčené na výšku bloku.
> - **Mechanismus úvěru krytého zástavou.** Dlužníci uzamkli tokeny EXTC v úschově kontraktu; kontrakt atomicky uvolnil výnos z úvěru po přijetí zástavy, bez prodlevy na upisování nebo schválení úvěrovou komisí.
> - **Co experiment odhalil o limitech Etherea.** Při propustnosti hlavní sítě kolem 15 TPS a nákladech na plyn 0,10 až 1,00 USD za transakci na vrcholu v lednu 2018 byla platební síť zpracovávající byť jen objem na úrovni remitencí ekonomicky i technicky neproveditelná na veřejném Etheru bez infrastruktury vrstvy 2.

---

## Problém návrhu: proč ERC-20 nedostačoval

Standard ERC-20, navržený v roce 2015 a formalizovaný v návrhu Ethereum Improvement Proposal 20, definoval kanonické rozhraní pro zastupitelné tokeny, které pohánělo boom ICO v letech 2017–2018. Jeho šest základních funkcí, tedy `totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve` a `allowance`, postačovalo pro jednoduché vydávání a směnu tokenů.

Pro platební platformu měl však ERC-20 vadu kritickou pro produkční nasazení. Funkce `transfer(address _to, uint256 _value)` přesouvala tokeny na jakoukoli adresu, včetně adres kontraktů, aniž by v přijímajícím kontraktu spustila jakýkoli kód. Kontrakt, který nebyl výslovně naprogramován ke sledování příchozích převodů ERC-20, neměl jak je rozpoznat. Tokeny poslané tímto způsobem zůstaly natrvalo uvězněné, bez jakéhokoli mechanismu pro jejich obnovení.

Komunita Etherea odhadovala, že tímto mechanismem se do poloviny roku 2018 natrvalo ztratily tokeny ERC-20 v hodnotě desítek milionů dolarů. Budovat platební platformu, kde by převody mohly tiše selhat a zničit prostředky uživatelů, nebylo přijatelné.

## Řešení ERC-223: atomický převod s notifikací

ERC-223, navržený v systému sledování problémů Etherea na GitHubu, řešil problém tichého ztracení tím, že změnil to, co musel převod tokenu udělat. Podle ERC-223 funkce `transfer(address _to, uint256 _value, bytes _data)` ověřila, zda adresa příjemce obsahuje kód kontraktu. Pokud ano, převod zavolal `_to.tokenFallback(address _from, uint256 _value, bytes _data)`.

Klíčová vlastnost: pokud přijímající kontrakt funkci `tokenFallback` neimplementoval, celá převodní transakce se vrátila zpět. Ze zůstatku odesílatele neodešly žádné tokeny. Žádné tokeny nezůstaly uvězněné. Převod byl atomický: buď proběhl celý s vykonáním kódu příjemce, nebo zcela selhal a stav zůstal beze změny.

Pro EXTC to znamenalo:

- **Platba chytrým kontraktům byla bezpečná už ze své konstrukce.** Úschovní kontrakty, peněženky s vícenásobným podpisem a úvěrové kontrakty mohly přijímat tokeny EXTC bez jakéhokoli rizika nevratné ztráty prostředků.
- **Pole `_data` umožnilo bohatá platební metadata.** Bajtová část mohla nést reference faktur, směrovací kódy nebo compliance potvrzení, tedy informace, které jednoduchý převod ERC-20 nedokázal přenést.
- **Náklady na plyn byly nepatrně vyšší.** Volání `tokenFallback` přidalo přibližně 2 000 až 5 000 jednotek plynu na převod, což byla při cenách plynu z roku 2018 malá režie.

## Architektura kontraktu EXTC

Kontrakt tokenu EXTC byl implementací v jazyce Solidity strukturovanou kolem pěti modulů:

### 1. Identita tokenu

```
string public name = "Express Transaction Credits";
string public symbol = "EXTC";
uint8 public decimals = 18;
```

Osmnáct desetinných míst dalo EXTC přesnost pod úrovní centu, odpovídající granularitě potřebné pro mikroplatby a mikroúvěry. Symbol `EXTC` byl identifikátor registrovaný v kontraktu tokenu na blockchainu.

### 2. Pevná celková nabídka

Celková nabídka byla stanovena při nasazení kontraktu a nebylo možné ji nafouknout dalším ražením (mint). Tato volba návrhu učinila z EXTC deflační aktivum: jakékoli tokeny natrvalo stažené z oběhu, prostřednictvím nevratných operací spálení (burn), snížily nabídku bez náhrady. Model pevné nabídky byl v návrzích platebních tokenů z roku 2018 standardem a odrážel předpoklad ovlivněný Bitcoinem, že deflační tlak je pro směnný prostředek přednost.

### 3. Zůstatek a převod odpovídající ERC-223

Základní převodní funkce implementovala celé rozhraní ERC-223. Interní mapování zůstatků sledovala držbu každé adresy. Pomocná funkce `isContract(address)` odlišovala adresy EOA (externally owned account, externě vlastněný účet) od adres kontraktů, aby určila, zda je třeba zavolat `tokenFallback`.

### 4. Firemní výplaty s vícenásobným podpisem

Firemní platební procesy vyžadovaly spoluautorizaci: žádný jednotlivý podepisující nemohl jednostranně zahájit výplatu nad stanovený práh. Kontrakt EXTC implementoval schéma vícenásobného podpisu typu dva z N:

1. Určený iniciátor navrhl převod a specifikoval příjemce, částku a nonce.
2. Spolupodepisující potvrdil nonce.
3. Převod se provedl teprve poté, co byly oba podpisy zaznamenány na blockchainu.

To pro firemní účty odstranilo riziko jediného bodu selhání a zároveň udrželo celý autorizační tok na blockchainu a auditovatelný bez zprostředníka v podobě zúčtovací instituce.

### 5. Trvalé příkazy časově uzamčené na výšku bloku

Opakované platby, tedy mzdy, předplatná a naplánované splátky úvěrů, vyžadovaly primitivum trvalého příkazu. EXTC to implementovalo jako časový zámek: záznam o převodu byl v kontraktu uložen s parametrem `releaseBlock`. Převod se nemohl provést, dokud výška bloku Etherea nedosáhla hodnoty `releaseBlock`.

Výška bloku jako náhrada za čas byla v roce 2018 pragmatickou volbou. Ethereum cílilo na interval bloku 15 sekund, což z výšky bloku činilo přiměřeně spolehlivou náhradu reálného času v rozsahu minut. Absolutní časové značky (`block.timestamp`) byly k dispozici, ale byly náchylné k manipulaci těžaři v okně ±900 sekund, takže výška bloku byla pro finanční kontrakty bezpečnějším referenčním bodem.

## Mechanismus okamžitého úvěru krytého zástavou

Úvěrové primitivum EXTC bylo nejsložitější komponentou. Návrh:

1. **Dlužník uzamkne zástavu.** Dlužník zavolal `lockCollateral(uint256 _collateralAmount)` a převedl tokeny EXTC do úschovy úvěrového kontraktu prostřednictvím `tokenFallback` podle ERC-223.
2. **Kontrola poměru úvěru k hodnotě zástavy.** Kontrakt načetl předem nastavený poměr LTV (například 50 %) a vypočítal maximální výši úvěru vůči uzamčené zástavě.
3. **Atomické vyplacení úvěru.** Pokud zástava splnila minimální práh, kontrakt okamžitě převedl výši úvěru na adresu dlužníka. Žádná fronta na upisování, žádná úvěrová komise, žádná prodleva zúčtování.
4. **Splacení a uvolnění.** Při splacení, tedy jistiny plus pevné úrokové sazby, kontrakt uvolnil zástavu zpět dlužníkovi. Nesplacení do `releaseBlock` spustilo automatickou likvidaci: kontrakt převedl zástavu na určenou adresu věřitele.

Celý tok vynucoval kód kontraktu. Žádná ze stran nemusela druhé důvěřovat ani se při vymáhání podmínek spoléhat na zprostředkovatele.

## Co experiment odhalil

Architektura kontraktu EXTC byla technicky konzistentní. ERC-223 vyřešil nejzávažnější bezpečnostní vadu ERC-20. Primitiva vícenásobného podpisu a časového zámku přímo odpovídala reálným firemním platebním procesům. Mechanismus úvěru krytého zástavou prokázal, že zajištěné úvěrování lze plně automatizovat a učinit samovynutitelným na blockchainu.

V praxi se ukázala dvě omezení:

**Náklady na plyn.** Na vrcholu v lednu 2018 dosáhly ceny plynu Etherea 50 až 100 gwei, takže jediný převod tokenu ERC-223 stál 0,50 až 2,00 USD. U mikroplateb nebo remitencí ve výši 10 až 50 USD byly tyto poplatky neúnosné.

**Propustnost.** Limit plynu na blok v hlavní síti Etherea byl na začátku roku 2018 přibližně 8 milionů jednotek plynu. Převod ERC-223 spotřeboval zhruba 50 000 až 80 000 jednotek plynu. Síť tak dokázala zpracovat přibližně 100 až 160 převodů tokenu EXTC na blok, tedy zhruba 7 až 11 za sekundu při intervalu bloku 15 sekund. Rozsah platební sítě, tedy stovky nebo tisíce transakcí za sekundu, nebyl na veřejném Etheru dosažitelný bez infrastruktury vrstvy 2, která tehdy ještě neexistovala v produkční podobě.

Šlo o omezení infrastruktury, nikoli o vady návrhu EXTC. Logika kontraktu byla správná. Podkladový blockchain zatím nedokázal unést objem plateb na úrovni finančního odvětví.

## Myšlenky, které se dostaly do produkce

Několik návrhových vzorů z EXTC potvrdil následující vývoj:

**Atomický převod tokenu s notifikací příjemce**, tedy základní vlastnost ERC-223, se stal základem pro ERC-777 (2019), který model notifikace rozšířil a který byl později začleněn do úvěrových protokolů DeFi. Vzor `tokenFallback` se objevuje napříč moderní architekturou DeFi.

**Autorizace firemních výplat s vícenásobným podpisem**, tedy vzor vyžadující před provedením více podpisů na blockchainu, se stal standardním modelem pro správu pokladny DAO a institucionální custody řešení. Gnosis Safe, spuštěný v roce 2018, tento vzor rozšířil ve velkém měřítku.

**Okamžité úvěry kryté zástavou bez zprostředkovatelů**, tedy mechanismus uzamčení zástavy v úschově a atomického uvolnění výnosu z úvěru, je základním návrhem úvěrových protokolů DeFi, jako jsou Compound (2018) a Aave (2020).

**Časové zámky na výšku bloku pro naplánované platby**, tedy vzor zakódování budoucího času provedení do kontraktu, se objevuje ve vesting kontraktech tokenů, odložených návrzích na správu (governance) a v návrzích orákulí s časově váženou průměrnou cenou (TWAP) napříč ekosystémem DeFi.

Experiment EXTC nedosáhl produkčního měřítka. Infrastruktuře potřebné k tomu, aby byl návrh životaschopný, trvalo dozrát další tři až pět let. Otázky návrhu, které kladl, byly pro rok 2018 ty správné.

## Často kladené otázky

**Proč nebyl ERC-223 nikdy přijat jako dominantní standard tokenů, přestože opravoval vadu ERC-20?**

ERC-223 vyžadoval, aby přijímající kontrakty implementovaly `tokenFallback`, což narušilo zpětnou kompatibilitu s tisíci kontraktů již nasazenými pro tokeny ERC-20. Existující ekosystém ERC-20 byl na migraci příliš velký. Následné návrhy, zejména ERC-777 a ERC-1363, řešily stejný problém s odlišnými kompromisy v kompatibilitě, ale ERC-20 zůstal dominantní díky kombinaci síťových efektů a zavedení vzorů obalených (wrapped) tokenů, které se scénáři tichého ztracení vyhnuly.

**Co se stalo s tokenem a platformou EXTC?**

EXTC byl důkaz koncepce a raný výzkumný projekt z roku 2018. Širší trh ICO a platebních tokenů se v průběhu let 2018 až 2019 prudce propadl, jak se ukázaly limity škálovatelnosti Etherea a regulační nejistota. Myšlenky obsažené v návrhu EXTC se znovu objevily v pozdějších protokolech, které měly přístup k infrastruktuře vrstvy 2, lepším nástrojům a jasnějším regulačním rámcům.

**Jak se model úvěru krytého zástavou EXTC srovnává s moderními protokoly DeFi, jako je Aave?**

Základní mechanismus je stejný: uzamknout zástavu, obdržet úvěr odměřený podle poměru LTV, splatit, nebo čelit likvidaci. Rozdíly jsou tyto: (1) moderní protokoly DeFi používají pro dynamické LTV cenové kanály z orákulí namísto pevných poměrů; (2) používají algoritmické úrokové sazby, které reagují na využití poolu; (3) fungují na sítích vrstvy 2 s náklady na plyn 10 až 100krát nižšími než v hlavní síti roku 2018; (4) Aave a Compound prošly formálními bezpečnostními audity a držely likviditu v hodnotě miliard dolarů, což empiricky potvrzuje, že základní model je funkční.

**Jaká byla na začátku roku 2018 omezení verzí jazyka Solidity?**

Kontrakt EXTC byl napsán pro Solidity 0.4.x, dominantní verzi na začátku roku 2018. Solidity 0.4 postrádal řadu bezpečnostních prvků zavedených v pozdějších verzích: kontrolu přetečení celých čísel (automaticky přidanou v 0.8.0), `require`/`revert` s chybovými hláškami (v 0.4 omezené) a explicitní viditelnost funkcí (výchozí byla v 0.4 public). Kontrakt se při ochraně proti přetečení spoléhal na knihovnu SafeMath od OpenZeppelin, což byl běžný vzor předtím, než to překladač začal vynucovat nativně.

## Reference

- Ethereum Foundation, (2015). [EIP-20: standard tokenů ⧉](https://eips.ethereum.org/EIPS/eip-20 "EIP-20 Token Standard").
- Dexaran, Ethereum GitHub, (2017). [Návrh standardu tokenu ERC-223 ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223 discussion").
- OpenZeppelin, (2018). [OpenZeppelin Contracts: SafeMath ⧉](https://github.com/OpenZeppelin/openzeppelin-contracts "OpenZeppelin Contracts").
- Ethereum Foundation, (2014). [Bílá kniha Etherea ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").
