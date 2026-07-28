---
title: "Plně homomorfní šifrování (FHE) v bankovní kvantové éře"
subtitle: "Posílení zabezpečení dat, zvýšení soukromí AI a budování důvěry zákazníků v éře kvantových výpočtů s FHE"
description: "Jak plně homomorfní šifrování zásadně mění zabezpečení dat v bankovnictví a finančním sektoru a zajišťuje soukromí vůči hrozbám kvantových výpočtů."
date: "March 25, 2024"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/fully-homomorphic-encryption.webp"
banner_alt: "Banner pro plně homomorfní šifrování"
keywords: "plně homomorfní šifrování, zabezpečení bankovnictví, kvantové výpočty, šifrování finančních dat, případové studie FHE, regulační rámce FHE, výpočetní režie FHE, výzkum FHE, hardware FHE, zákony o ochraně dat"
---


**Plně homomorfní šifrování (FHE, Fully Homomorphic Encryption)** slibuje nově vymezit zabezpečení dat v bankovnictví a finančním sektoru. Tím, že umožňuje provádět výpočty nad šifrovanými daty, chrání FHE soukromí před konvenčními i kvantovými výpočetními hrozbami.

## Úvod

Nasazení FHE ve finančním sektoru není jen teoretické; stává se praktickou realitou a proměňuje standardy zabezpečení a soukromí dat. Tento článek zkoumá praktická využití, regulatorní otázky, možné nevýhody a pokroky ve výzkumu plně homomorfního šifrování (FHE) ve financích i v aplikacích umělé inteligence (AI).

## Porozumění plně homomorfnímu šifrování

### Základy šifrování

Šifrování je metoda převodu čitelných dat (otevřený text) do nečitelného formátu (šifrový text) pomocí algoritmu a šifrovacího klíče. Hlavním cílem je zajistit, aby k původním datům měly přístup pouze oprávněné strany, a to dešifrováním šifrového textu pomocí dešifrovacího klíče.

### Tradiční metody šifrování

Tradiční metody šifrování lze zhruba rozdělit do dvou typů: symetrické a asymetrické šifrování. Symetrické šifrování používá jediný klíč pro šifrování i dešifrování. Tato efektivita jde na úkor bezpečnosti, zejména když distribuce klíčů představuje problém. Asymetrické šifrování, označované také jako kryptografie s veřejným klíčem, používá dva klíče: jeden pro šifrování a druhý pro dešifrování. Tato metoda je bezpečnější, ale pomalejší než symetrické šifrování.

### Omezení konvenčního šifrování pro výpočty

I když tradiční metody šifrování účinně zabezpečují data v klidu nebo při přenosu, selhávají, pokud jde o provádění výpočtů nad šifrovanými daty. Aby bylo možné šifrovaná data zpracovat nebo analyzovat, je obvykle nutné je nejprve dešifrovat, provést potřebné operace a poté je znovu zašifrovat. Tento krok dešifrování představuje významné riziko pro soukromí dat, zejména v nedůvěryhodných nebo cloudových výpočetních prostředích.

![divider][divider].class=\"m-10 w-100\"

## Průlom homomorfního šifrování

**Homomorfní šifrování (HE)** řeší omezení konvenčního šifrování. Umožňuje provádět určité výpočty přímo nad šifrovanými daty (šifrovými texty). Dešifrovaný výsledek je stejný jako původní data (otevřený text) po provedení stejných operací. HE existuje ve třech hlavních variantách: částečně homomorfní šifrování (PHE), do jisté míry homomorfní šifrování (SHE) a plně homomorfní šifrování (FHE).

- **Partially Homomorphic Encryption (PHE):** Podporuje neomezený počet operací jediného typu (např. buď sčítání, nebo násobení) nad šifrovými texty.
- **Somewhat Homomorphic Encryption (SHE):** Podporuje omezený počet operací kombinujících sčítání i násobení, ale pouze do určité hloubky.
- **Fully Homomorphic Encryption (FHE):** Nejpokročilejší forma, umožňující neomezený počet operací sčítání i násobení nad šifrovými texty.

### Technická důmyslnost FHE

FHE je založeno na složitých matematických strukturách, jako je kryptografie na mřížkách. Kryptografie na mřížkách je typ šifrování, který využívá matematické struktury zvané mřížky.

Mřížka je pravidelné uspořádání bodů v prostoru a kryptografie na mřížkách se opírá o obtížnost řešení určitých matematických problémů spojených s těmito strukturami. Díky tomu je kryptografie na mřížkách bezpečná a odolná vůči útokům, včetně útoků z kvantových počítačů.

V roce 2009 Craig Gentry vyvinul metodu, popsanou v jeho článku [**A Fully Homomorphic Encryption Scheme ⧉**][00], pro vytvoření systému, který dokáže provádět homomorfní vyhodnocení svého vlastního dešifrovacího obvodu. Tento sebereferenční návrh umožňuje schématům FHE provádět libovolné výpočty nad šifrovanými daty.

### Průběh algoritmu FHE

![Operační tok FHE][fhe].class=\"m-10 w-100\"

Výše uvedený diagram znázorňuje operační tok algoritmu plně homomorfního šifrování (FHE).

- Proces šifrování začíná daty v otevřeném textu, která jsou zašifrována pomocí šifrovacího klíče, aby vznikl šifrový text.

- Tato šifrovaná data pak mohou být podrobena různým výpočtům přímo nad šifrovým textem prostřednictvím procesu známého jako bootstrapping.

- Tato jedinečná schopnost FHE umožňuje, aby data zůstala šifrovaná po celou dobu procesu. Jakmile jsou provedeny potřebné operace, proces dešifrování může upravený šifrový text převést zpět na otevřený text pomocí schématu FHE.

Hlavní výhoda FHE spočívá v jeho schopnosti provádět výpočty nad šifrovým textem bez nutnosti dešifrování, čímž je po celou dobu výpočtu zachováno soukromí a bezpečnost dat.

### Kvantová odolnost FHE

Tradiční metody šifrování jsou často zranitelné vůči kvantovým algoritmům. Tyto algoritmy dokážou rychle řešit problémy, jako je faktorizace celých čísel a diskrétní logaritmy, které tvoří základ těchto metod šifrování. Naproti tomu plně homomorfní šifrování (FHE) využívá problémy na mřížkách, u nichž se předpokládá, že jsou pro kvantové počítače obtížně řešitelné. Tato kvantová odolnost činí z FHE slibnou metodu šifrování pro postkvantovou éru.

FHE založené na mřížkách je odolné vůči kvantovým útokům, protože základní matematické problémy, jako je problém nejkratšího vektoru (Shortest Vector Problem, SVP) a problém nejbližšího vektoru (Closest Vector Problem, CVP), jsou považovány za obtížně řešitelné i pro kvantové počítače. Zatímco kvantové algoritmy jako Shorův algoritmus dokážou prolomit tradiční metody šifrování, které se opírají o faktorizaci velkých čísel nebo výpočet diskrétních logaritmů, není známo, že by poskytovaly významnou výhodu při řešení problémů na mřížkách. Tato vlastnost činí z FHE založeného na mřížkách slibného kandidáta pro postkvantovou kryptografii.

![divider][divider].class=\"m-10 w-100\"

## Dopad FHE na bankovnictví a finance

### Posílené soukromí a zabezpečení dat

Uplatnění FHE ve finančním sektoru slibuje významné posílení soukromí dat. Banky nyní mohou provádět hodnocení rizik, detekci podvodů a komplexní datovou analytiku a přitom zajistit absolutní důvěrnost informací o zákaznících. Tento technologický pokrok zmírňuje riziko úniku dat a posiluje integritu digitálních bankovních platforem a finančních transakcí.

### Cloud computing a outsourcing

Jednou z hlavních oblastí použití homomorfního šifrování je bezpečné zpracování dat v cloudu. Banky mohou využívat služby cloud computingu ke zpracování šifrovaných dat, aniž by ohrozily jejich soukromí. To finančním institucím umožňuje využít škálovatelnost a nákladovou efektivitu cloud computingu při zachování důvěrnosti citlivých finančních informací.

Přechod bank ke cloud computingu a outsourcingu výpočetních úloh podtrhuje význam FHE. Díky bezpečnému cloud computingu mohou finanční instituce čerpat z externích zdrojů a přitom chránit citlivá šifrovaná data pomocí plně homomorfního šifrování (FHE). FHE umožňuje bankám bezpečně využívat služby cloud computingu a zároveň zajišťuje, že citlivá šifrovaná data zůstanou vždy chráněna.

![divider][divider].class=\"m-10 w-100\"

## Příprava na kvantovou budoucnost

Bezprostřední příchod kvantových výpočtů ohlašuje potenciální krizi pro tradiční metodiky šifrování. FHE založené na mřížkách je ze své podstaty odolné vůči kvantovým útokům a nabízí robustní obranu proti hrozbě, kterou kvantové výpočty představují pro zabezpečení dat.

### Kvantově odolné šifrování

FHE poskytuje mimořádnou vrstvu ochrany proti hrozbám kvantových výpočtů. Použitím kryptografických technik na mřížkách FHE zajišťuje, že finanční data a aktiva zůstanou v bezpečí i tváří v tvář kvantovým protivníkům.

Kvantová odolnost FHE vyplývá ze složitých základních matematických problémů, jako je problém nejkratšího vektoru (Shortest Vector Problem, SVP) a problém nejbližšího vektoru (Closest Vector Problem, CVP). Předpokládá se, že tyto problémy jsou neřešitelné i pro kvantové počítače, což činí z FHE založeného na mřížkách ideálního kandidáta pro postkvantovou kryptografii.

Používání kvantově odolného šifrování, jako je FHE, je zásadní nejen pro ochranu finančních aktiv, ale také pro udržení důvěry zákazníků v digitální éře. S postupem kvantových výpočtů budou finanční instituce, které upřednostní robustní šifrování, lépe připraveny zvládat budoucí výzvy a příležitosti.

![divider][divider].class=\"m-10 w-100\"

## Budoucnost FHE v bankovnictví a financích

Vývoj FHE ve finančním sektoru je slibný, stále však čelí výzvám. Bankovní sektor může plný potenciál FHE využít zdokonalováním technologie, jejím začleněním do každodenních finančních operací a spoluprací s regulátory.

FHE lze použít v různých bankovních a finančních aplikacích, jako jsou:

- **Bezpečná analýza finančních dat**: FHE umožňuje bankám analyzovat šifrovaná finanční data, jako jsou transakce, úvěrová skóre a investiční portfolia, bez ohrožení soukromí zákazníků, a zajišťuje tak bezpečné zpracování citlivých informací.

- **Strojové učení zachovávající soukromí**: FHE umožňuje bankám trénovat a nasazovat modely strojového učení nad šifrovanými daty, což jim umožňuje využívat AI k detekci podvodů, hodnocení rizik a segmentaci zákazníků při zachování důvěrnosti dat.

- **Bezpečný vícestranný výpočet**: FHE umožňuje bezpečnou spolupráci mezi více finančními institucemi, které mohou provádět společné výpočty nad šifrovanými daty bez sdílení citlivých informací, což usnadňuje bezpečné mezibankovní transakce a dodržování předpisů.

- **Zabezpečení API**: FHE dokáže zabezpečit API šifrováním citlivých dat před přenosem a zajišťuje, že informace o zákaznících zůstanou důvěrné během výměny dat mezi bankami a službami třetích stran.

- **Bezpečný cloud computing**: FHE umožňuje bankám bezpečně přenést výpočty a ukládání dat na cloudové platformy bez ohrožení soukromí dat, protože data zůstávají po celý proces šifrovaná, což rozšiřuje využití nákladově efektivních a škálovatelných cloudových služeb.

- **Dodržování předpisů zachovávající soukromí**: FHE umožňuje bankám bezpečně sdílet šifrovaná data s regulačními orgány, což umožňuje dodržování požadavků na výkaznictví bez vystavení citlivých informací o zákaznících, čímž se zjednodušuje proces dodržování předpisů při zachování soukromí.

Tyto aplikace ukazují transformační sílu FHE v bankovnictví a finančním sektoru a podtrhují jeho potenciál zásadně změnit standardy zabezpečení a soukromí dat.

![divider][divider].class=\"m-10 w-100\"

## Překonání výzev při zavádění FHE

### Výkonnostní výzvy a optimalizace

Řešení výpočetní režie, která je FHE vlastní, zůstává klíčovou výzvou. Nedávný pokrok v optimalizaci algoritmů a vývoji specializovaných hardwarových akcelerátorů zmenšuje výkonnostní rozdíl mezi tradičními výpočty a plně homomorfním šifrováním (FHE).

### Standardizace a spolupráce

Cesta k širokému rozšíření FHE závisí na standardizaci protokolů a posílené spolupráci mezi zainteresovanými stranami finančního ekosystému. Jednotný přístup k přijetí FHE může výrazně urychlit jeho integraci do běžných finančních služeb.

### Regulace a dodržování předpisů

Regulační orgány hrají v přijetí FHE zásadní roli, přičemž vyvíjející se zákony o ochraně soukromí dat nařizují jeho použití. Regulační tlak by mohl posloužit jako katalyzátor komplexního přijetí FHE napříč bankovnictvím a finančním sektorem a zároveň zajistit soulad s předpisy na ochranu dat.

Regulační rámec týkající se soukromí a zabezpečení dat hraje významnou roli v přijetí FHE v bankovním sektoru. Přísné předpisy, jako je obecné nařízení o ochraně osobních údajů (General Data Protection Regulation, GDPR) a kalifornský zákon o ochraně soukromí spotřebitelů (California Consumer Privacy Act, CCPA), nařizují robustní opatření na ochranu dat a zdůrazňují právo jednotlivce na soukromí. FHE se svou schopností zpracovávat šifrovaná data bez dešifrování dobře odpovídá orientaci těchto předpisů na soukromí. Jak se zákony o ochraně soukromí dat stávají stále přísnějšími, nabízí FHE přesvědčivé řešení, které bankám umožňuje provádět potřebné výpočty a analýzy při dodržení požadavků na soulad.

![divider][divider].class=\"m-10 w-100\"

## Zabezpečení velkých jazykových modelů pomocí plně homomorfního šifrování (FHE)

Velké jazykové modely (LLM) jsou výkonné nástroje AI. Jejich používání však vyvolává obavy o soukromí, zejména při práci s citlivými uživatelskými daty. Plně homomorfní šifrování (FHE) poskytuje řešení, které chrání soukromí uživatelů a zachovává duševní vlastnictví vlastníků modelů tím, že umožňuje výpočty nad šifrovanými daty.

### Výzvy soukromí u LLM

Nasazení lokálního (on-premise) LLM za účelem zachování soukromí dat přináší výzvy, jako jsou vysoké náklady a možné vystavení cenného duševního vlastnictví. FHE tyto výzvy řeší tím, že umožňuje LLM pracovat nad šifrovanými uživatelskými daty a zajišťuje současně soukromí i bezpečnost modelu.

### Přístup Zama k šifrovaným LLM

[**Zama ⧉**][01], společnost zaměřená na technologie ochrany soukromí, prokázala proveditelnost vytvoření šifrovaného LLM pomocí FHE. Její přístup, který kombinuje FHE s dalšími technologiemi posilujícími soukromí, dosahuje výkonu srovnatelného s nešifrovanými modely pouze s mírným nárůstem výpočetní režie.

### Zlepšení soukromí uživatelů pomocí šifrovaných LLM

Integrace FHE do LLM má potenciál proměnit soukromí uživatelů, zejména v aplikacích pracujících s citlivými osobními nebo obchodními informacemi. Jak se AI stále více zaměřuje na soukromí, je důležité, aby vývojáři, uživatelé a regulátoři spolupracovali. Tato spolupráce je klíčová pro vybudování ekosystému AI, který klade bezpečnost a soukromí na první místo.

![divider][divider].class=\"m-10 w-100\"

## Závěr

**Plně homomorfní šifrování (FHE)** je průlomová technologie zabezpečení dat, která nabízí výjimečné soukromí a zabezpečení pro bankovnictví a finanční sektor.

Jak kvantové výpočty postupují, stává se FHE ještě zásadnějším. Jeho přijetí přetvoří kybernetickou bezpečnost ve finančních službách a učiní digitální bankovnictví důvěryhodnějším a bezpečnějším v našem stále propojenějším světě.

Příchod FHE také otevřel nové možnosti bezpečného a soukromého využití velkých jazykových modelů. Umožněním šifrovaných LLM FHE zajišťuje, že uživatelská data zůstanou důvěrná a zároveň těží z pokročilých schopností těchto modelů.

Éra kvantových výpočtů se blíží. Banky musí proaktivně vyhodnotit svou šifrovací infrastrukturu, identifikovat potenciální zranitelnosti a vypracovat jasný plán přijetí FHE, aby ochránily data a udržely důvěru zákazníků.

[00]: https://crypto.stanford.edu/craig/ "Původní článek Craiga Gentryho o plně homomorfním šifrování"
[01]: https://zama.ai/ "Zama - Plně homomorfní šifrování"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Oddělovač"
[fhe]: https://cloudcdn.pro/stocks/diagrams/fhe_algorithm_diagram.webp "Architektura FHE"
