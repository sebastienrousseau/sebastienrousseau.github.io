---
author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Abstraktní bloky digitální účetní knihy propojené světelnými stopami na tmavém pozadí"
banner_height: "100vh"
banner_width: "100vw"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
cdn: "https://cloudcdn.pro/clients"
changefreq: "weekly"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2007 - 2026 - Sebastien Rousseau. All rights reserved."
date: "Jan 09, 2018"
description: "Technický úvod do fungování blockchainu: kryptografické hashovací řetězce, Merkleovy stromy, distribuovaný konsenzus a proč programovatelná vrstva Etherea proměnila platební účetní knihu v platformu pro chytré kontrakty a tokenizovaná aktiva."
format-detection: "telephone=no"
hreflang: "cs"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/cs/2018-01-09-understanding-the-technology-behind-blockchain"
image_alt: "Černobílý portrét Sebastiena Rousseaua"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "technologie blockchainu, kryptografický hash, Merkleův strom, distribuovaný konsenzus, proof of work, Ethereum, chytré kontrakty, EVM, Solidity, ERC-20, distribuovaná účetní kniha, decentralizované finance"
language: "cs"
layout: "report"
locale: "cs_CZ"
logo_alt: "Logo Sebastiena Rousseaua"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: "active"
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/cs/2018-01-09-understanding-the-technology-behind-blockchain"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "sebastienrousseau"
subtitle: "Praktický průchod kryptografií a konsenzem, na nichž blockchain stojí."
tags: "blockchain, Ethereum, chytré kontrakty, kryptografie, Merkleův strom, mechanismus konsenzu, proof of work, EVM, Solidity, ERC-20, decentralizované finance, ISO 20022, postkvantová kryptografie, AI, stablecoiny, tokenizované vklady"
theme-color: "0, 67, 165"
title: "Pochopení technologie za blockchainem"
url: "https://sebastienrousseau.com/cs/2018-01-09-understanding-the-technology-behind-blockchain"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/rss.xml"
category: "Blockchain"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Technický úvod do blockchainu: kryptografické hashovací řetězce, Merkleovy stromy, distribuovaný konsenzus a jak Ethereum rozšířilo platební účetní knihu na programovatelnou platformu."
item_guid: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/rss.xml"
item_link: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/rss.xml"
item_pub_date: "Tue, 09 Jan 2018 09:09:00 +0000"
item_title: "Pochopení technologie za blockchainem"
last_build_date: "Tue, 09 Jan 2018 09:09:00 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Tue, 09 Jan 2018 09:09:00 +0000"
ttl: "60"
type: "website"
webmaster: "contact@sebastienrousseau.com"
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "Blockchain Tech"
apple-touch-fullscreen: "yes"
msapplication-navbutton-color: "0, 67, 165"
twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "Jak blockchain funguje: kryptografické hashovací řetězce, Merkleovy stromy, mechanismy konsenzu a jak Ethereum proměnilo účetní knihu v programovatelnou platformu."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo Sebastiena Rousseaua"
twitter_site: "@wwdseb"
twitter_title: "Pochopení technologie za blockchainem"
twitter_url: "https://sebastienrousseau.com"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Děkujeme za přečtení!"
site_last_updated: "2023-07-05"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
site_software: "Static Site Generator, Rust"
excerpt: "Blockchain je účetní kniha s možností pouze přidávat záznamy, zabezpečená kryptografickými hashovacími řetězci a distribuovaným konsenzem. Jde o návrh, který činí manipulaci výpočetně nákladnou a auditovatelnou kýmkoli. Ethereum tento základ rozšířilo o programovatelnou prováděcí vrstvu a proměnilo jednoduchý platební záznam v platformu pro chytré kontrakty, tokeny a decentralizované finance."
last_reviewed: "2026-05-24"
---

![Abstraktní bloky digitální účetní knihy propojené světelnými stopami na tmavém pozadí](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

> **Shrnutí pro vedení / Klíčové body**
>
> - **Problém.** Digitální hotovost vyžaduje vyřešení problému dvojí útraty: zabránit tomu, aby byla stejná jednotka utracena dvakrát bez důvěryhodné clearingové instituce. Bílá kniha Bitcoinu z roku 2008 to vyřešila nahrazením důvěryhodných prostředníků kryptografickým důkazem a distribuovaným konsenzem ([Nakamoto, 2008](https://bitcoin.org/bitcoin.pdf "Bitcoin: A Peer-to-Peer Electronic Cash System")).
> - **Datová struktura.** Blockchain je spojový seznam bloků, kde hlavička každého bloku obsahuje hash SHA-256 předchozí hlavičky. Hashovací řetězec činí historii pouze přidávatelnou: úprava jakéhokoli minulého bloku zneplatní každý následující hash a nutí útočníka znovu provést veškerý následný proof-of-work.
> - **Merkleovy stromy.** Transakce v bloku jsou hashovány do binárního Merkleova stromu. Kořenový hash uložený v hlavičce bloku umožňuje efektivní ověření kterékoli jednotlivé transakce bez stažení celého bloku, což je základ odlehčených klientů SPV.
> - **Rozšíření Etherea.** Žlutá kniha Etherea (2014) představila EVM, deterministický zásobníkový stroj běžící na každém plném uzlu. Chytré kontrakty jsou bytecode nasazený na řetězec; vykonávají se identicky na všech uzlech a vypořádávají se atomicky, čímž nahrazují důvěryhodné prostředníky kódem, který sám sebe vynucuje ([Wood, 2014](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper")).
> - **Praktický význam.** Každé tokenizované aktivum, stablecoin a protokol DeFi nasazený od roku 2017 běží na těchto základech. Pochopení hashovacího řetězce, Merkleova stromu a prováděcího modelu EVM je předpokladem pro práci s jakýmkoli systémem založeným na Ethereu.

---

## Problém, který blockchain vyřešil

Před Bitcoinem vyžadovaly digitální platby důvěryhodného prostředníka, banku, zpracovatele plateb nebo clearingové centrum, aby se zabránilo dvojí útratě. Pokud Alice poslala Bobovi digitální soubor představující 10 liber, samotný soubor jí nijak nebránil poslat identickou kopii Carol. Řešením ve všech tehdejších systémech bylo centralizované vedení záznamů: účetní kniha banky uváděla, že peníze byly utraceny, takže je nebylo možné utratit znovu.

Přínosem Bitcoinu bylo nahradit tuto důvěryhodnou účetní knihu distribuovanou, v níž je záznam všech transakcí replikován napříč tisíci nezávislých uzlů. Vzájemná nedůvěra mezi uzly se prostřednictvím dvou mechanismů proměnila v bezpečnost:

1. **Kryptografické propojení.** Každý blok transakcí obsahuje hash předchozího bloku. Hashovací funkce je jednosměrné deterministické zobrazení: pro libovolný vstup funkce vytvoří výstup pevné délky a změna byť jediného bitu vstupu vytvoří zcela odlišný výstup. To znamená, že jakákoli úprava historického bloku zneplatní každý blok po něm.

2. **Konsenzus proof-of-work.** Přidání nového bloku vyžaduje nalezení hodnoty nonce takové, aby hash bloku klesl pod cílovou prahovou hodnotu, což je výpočetně nákladné nalézt, ale triviálně levné ověřit. Tím se přepis historie stává nákladným úměrně hloubce upravovaného bloku, protože útočník musí znovu provést veškerý proof-of-work od tohoto bloku až po vrchol řetězce.

Tato kombinace znamená, že nejdelší řetězec s největším kumulativním proof-of-work je z podstaty svého návrhu ten, který udržují poctiví účastníci vynakládající reálné zdroje.

## Kryptografické stavební kameny

Technologie blockchainu skládá tři již existující kryptografické primitivy do nové architektury:

### Hashovací funkce SHA-256

SHA-256 (Secure Hash Algorithm 256-bit) je členem rodiny SHA-2 standardizované institutem NIST. Přijímá vstup libovolné délky a vytváří 256bitový výstup. Klíčové vlastnosti pro použití v blockchainu:

- **Determinismus.** Stejný vstup vždy vytvoří stejný výstup.
- **Odolnost vůči nalezení vzoru.** Ze zadaného hashovacího výstupu je výpočetně neproveditelné rekonstruovat vstup.
- **Lavinový efekt.** Změna jednoho bitu vstupu změní zhruba polovinu výstupních bitů, což činí vyhledávání hrubou silou neefektivním.
- **Odolnost vůči kolizím.** Je výpočetně neproveditelné najít dva různé vstupy, které vytvoří stejný hash.

Bitcoin aplikuje SHA-256 dvakrát (SHA-256d) pro zvýšenou bezpečnost proti útokům prodloužením délky. Ethereum používá Keccak-256, variantu finalisty SHA-3.

### Merkleovy stromy

Merkleův strom je binární strom hashů. Každý listový uzel je hash transakce. Každý vnitřní uzel je hash svých dvou potomků. Kořen, tedy Merkleův kořen, shrnuje všechny transakce v bloku do jediné 32bajtové hodnoty uložené v hlavičce bloku.

Praktický důsledek: k ověření, že určitá transakce je zahrnuta v bloku, potřebujete pouze `log₂(n)` hashů, nikoli všech `n` transakcí. U bloku s 2 000 transakcemi vyžaduje ověření 11 hashů namísto 2 000, což je základ zjednodušeného ověřování plateb (SPV) v odlehčených klientech.

### Digitální podpisy (ECDSA)

Autorizace transakcí v Bitcoinu a Ethereu využívá algoritmus digitálního podpisu na eliptických křivkách (ECDSA) nad křivkou secp256k1. Soukromý klíč podepíše transakci; kterýkoli uzel může podpis ověřit pomocí odpovídajícího veřejného klíče, aniž by znal soukromý klíč. Tím je zajištěno, že pouze držitel soukromého klíče může autorizovat útratu z adresy.

Adresy Etherea tvoří posledních 20 bajtů hashe Keccak-256 veřejného klíče. Toto odvození činí adresy kompaktní a přenositelné, přičemž zůstávají kryptograficky vázány na pár klíčů.

## Jak funguje blockchain Bitcoinu

Blok Bitcoinu obsahuje tři logické komponenty:

**Hlavička bloku** představuje 80 bajtů zahrnujících: verzi protokolu, hash hlavičky předchozího bloku, Merkleův kořen transakcí, časové razítko Unix, aktuální cíl obtížnosti a nonce. Těžaři iterují nonce (a někdy časové razítko nebo extra-nonce v transakci coinbase), dokud dvojitý hash SHA-256 hlavičky neklesne pod cíl obtížnosti.

**Seznam transakcí** je uspořádaná množina transakcí zahrnutých v bloku. Transakce coinbase (první) přiděluje odměnu za blok a transakční poplatky na adresu těžaře.

**Řetězec** je propojení hlaviček. Kumulativní proof-of-work v řetězci (součet veškeré práce vykonané k vytvoření každého bloku) určuje, který fork je kanonickým řetězcem. Uzly vždy následují řetězec s největší kumulativní prací.

Doba bloku je u Bitcoinu cílena na 10 minut. Obtížnost se upravuje každých 2 016 bloků (přibližně dva týdny), aby se tento cíl udržel se změnami celkového hashovacího výkonu sítě.

## Programovatelná vrstva Etherea

Ethereum zobecnilo transakční model Bitcoinu z „přenosu hodnoty" na „provedení kódu". Klíčové doplňky:

**Virtuální stroj Etherea (EVM).** Zásobníkový virtuální stroj se 256bitovým slovem, který se deterministicky vykonává na všech plných uzlech. Každý opcode má explicitní náklad na gas. Výpočet je omezen limitem gas na blok, což brání nekonečným smyčkám zastavit síť. Všechny uzly vykonávající stejný bytecode nad stejným stavem musí vytvořit stejný výstup; tento konsenzus nad prováděním je to, co činí chytré kontrakty bezdůvěrnými.

**Účty.** Ethereum má dva typy účtů: externě vlastněné účty (EOA) řízené soukromými klíči a účty kontraktů, jejichž kód je uložen na řetězci. Transakce odeslaná na adresu kontraktu spustí provedení bytecode kontraktu.

**Stav.** Globální stav Etherea je mapování adres na stavy účtů (nonce, zůstatek, úložiště, hash kódu). Kořen stavu, Merkleovo-Patriciovo trie všech stavů účtů, je zahrnut v každé hlavičce bloku a umožňuje efektivní důkaz stavu libovolného účtu v libovolné výšce bloku.

**Gas.** Uživatelé platí gas (v ETH) za každou operaci EVM. Gas plní dvě funkce: kompenzuje těžaře a validátory za výpočet a omezuje zdroje, které může jediná transakce spotřebovat, čímž brání útokům typu odepření služby prostřednictvím nákladných operací.

## Psaní chytrých kontraktů v Solidity

Solidity je staticky typovaný, na kontrakty orientovaný jazyk, který se kompiluje do bytecode EVM. Základní koncepty ilustruje minimální kontrakt tokenu:

```solidity
pragma solidity ^0.8.0;

contract MyToken {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 _totalSupply
    ) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _totalSupply;
        balanceOf[msg.sender] = _totalSupply;
    }

    function transfer(address _to, uint256 _value) external returns (bool) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}
```

Klíčová pozorování: `mapping(address => uint256)` je rozvržení úložiště EVM, nikoli datová struktura v paměti; čtení a zápisy stojí gas. `require` při selhání vrátí celou transakci a vrací nevyužitý gas. `event Transfer` vyzařuje log, který indexery mimo řetězec využívají ke sledování převodů bez opětovného čtení celého stavu. `constructor` se spustí jednou při nasazení; následná volání směřují do pojmenovaných funkcí.

Standard ERC-20 formalizoval společné rozhraní pro zaměnitelné tokeny, `transfer`, `transferFrom`, `approve`, `allowance`, `balanceOf`, `totalSupply`, což umožňuje libovolnému tokenu vyhovujícímu ERC-20 fungovat s libovolnou burzou nebo peněženkou znající ERC-20 bez vlastní integrace.

## Od účetní knihy k finanční infrastruktuře

Zde popsané primitivy blockchainu, hashovací řetězce, Merkleovy stromy, EVM a ERC-20, se staly základem pro širší soubor finančních aplikací mezi lety 2018 a 2026:

**Decentralizované finance (DeFi).** Zápůjční protokoly (Compound, Aave), automatizovaní tvůrci trhu (Uniswap) a agregátory výnosů běží všechny jako chytré kontrakty EVM. Nahrazují funkce clearingu, úschovy a vypořádání tradičních finančních prostředníků samočinně vykonávaným kódem a likviditními pooly na řetězci.

**Tokenizovaná aktiva.** Centrální banky a komerční banky pilotují tokenizované vklady, tokenizované dluhopisy a tokenizované fondy peněžního trhu na povolovaných variantách řetězců kompatibilních s EVM. Základní mechanika, hashem zabezpečené přechody stavů, atomické vypořádání a programovatelná pravidla převodů, je přímým potomkem architektury Etherea z roku 2014.

**Digitální měny centrálních bank.** Výzkum wholesale CBDC Bank of England, program digitálního eura ECB a Project Agorá zkoumají architektury DLT odvozené od základních návrhů v Bitcoinu a Ethereu nebo s nimi kompatibilní. Struktury konsenzu a hashovacího řetězce zůstávají relevantní i tam, kde se model povolování a správy zcela liší od veřejných blockchainů.

Cesta od bílé knihy Bitcoinu z roku 2008 k tokenizovaným financím roku 2026 se rozprostírá přes dvě desetiletí, ale běží po ucelené technické linii. Pochopení toho, jak hashovací řetězec SHA-256 vynucuje neměnnost, jak Merkleův strom umožňuje efektivní ověřování a jak EVM atomicky vykonává chytré kontrakty, je předpokladem pro posouzení jakéhokoli tvrzení o tom, co blockchain v regulovaných finančních službách dokáže a co ne.

## Často kladené otázky

**Jaký je rozdíl mezi blockchainem a distribuovanou databází?**

Tradiční distribuovaná databáze replikuje data napříč uzly kvůli dostupnosti a výkonu, ale důvěra je centralizovaná; správce může záznamy měnit. Blockchain činí manipulaci výpočetně nákladnou prostřednictvím řetězení hashů a konsenzu: úprava jakéhokoli historického záznamu vyžaduje znovuprovedení veškerého následného proof-of-work nebo proof-of-stake a přesvědčení sítě, aby upravený fork přijala. Rozlišujícím rysem je průkaznost manipulace vynucená kryptografií a návrhem pobídek, nikoli řízením přístupu.

**Proč Ethereum používá Keccak-256 místo SHA-256?**

Ethereum přijalo Keccak-256 (finalistu SHA-3 před úpravami při standardizaci NIST) částečně proto, že jeho tvůrci chtěli nezávislost na linii SHA-2, na které již Bitcoin závisel. Keccak má také odlišné algebraické vlastnosti, které jej učinily atraktivním pro určité operace EVM. Praktickým dopadem pro vývojáře je, že odvození adres Etherea a hashování paměťových slotů používá Keccak-256, nikoli SHA-256d jako v Bitcoinu.

**Čemu „gas" v EVM brání?**

Gas brání dvěma kategoriím útoku. Zaprvé brání odepření služby prostřednictvím výpočetně nákladných operací: každý opcode stojí gas, takže útočník nemůže síť přinutit vykonávat nekonečné smyčky zdarma. Zadruhé limit gas na blok omezuje celkový výpočet na blok, čímž zajišťuje, že doba validace bloku zůstává omezená a předvídatelná pro plné uzly. Bez gasu by jediné volání kontraktu mohlo síť zastavit vykonáním neomezeného výpočtu.

**Jak proof-of-stake mění bezpečnostní model ve srovnání s proof-of-work?**

U proof-of-work zajišťuje bezpečnost vynaložení energie: útok na řetězec vyžaduje kontrolu nad více než 50 % hashovacího výkonu sítě, což znamená kontrolu nad více než 50 % jejího fyzického hardwaru a energie. U proof-of-stake (které Ethereum používá od Merge v roce 2022) zajišťuje bezpečnost ekonomický vklad: validátoři uzamykají ETH jako zástavu, která je zkrácena (slashing), pokud podepíší konfliktní bloky. Útok 51 % vyžaduje získání a vystavení riziku více než 50 % veškerého vsazeného ETH, což je kapitálový náklad, nikoli náklad na hardware a energii. Bezpečnostní model je odlišný, ale matematicky srovnatelný v ekonomických pojmech za předpokladu, že racionální validátoři preferují příjem z poplatků před zničením kapitálu.

## Reference

- Nakamoto, S., (2008). [Bitcoin: A Peer-to-Peer Electronic Cash System ⧉](https://bitcoin.org/bitcoin.pdf "Bitcoin Whitepaper").
- Buterin, V., (2014). [Ethereum: A Next-Generation Smart Contract and Decentralised Application Platform ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").
- Wood, G., (2014). [Ethereum: A Secure Decentralised Generalised Transaction Ledger ⧉](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper").
- NIST, (2015). [SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions ⧉](https://www.nist.gov/publications/sha-3-standard-permutation-based-hash-and-extendable-output-functions "NIST FIPS 202").
