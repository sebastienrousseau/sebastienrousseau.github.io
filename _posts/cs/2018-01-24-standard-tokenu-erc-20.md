---
title: "ERC-20: rozhraní ethereového tokenu, které změnilo svět"
subtitle: "Tokeny ERC-20, chytré kontrakty Etherea a standardizace digitálních aktiv."
description: "ERC-20 je nejběžnější typ tokenu používaný na blockchainu Ethereum a často se označuje jako digitální chytrý kontrakt."
date: "January 24, 2018"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Vypnutý notebook na hnědém dřevěném stole"
keywords: "ERC-20, Ethereum, token, chytrý kontrakt, DeFi, EIP, blockchain, interoperabilita, DApps, standard"
---


> **TL;DR.** ERC-20 je nejběžnější typ tokenu na blockchainu Ethereum a často se označuje jako digitální chytrý kontrakt.

**Klíčové body**

- **Myšlenka.** Standard ERC-20 definuje šest základních funkcí, které musí implementovat každý token kompatibilní s ERC-20.
- **Dopad.** Standard ERC-20 měl významný vliv na ekosystém Ethereum.
- **Motivace.** Standardizace zavedená protokolem ERC-20 měla i přímý ekonomický dopad.
- **Potřeba standardizovaného rozhraní tokenu.** Před příchodem standardu ERC-20 (Ethereum Request for Comments 20) připomínal blockchain Ethereum divoký západ tokenových architektur.

![Vypnutý notebook na hnědém dřevěném stole](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

## Poznatek

### Potřeba standardizovaného rozhraní tokenu

Před příchodem standardu ERC-20 (Ethereum Request for Comments 20) připomínal blockchain Ethereum divoký západ tokenových architektur. Každý nově vydaný token měl vlastní sadu pravidel, funkcí a rozhraní. To vývojáře stavělo před náročnou křivku učení a zároveň bránilo interoperabilitě tokenů. V zásadě byl každý nový token jako nový jazyk, který bylo třeba se naučit, pochopit a implementovat. Tato roztříštěnost brzdila škálovatelnost a širší přijetí tokenů na platformě Ethereum.

Zavedení standardu ERC-20 posloužilo jako sjednocující jazyk. Stanovilo společnou sadu pravidel a funkcí, kterými se musí řídit všechny tokeny Etherea. Vývojáři teď mají k dispozici konzistentní rozhraní bez ohledu na to, o jaký token jde. Tato standardizace zjednodušila procesy interakce s tokeny a umožnila plynulejší integraci do různých aplikací a služeb. Vývojáři díky tomu mohou s tokeny pracovat smysluplněji, což vytváří prostředí příznivé pro inovace a růst v ekosystému Ethereum.

#### Divoký západ tokenových architektur

Blockchain Ethereum byl původně navržen tak, aby podporoval jediný typ tokenu: ETH. S rostoucí popularitou platformy však vývojáři začali vytvářet vlastní tokeny, které představovaly nejrůznější aktiva a koncepty. To vedlo k rozmachu různých tokenových architektur, z nichž každá měla vlastní sadu pravidel a funkcí.

Tato roztříštěnost vývojářům ztěžovala tvorbu aplikací, které by dokázaly pracovat s více tokeny. Uživatelům zase komplikovala správu jejich tokenových aktiv napříč různými platformami.

#### Standard ERC-20

Standard ERC-20 byl představen v roce 2015, aby řešil problémy, které přinesl divoký západ tokenových architektur. Standard definuje společnou sadu pravidel a funkcí, kterými se musí řídit všechny tokeny Etherea. Tato standardizace usnadňuje vývojářům tvorbu aplikací schopných pracovat s libovolným tokenem ERC-20 a uživatelům zjednodušuje správu jejich tokenových aktiv.

Standard ERC-20 komunita Etherea široce přijala. Dnes existuje přes 200 000 tokenů ERC-20 a standard využívá široká škála aplikací, včetně decentralizovaných burz, úvěrových platforem a herních dapp aplikací.

## Myšlenka

### Společná sada funkcí a vlastností pro všechny tokeny

Standard ERC-20 definuje šest základních funkcí, které musí implementovat každý token kompatibilní s ERC-20. Tyto funkce jsou:

- `transfer(address to, uint256 amount)`: Převede určité množství tokenů z adresy volajícího na zadanou adresu.
- `approve(address spender, uint256 amount)`: Povolí zadané adrese utratit určité množství tokenů jménem volajícího.
- `allowance(address owner, address spender)`: Vrátí množství tokenů, které smí zadaný spender utratit jménem zadaného ownera.
- `totalSupply()`: Vrátí celkový počet tokenů v oběhu.
- `balanceOf(address owner)`: Vrátí počet tokenů vlastněných zadanou adresou.
- `name()`: Vrátí název tokenu.
- `symbol()`: Vrátí symbol tokenu.

Standard ERC-20 dále definuje dvě události, které musí být vyvolány po úspěšném provedení odpovídajících funkcí. Tyto události jsou:

- `Transfer(address from, address to, uint256 amount)`: Vyvolána, když je určité množství tokenů převedeno z jedné adresy na druhou.
- `Approval(address owner, address spender, uint256 amount)`: Vyvolána, když je zadané adrese povoleno utratit určité množství tokenů jménem zadaného ownera.

## Dopad

### Růst DeFi a přijetí Etherea

Standard ERC-20 měl významný vliv na ekosystém Ethereum. Byl klíčovým předpokladem hnutí DeFi (decentralizované finance) a přispěl také k širšímu přijetí Etherea.

Platformy DeFi, které nabízejí řadu finančních služeb od půjček po správu aktiv, se při zpracování transakcí silně opírají o tokeny. Díky tomu, že ERC-20 funguje jako univerzální adaptér, mohou aplikace DeFi mnohem snáze zapojit širokou škálu tokenů, aniž by musely přizpůsobovat svůj kód každému z nich.

Standard ERC-20 také uživatelům usnadnil správu tokenových aktiv. Protože se tokeny řídí stejnými základními pravidly, mohou je uživatelé snáze převádět, utrácet a spravovat napříč více platformami. Tato zlepšená uživatelská zkušenost byla jedním z hnacích faktorů rostoucí míry přijetí Etherea.

## Motivace

### Nižší náklady na vývoj a vyšší bezpečnost

Standardizace, kterou přinesl protokol ERC-20, měla i přímý ekonomický dopad. Tím, že poskytl ověřený a komunitou schválený vzor pro tvorbu tokenů, výrazně snížil bariéry vstupu pro vývojáře. Ti mohou nyní vytvořit nový token s nižšími náklady na vývoj a rychlejším uvedením na trh, protože již nemusí znovu vynalézat kolo. Standard rovněž nepřímo podporuje tvorbu aplikací DApps (decentralizované aplikace) a služeb, které dokážou univerzálně pracovat s libovolným tokenem ERC-20, a tím přispívá k živějšímu ekosystému.

Dalším významným přínosem je vyšší bezpečnost. Standard ERC-20 prošel důkladným prověřením komunitou Etherea, což z něj činí robustní a bezpečný model pro implementaci tokenů. Dodržování tohoto standardu znamená, že základní aspekty chytrého kontraktu tokenu odpovídají osvědčeným postupům přijímaným komunitou. To minimalizuje riziko bezpečnostních zranitelností, které by jinak mohly vyplynout z nesprávně navrženého modelu tokenu. Není to sice záruka proti všem typům zranitelností, ale je to významný krok k zajištění celkové bezpečnosti tokenů a potažmo i projektů, které je využívají.

![oddělovač](https://cloudcdn.pro/clients/common/images/elements/divider.svg).class=\"m-10 w-100\"

**Tím se naše společná chvíle uzavírá. Děkuji za váš čas!**

Máte-li jakékoli dotazy, neváhejte mě kontaktovat přes [LinkedIn ⧉][11] nebo prostřednictvím [kontaktní stránky][10]. Ještě jednou děkuji za váš čas a těším se na vaši zprávu.

[**❬ Zpět na články**][09]

[09]: /articles/index.html "Zpět na články"
[10]: /contact/index.html "Kontaktovat Sebastiena Rousseaua"
[11]: https://www.linkedin.com/in/sebastienrousseau/ "Sebastien Rousseau na LinkedIn"
