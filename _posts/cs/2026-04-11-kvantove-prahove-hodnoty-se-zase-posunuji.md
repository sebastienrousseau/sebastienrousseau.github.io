---
title: "Kvantové prahové hodnoty se zase posunují"
subtitle: "Nový článek naznačuje, že Shorův algoritmus by mohl běžet na pouhých 10 000 qubitech. Důsledky pro kryptografii je těžké přehlédnout."
description: "Shorův algoritmus může nyní běžet na pouhých 10 000 qubitech. RSA, ECC i časový plán postkvantové migrace se posouvají dopředu. Zde je proč."
date: "April 11, 2026"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/leo_visions-Q_y8ZzhQ2_s-unsplash.webp"
banner_alt: "Diagram prahové hodnoty qubitů pro Shorův algoritmus. Deska plošných spojů kvantového počítače s modrými světelnými vzory"
keywords: "kvantové počítání, Shorův algoritmus, 10000 qubitů, postkvantová kryptografie, RSA-2048, kryptografie eliptických křivek, qubity z neutrálních atomů, kvantová korekce chyb, kryptografická agilita, časová osa kvantové hrozby"
---

## Kvantové prahové hodnoty se zase posunují

Nový článek naznačuje, že Shorův algoritmus by mohl běžet na pouhých 10 000 qubitech. Prahová hodnota pro kryptograficky relevantní kvantové počítání klesá rychleji, než většina předpokládala.

> **Klíčové poznatky**
>
> - Nový článek navrhuje, že Shorův algoritmus by mohl běžet na pouhých **10 000 fyzických qubitech**. Přibližně stokrát méně než dřívější konsenzuální odhady.
> - Toto snížení pohánějí tři sbíhající se pokroky: kvantové kódy pro korekci chyb s vysokou rychlostí, rekonfigurovatelná pole neutrálních atomů a zvýšený paralelismus.
> - Hrozba není rovnoměrná. **Kryptografie eliptických křivek (ECC)** je zranitelnější při nižších počtech qubitů; RSA-2048 vyžaduje při srovnatelných rozsazích výrazně delší doby běhu.
> - Jde o **teoretickou projekci**, nikoli o funkční demonstraci. Mezi současným hardwarem a provozem odolným vůči chybám v tomto rozsahu zůstává značná inženýrská mezera.
> - Postkvantové kryptografické standardy jsou již finalizovány. Prioritou je nyní **zrychlit migraci**. Ne čekat, až se kvantový systém objeví.

## Známý předpoklad, nyní pod tlakem

Během uplynulého desetiletí sledovaly diskuse o kvantovém počítání a kryptografii známý oblouk. Kvantové stroje byly uznávány jako teoreticky výkonné, avšak považovány za nepraktické ve velkém rozsahu. Prolomení moderních kryptografických systémů by vyžadovalo miliony fyzických qubitů a časový plán zůstával pohodlně vzdálený. Tento předpoklad je nyní pod vážným tlakem.

Nedávný článek, [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/pdf/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (PDF)"), navrhuje něco závažnějšího než jediný průlom. Naznačuje, že prahová hodnota pro kryptograficky relevantní kvantové výpočty může být o řád nižší, než se dříve věřilo. Ne miliony qubitů, ale desítky tisíc. Tento rozdíl je podstatný a směr, který naznačuje, je těžké přehlédnout.

## Souběh, který pohání tento posun: korekce chyb, architektura a paralelismus

Tento výsledek nevychází z jediného objevu. Odráží souběh zlepšení napříč několika vrstvami zásobníku kvantového počítání, která společně posouvají hranici toho, co se jeví jako proveditelné.

První zlepšení se týká korekce chyb. Tradiční přístupy vyžadovaly velkou režii, často stovky fyzických qubitů k reprezentaci jediného logického qubitu. Článek se místo toho opírá o kvantové kódy pro korekci chyb s vysokou rychlostí, které tuto režii výrazně snižují. ([Emergent Mind ⧉](https://www.emergentmind.com/papers/2603.28627 "Shor's Algorithm with 10000 Atomic Qubits")) Druhé se týká architektury. Systém je postaven na rekonfigurovatelných polích neutrálních atomů, která lze během výpočtu přeuspořádat, což umožňuje pružnější propojení a efektivnější provádění. ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")) Třetím je paralelismus: zvýšení počtu qubitů umožňuje souběžně provádět více operací, což zkracuje celkovou dobu provádění.

Žádná z těchto myšlenek není sama o sobě nová. V kombinaci však mění to, co bylo dříve považováno za pevnou hranici.

## Od milionů k desítkám tisíc: co čísla ve skutečnosti znamenají

Po léta vyžadoval konsenzuální odhad pro spuštění Shorova algoritmu v kryptografických rozsazích miliony fyzických qubitů. Nová analýza naznačuje, že za určitých předpokladů by toto číslo mohlo klesnout přibližně na 10 000. ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")) Toto číslo však není úplným obrazem.

Na spodním konci tohoto rozsahu zůstávají doby běhu dlouhé. Faktorizace RSA-2048 při minimálních počtech qubitů by stále mohla trvat roky nepřetržitého provozu. Rychlejší provádění vyžaduje více qubitů, potenciálně v řádu desítek tisíc. Vztah mezi počtem qubitů a dobou běhu není lineární a článek dbá na to, aby to prezentoval jako spektrum, nikoli jako pevnou prahovou hodnotu. Co se mění, je směr: bariéra již není čistě teoretická. Nyní je to otázka inženýrství.

### Staré předpoklady vs. nové skutečnosti

| Dimenze | Starý předpoklad | Nová skutečnost |
|---|---|---|
| Požadované fyzické qubity (Shorův algoritmus) | ~1 000 000+ | ~10 000–26 000 |
| Doba k prolomení RSA-2048 (při minimu qubitů) | V tomto desetiletí neproveditelné | Roky (při 10 tis. qubitech); rychleji s více |
| Doba k prolomení ECC-256 | V tomto desetiletí neproveditelné | Dny (odhad při ~26 tis. qubitech) |
| Dominantní hardwarové paradigma | Supravodivé qubity | Rekonfigurovatelná pole neutrálních atomů |
| Režie korekce chyb | Stovky fyzických qubitů na logický qubit | Výrazně snížena pomocí kódů s vysokou rychlostí |
| Povaha bariéry | Teoretická | Inženýrská |
| Naléhavost migrace | Dlouhodobé plánování | Nyní vyžadováno aktivní nasazení |

*Zdroj: Analýza založená na [arXiv:2603.28627 ⧉](https://arxiv.org/abs/2603.28627) a předchozí literatuře.*

## Čas, rozsah a nerovnoměrná zranitelnost kryptografických systémů

Jedním z významnějších přínosů článku je odstín, který vnáší do otázky času. Kvantová výhoda nepřichází naráz. Existuje podél spektra určeného rozsahem systému a povahou kryptografického cíle.

Přibližně s 26 000 qubity autoři odhadují, že prolomení kryptografie eliptických křivek by za příznivých podmínek mohlo trvat dny. ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")) Pro RSA-2048 jsou časové plány podstatně delší. Tato asymetrie je důležitá. Naznačuje, že různé kryptografické systémy se mohou stát zranitelnými v různých okamžicích, nikoli současně, a že přechod k postkvantovým standardům pravděpodobně nebude jedinou událostí s jediným termínem.

Tento vzorec je v souladu s širším zpravodajstvím. Analýzy z posledních měsíců naznačují, že kvantové systémy schopné ohrozit široce používané šifrování by se mohly objevit před koncem desetiletí. ([Nature ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption")) Vlády a normalizační orgány již plánují přechody na postkvantovou kryptografii, s harmonogramy implementace sahajícími do 30. let. ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")) Diskuse se posunula od „zda“ k „kdy“.

## Inženýrská mezera, která přetrvává

Je důležité být přesný v tom, co tento článek představuje. Je to projekce, nikoli demonstrace. Navrhované systémy závisí na předpokladech o chybovosti, stabilitě hardwaru a chování při škálování, které dosud nebyly ověřeny v požadovaném rozsahu. Současné experimenty pracují na úrovni stovek až nižších tisíců qubitů, nikoli desítek tisíc pracujících odolně vůči chybám po delší dobu. ([Phys.org ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits"))

Zůstává značná inženýrská mezera. Cesta od přesvědčivého teoretického modelu k funkčnímu systému schopnému trvalého provozu odolného vůči chybám v tomto rozsahu zahrnuje výzvy, které dosud nejsou plně pochopeny, natož vyřešeny. Co se změnilo, není blízkost funkčního stroje, ale věrohodnost cíle. Mezera se zužuje a směr pokroku je konzistentní.

## Proč zkracující se časový plán vyžaduje pozornost už teď

Význam této práce nespočívá v tom, že kryptografie bude prolomena v blízké době. Je v tom, že se časový plán zkracuje způsoby, které ovlivňují rozhodnutí přijímaná dnes. Bezpečnostní systémy jsou navrhovány s ohledem na dlouhé životní cykly. Data zašifrovaná dnes mohou potřebovat zůstat důvěrná po desetiletí. Rozhodnutí o infrastruktuře přijatá letos bude obtížné zvrátit v horizontu pěti let. Pokud kvantové schopnosti přijdou dříve, než se očekává, stanou se tyto předpoklady křehkými.

Proto je postkvantová kryptografie již nasazována napříč kritickými sektory. Ne proto, že by hrozba byla bezprostřední, ale protože přechod vyžaduje čas a náklady na pozdní reakci jsou asymetrické. V historii výpočetní techniky se opakuje jeden vzorec: pokrok se zdá pomalý, dokud náhle není. To, co začíná jako teoretické zlepšení, se stává praktickým omezením, a to, co bylo kdysi odmítáno jako vzdálené, se stává něčím, s čím je třeba počítat. Kvantové počítání může sledovat přesně tuto trajektorii, ne prostřednictvím jediného dramatického průlomu, ale prostřednictvím stálého snižování nákladů, složitosti a rozsahu.

## Co to znamená podle odvětví: praktický průvodce

Důsledky tohoto výzkumu nejsou napříč odvětvími rovnoměrné. Vhodná reakce závisí na typu ohrožených kryptografických aktiv, na citlivosti a životnosti dotčených dat a na tempu, jakým se posouvají regulační očekávání.

### Finanční služby a FinTech

Finanční instituce čelí složenému riziku: uchovávají dlouhověká citlivá data, provozují infrastrukturu s pomalými cykly obměny a podléhají rostoucímu regulačnímu dohledu nad kryptografickou odolností. ECC se široce používá v připojeních TLS, mobilní autentizaci a digitálních podpisech napříč platebními kolejemi. Kryptografická kategorie, kterou článek označuje jako nejzranitelnější při nižších počtech qubitů. Instituce, které dosud nezahájily kryptografickou inventarizaci ani nezačaly plán postkvantové migrace, by měly tento článek brát jako podnět ke zrychlení, nikoli jako důvod k panice. [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) a CRYSTALS-Dilithium, oba nyní standardizované institucí NIST, jsou vhodnými cíli migrace pro zapouzdření klíčů, respektive pro digitální podpisy.

### Veřejná správa a obrana

Státní aktéři mají nejsilnější motivaci. A v mnoha případech i zdroje. K urychlení vývoje kvantového hardwaru nad rámec toho, co je veřejně známo. Vlády uchovávající citlivou komunikaci, zpravodajská data nebo klíče ke kritické infrastruktuře musí předpokládat, že protivníci již sklízejí zašifrovaná data pro budoucí dešifrování, což je strategie běžně známá jako „harvest now, decrypt later“. Pro organizace veřejného sektoru je dodržování národních mandátů kvantové připravenosti stále nevyhnutelnější a okno pro proaktivní migraci se zužuje.

### Zdravotnictví a kritická infrastruktura

Zdravotní záznamy, řídicí systémy inženýrských sítí a průmyslové sítě sdílejí společnou zranitelnost: data a systémy s velmi dlouhou provozní životností, chráněné kryptografickými standardy, které byly navrženy pro předkvantový model hrozeb. Zdravotní záznam zašifrovaný dnes může potřebovat zůstat soukromý po padesát let. Řídicí systém certifikovaný letos může zůstat v provozu dvě desetiletí. Pro tato odvětví není zkracující se časový plán abstraktní starostí. Je to přímá výzva základním předpokladům, na nichž stojí současné bezpečnostní architektury.

## Závěr

Nejdůležitějším aspektem tohoto článku není konkrétní počet qubitů, který uvádí. Je to směr, který tento počet naznačuje. Otázkou již není, zda kvantové počítače mohou ohrozit moderní kryptografii. Je to, jak rychle lze potřebné systémy vybudovat a zda se organizace závislé na současných standardech pohybují v reakci dostatečně rychle.

Prozatím zůstávají odpovědi nejisté. Ale prostor pro odkládání této otázky se zužuje a náklady na čekání rostou s každým věrohodným snížením teoretické prahové hodnoty. Kryptografická komunita, bezpečnostní plánovači a odvětví, která se na ně spoléhají, by udělali dobře, kdyby tento článek nebrali jako důvod k poplachu, ale jako vážný podnět ke zrychlení přechodů, které již probíhají.

## Často kladené otázky

**Mohou 10 000 qubitů opravdu prolomit šifrování RSA?**

Teoreticky ano. Ale s důležitými výhradami. Zatímco dřívější odhady naznačovaly, že je zapotřebí miliony fyzických qubitů, nový výzkum kódů pro korekci chyb s vysokou rychlostí a rekonfigurovatelných polí neutrálních atomů naznačuje, že prahová hodnota je výrazně nižší. Nicméně při 10 000 qubitech zůstává odhadovaná doba běhu pro faktorizaci RSA-2048 extrémně dlouhá. Potenciálně roky nepřetržitého provozu. Rychlejší útoky vyžadují více qubitů, pravděpodobně v řádu desítek tisíc. Článek představuje projekci založenou na modelovaných předpokladech, nikoli demonstraci na funkčním systému.

**Které šifrování je nejvíce ohroženo kvantovým počítáním?**

Kryptografie eliptických křivek (ECC) je obecně zranitelnější při nižších počtech qubitů než RSA-2048. Článek odhaduje, že prolomení ECC by mohlo za příznivých podmínek trvat dny při použití přibližně 26 000 rekonfigurovatelných qubitů. RSA-2048 vyžaduje při srovnatelných počtech qubitů výrazně delší dobu běhu. Tato asymetrie znamená, že systémy závislé na ECC. Běžné v TLS, mobilní autentizaci a blockchainu. Mohou čelit riziku v kratším časovém horizontu než infrastruktura založená na RSA.

**Co je rekonfigurovatelný qubit z neutrálního atomu?**

Qubity z neutrálních atomů jsou jednotlivé atomy. Obvykle rubidium nebo cesium. Zachycené a manipulované pomocí laserového světla ve vakuové komoře. „Rekonfigurovatelný“ znamená, že uspořádání atomů lze během výpočtu dynamicky měnit, což umožňuje efektivnější provádění složitých kvantových obvodů. Tato pružnost snižuje počet fyzických qubitů potřebných k implementaci logických operací odolných vůči chybám a je klíčovým důvodem, proč nový článek dosahuje nižších odhadů qubitů než dřívější práce založené na architekturách supravodivých qubitů.

**Co je postkvantová kryptografie a proč se nasazuje už teď?**

Postkvantová kryptografie (PQC) označuje kryptografické algoritmy, o nichž se věří, že jsou bezpečné vůči klasickým i kvantovým počítačům. NIST finalizoval svou první sadu standardů PQC v roce 2024, včetně [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) pro zapouzdření klíčů a CRYSTALS-Dilithium pro digitální podpisy. Nasazení začíná nyní. Dlouho předtím, než kvantové počítače představují bezprostřední hrozbu. Protože kryptografické přechody jsou pomalé. Nahrazení zabudovaných standardů napříč globální infrastrukturou obvykle trvá desetiletí nebo více a data zašifrovaná dnes mohou potřebovat zůstat důvěrná dlouho poté, co kvantové schopnosti dozrají.

**Kolik qubitů má dnes nejvýkonnější kvantový počítač?**

Na začátku roku 2026 pracují přední kvantové systémy v řádu stovek až nižších tisíců fyzických qubitů. Zásadní je, že většina z nich dosud není odolná vůči chybám. Pracují pod prahovými hodnotami korekce chyb požadovanými pro trvalé, spolehlivé logické výpočty. Mezera mezi dnešním hardwarem a desítkami tisíc vysoce věrných logických qubitů odolných vůči chybám popsanými v novém článku zůstává značná, ačkoli tempo pokroku napříč platformami supravodivých qubitů, neutrálních atomů a zachycených iontů se zrychluje.

## Odkazy

- Sebastien Rousseau, (2025). [Quantum-Safe Payments: Why the Payments Industry Must Act Now](https://sebastienrousseau.com/2025-09-01-quantum-safe-payments-epaa/index.html "Quantum-Safe Payments: Why the Payments Industry Must Act Now").
- Sebastien Rousseau, (2023). [Quantum Key Distribution: Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Anonymous, (2026). [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits"). arXiv preprint arXiv:2603.28627.
- Castelvecchi, D. (2026). [Quantum-computing breakthroughs pose risks to encryption ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption"). Nature.
- Phys.org, (2026). [Useful quantum computers could be built with as few as 10,000 qubits ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits"). Phys.org.
