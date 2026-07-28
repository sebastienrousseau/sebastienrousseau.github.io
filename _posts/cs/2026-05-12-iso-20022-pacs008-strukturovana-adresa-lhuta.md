---
title: "Listopadová lhůta 2026 pro strukturovanou adresu v pacs.008: pohled na zbývajících šest měsíců"
subtitle: "Od poloviny listopadu 2026 bude SWIFT CBPR+ odmítat nestrukturované poštovní adresy v pacs.008 a souvisejících přeshraničních platebních zprávách. Přibližně 65 % zpráv stále nevyhovuje a okno pro nápravu se rychle uzavírá."
description: "Od listopadu 2026 vyžaduje SWIFT CBPR+ strukturované poštovní adresy v přeshraničních platebních zprávách. Samostatné nestrukturované řádky adresy (AdrLine) již nebudou u klíčových polí stran v pacs.008 přijímány. Minimálně se vyžadují TwnNm a Ctry, doporučují se StrtNm a BldgNb nebo PstBx. Šest měsíců před lhůtou stále 65 % platebních zpráv obsahuje nestrukturované adresy a 44 % bank zaostává za harmonogramem."
date: "May 12, 2026"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "Diagram strukturované adresy ISO 20022 pacs.008: pole přeshraniční platební zprávy se zvýrazněnými TwnNm a Ctry"
keywords: "ISO 20022, pacs.008, SWIFT CBPR+, strukturovaná adresa, listopad 2026, poštovní adresa, TwnNm, Ctry, StrtNm, BldgNb"
---

Od poloviny listopadu 2026 bude SWIFT CBPR+ odmítat nestrukturované poštovní adresy v pacs.008 a souvisejících přeshraničních platebních zprávách. Přibližně 65 % zpráv stále nevyhovuje a 44 % bank zaostává za harmonogramem, takže se okno pro nápravu uzavírá rychleji, než na co je většina programů připravenosti navržena.

---

> **Klíčové body**
>
> - Od **listopadu 2026** nebude SWIFT CBPR+ nadále přijímat nestrukturované poštovní adresy v přeshraničních platebních zprávách. Změna se týká **pacs.008** (úhrada klienta), **pacs.009** (mezibankovní úhrada), **pacs.004** (vratky) a **pacs.003** (inkasa), stejně jako navazujících toků **pain.001**, které je napájejí.
> - Minimálně musí být v samostatných strukturovaných polích uvedeny **název města (TwnNm)** a **země (Ctry)**. Důrazně se doporučují **název ulice (StrtNm)** a buď **číslo budovy (BldgNb)**, nebo **poštovní přihrádka (PstBx)**. Samotné řádky adresy ve volném textu (AdrLine) už u klíčových polí stran požadavek nesplní.
> - Změna zvyšuje přesnost prověřování sankcí, snižuje míru ručních oprav a chrání přímé zpracování (straight-through processing), ale jen u institucí, které napravily svá vstupní klientská data, nikoli pouze své zpracovatele zpráv.
> - Připravenost odvětví je nerovnoměrná. K březnu 2026 stále přibližně **65 % zpráv CBPR+ nese nestrukturované adresy**, **44 % bank** není na dobré cestě k dodržení lhůty a průměrně **32 % záznamů klientských adres** zůstává nestrukturovaných.
> - Nástroje s otevřeným zdrojovým kódem, včetně **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, knihovny v jazyce Python a služby FastAPI pro generování, validaci a orchestraci toků zpráv pacs.008, dokážou zkrátit časové plány nápravy automatizací validace schémat, kontrol kvality adres a vynucování na úrovni CI dříve, než zprávy dorazí do sítě SWIFT.

---

## Lhůta, se kterou se vždy počítalo

Požadavek na strukturovanou adresu z listopadu 2026 není náhlým regulatorním krokem. Je na plánu SWIFT CBPR+ od okamžiku, kdy byla oznámena původní migrace [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html), a navazuje na konec souběhu MT/MX v listopadu 2025. Co se v roce 2026 změnilo, je blízkost. Se zhruba šesti zbývajícími měsíci odvětví nyní funguje uvnitř okna, v němž se nevyřešené problémy s kvalitou dat mění v provozní riziko.

Čísla vyprávějí ten příběh jasně. Vlastní komunitní aktualizace SWIFT z března 2026 uvádí, že [přibližně 65 % platebních zpráv stále obsahuje nestrukturované adresy ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed") a že přijetí zůstává nerovnoměrné napříč regiony a typy institucí. [Průzkum RedCompass Labs mezi 308 vedoucími odborníky na platby ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022") z března 2026 zjistil, že 44 % bank v současnosti není na dobré cestě ke splnění lhůty pro strukturovanou adresu, přestože na připravenost pro rok 2026 vynaložily v průměru 20 milionů dolarů (a v největších institucích přes 30 milionů dolarů) a k programům [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) přiřadily v průměru 13 dalších pracovníků. Tentýž průzkum zjistil, že průměrně 32 % záznamů klientských adres zůstává nestrukturovaných a že 60 % bank hlásí mezery v jádrových bankovních systémech při podpoře strukturovaných polí adres.

Jinými slovy nejde o problém, který lze vyřešit dalším měsícem práce na zpracovateli zpráv. Je to problém kvality dat, který sahá od vrstvy zpráv proti proudu do onboardingových systémů, procesů KYC, firemních kanálů a desetiletí nashromážděných klientských kmenových dat ve volném textu.

## Co pravidlo skutečně vyžaduje

Podle SWIFT CBPR+ Standards Release 2026 (SR2026) je klíčový požadavek v principu přímočarý a v detailu neúprosný. Od poloviny listopadu 2026 musí být [název města a země uvedeny ve svých určených strukturovaných polích ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed") u všech agentů a stran v platebních zprávách CBPR+, s velmi omezenými výjimkami (výpisy a oznámení v camt.052, camt.053, camt.054 a několik administrativních zpráv zůstávají mimo striktní požadavek). U agentů zůstává další používání samotného BIC platnou alternativou k názvu a adrese.

Po přechodu jsou povoleny dva formáty adresy:

- **Plně strukturovaný:** každá složka poštovní adresy je namapována na svůj vyhrazený prvek [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html): StrtNm (název ulice), BldgNb (číslo budovy) nebo BldgNm (název budovy), PstCd (PSČ), TwnNm (název města), CtrySubDvsn (nižší územní celek), Ctry (země jako kód ISO 3166-1 alpha-2). Je to formát, který SWIFT výslovně označuje za žádoucnější variantu tam, kde je to možné.
- **Hybridní:** název města a země se vyplní ve svých strukturovaných polích, zatímco zbytek adresy může využít až dva nestrukturované prvky AdrLine. Důležité je, že [strukturované prvky se nesmějí opakovat uvnitř nestrukturovaných řádků ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); pro kteroukoli danou složku je adresa buď jedno, nebo druhé.

Plně nestrukturované adresy, kde celá adresa leží v prvcích AdrLine bez TwnNm či Ctry, nebudou přijaty u žádného z dotčených polí stran. European Payments Council sladil svůj rulebook SEPA se stejným přechodem, takže od [15. listopadu 2026 je nestrukturovaný formát zakázán také napříč SCT, SDD a SCT Inst ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). Sladění je záměrné: SWIFT a EPC připravily jediný přechodový víkend pro celé odvětví.

Pro vyloučení pochybností [dokumentace pacs008 uvádí dotčené zprávy přímo ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (plátce a příjemce v úhradách klientů), pacs.009 (adresy institucí v mezibankovních úhradách a krycích platbách), pacs.004 (adresy stran ve vratkách) a pacs.003 (inkasa). Požadavek působí i proti proudu: firemní soubory pain.001 nesoucí nestrukturované adresy zablokují generování vyhovujícího pacs.008 v přijímající bance.

## Proč z toho odvětví udělalo prioritu

Argument pro strukturované adresy není estetický. Je provozní a projevuje se na třech místech.

**Prověřování sankcí.** Jediný největší praktický přínos spočívá v tom, že strukturované adresy umožňují prověřovacím systémům oddělit název strany od lokalizačních dat. Bloky adres ve volném textu pravidelně způsobují falešně pozitivní shody, když se název města náhodou překrývá s tokenem jména sankcionované osoby nebo když je země vložená ve volném textu zcela přehlédnuta. Strukturovaná pole umožňují prověřovacím enginům deterministicky uplatňovat pravidla rizika specifická pro danou zemi a umožňují vynutit porovnávání se sankčním seznamem proti kódu země namísto odhadování z parsovaného řetězce. Analýza CGI UK zveřejněná v březnu 2026 tento bod výslovně zdůrazňuje: [strukturovaná adresní data se stávají ústředním prvkem provozní odolnosti, nikoli pouze povinností v oblasti compliance ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Míra ručních oprav.** Přeshraniční platby dnes nesou významné provozní náklady v podobě ručních šetření, zpracování výjimek a front na opravy, přičemž velkou část z toho pohánějí adresy, které prověřovací nebo směrovací systémy nedokážou s jistotou parsovat. Banky, které již přešly na strukturované adresy, hlásí podstatné snížení výjimek při přímém zpracování (straight-through processing), zejména v tocích uprostřed korridoru, kde zprostředkující agenti dříve museli interpretovat data ve volném textu, která sami nevytvořili.

**Vynucování na úrovni sítě.** SR2026 zpřísňuje validaci ve vrstvě sítě SWIFT. Některé z nových kontrol budou zpočátku fungovat v neblokujícím režimu, tedy budou označovat problémy s kvalitou dat, aniž by zastavovaly platby, ale trajektorie je jasná a po přechodu budou [nevyhovující zprávy rovnou odmítány ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Několik amerických platebních systémů (Fedwire, CHIPS) a SWIFT CBPR+ se sbíhá v podstatě na stejném harmonogramu, což odstraňuje možnost postupného přechodu, s níž některé instituce v dřívějších plánech počítaly.

## Pohled na úrovni polí: co se ve zprávě mění

Zpráva pacs.008 nese podporu strukturované adresy od doby, kdy v březnu 2023 vstoupily v platnost první pokyny pro použití CBPR+. Co se v listopadu 2026 mění, není schéma, nýbrž validace. Doposud směly banky plnit prvky AdrLine volným textem a předávat jej sítí. Od lhůty musí obsah bloků stran splňovat minimální požadavky na strukturovaná pole.

### Povinné, doporučené a vyřazené

| Prvek | XPath (pod `PstlAdr`) | Stav po listopadu 2026 | Poznámky |
|---|---|---|---|
| Název města | `<TwnNm>` | **Povinné** | Alespoň jeden strukturovaný název města na dotčenou stranu |
| Země | `<Ctry>` | **Povinné** | Kód ISO 3166-1 alpha-2 |
| Název ulice | `<StrtNm>` | Důrazně doporučené | Vyžadované pro plně strukturovaný formát |
| Číslo budovy | `<BldgNb>` | Doporučené | Buď BldgNb, nebo PstBx, ne obojí |
| Poštovní přihrádka | `<PstBx>` | Doporučené | Alternativa k BldgNb |
| PSČ | `<PstCd>` | Doporučené | Vyžadované některými místními schématy |
| Nižší územní celek | `<CtrySubDvsn>` | Volitelné | Stát, region, provincie |
| Řádek adresy (volný text) | `<AdrLine>` | **Omezené** | Max. 2 řádky v hybridním režimu; nikdy vedle téže složky ve strukturovaných polích |
| Typ adresy | `<AdrTp>` | Volitelné | U poštovních adres doporučeno použití `ADDR` |

*Zdroj: syntéza pokynů pro použití SWIFT CBPR+ pro SR2026 a [dokumentace strukturované adresy pacs008.com ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008").*

Praktickým důsledkem je, že každá instituce, která se stále spoléhá pouze na AdrLine, ať už ve vlastním generování zpráv, v souborech pain.001 přijatých od firemních klientů, nebo v záznamech kmenových dat používaných k obohacení plateb za letu, musí tato data před přechodem migrovat do strukturovaných polí. Průběžná překladová služba SWIFT může pomoci při přenosu, ale [od ledna 2026 podléhá příplatkům ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB") a nedokáže spolehlivě parsovat každý formát adresy. SWIFT rovněž vydal [model AI pro strukturování adres s otevřeným zdrojovým kódem ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"), natrénovaný na datech z více než 200 zemí, aby z nestrukturovaných starších dat odvodil město a zemi se skóre spolehlivosti, ale jde výslovně o pomůcku k nápravě, nikoli o dlouhodobou náhradu čistých vstupních dat.

## Jak pacs008.com pomáhá zkrátit časový plán

Pro instituce, které potřebují rychle industrializovat své pipeline pro kvalitu adres a validaci zpráv, poskytuje [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") sadu nástrojů s otevřeným zdrojovým kódem pod licencí MIT a službu FastAPI navrženou konkrétně pro pracovní postup mezibankovní úhrady klienta (FI-to-FI). Řeší tři vrstvy, na nichž programy nápravy nejčastěji uváznou: validace dat, generování XML a vynucování v pipeline.

Schopnosti sady nástrojů v oblasti strukturované adresy jsou sladěny s požadavky SR2026:

- **Validace před generováním** strukturovaných a hybridních polí poštovní adresy, takže nevyhovující data jsou zachycena dříve, než se jakékoli XML vytvoří nebo odešle.
- **Označování nestrukturovaných adresních dat**, která by po listopadové lhůtě 2026 neprošla, s jasným rozlišením mezi případy přijatelnými v hybridním režimu a plně nestrukturovanými.
- **Podpora dvou formátů** jak pro hybridní formáty před lhůtou, tak pro plně strukturovaná uspořádání po lhůtě, což institucím umožňuje migrovat postupně, aniž by narušily interoperabilitu s protistranami, které dosud nedokončily vlastní přechody.
- **Integrace do CI pipeline**, takže kontroly kvality adres se stanou součástí procesu sestavení, nikoli dodatečnou úvahou na konci toku; jde o praktickou odpověď na [pozorování CGI, že správa dat musí být základním principem návrhu ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"), nikoli vrstvou compliance přidanou navrch.

Kromě adres pokrývá sada nástrojů širší validační plochu, kterou vydání SR2026 zpřísňuje: validaci JSON Schema proti 20 schématům specifickým pro zprávy, ověření formátu a kontrolního součtu IBAN napříč 75 zeměmi, validaci XSD generovaného XML proti oficiálním schématům [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) a generování s ohledem na verzi napříč všemi 13 podporovanými revizemi pacs.008 (pacs.008.001.01 až pacs.008.001.13). Pro provozní a compliance týmy zahrnuje také prevenci XXE pomocí defusedxml, striktní ochranu proti path traversal a maskování PII ve strukturovaných protokolech JSON na podporu požadavků GDPR a PCI DSS; jde o druh kontrol, které jsou v produkčních platebních tocích nezbytné, ale při migracích vedených dodavatelem se často doplňují pozdě.

Knihovna je dostupná [na PyPI ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") jako balíček `pip install pacs008` a na [GitHubu ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") s plnou transparentností zdrojového kódu. Pro instituce, které zvažují své možnosti, na tom záleží: nástroje s otevřeným zdrojovým kódem umožňují interním týmům auditovat validační logiku, integrovat ji do stávajících prostředí Python nebo FastAPI bez vyjednávání o licencích a přispívat opravami, jakmile se objeví jejich vlastní hraniční případy.

Vyplatí se být přesný ohledně rozsahu. pacs008 je sada nástrojů na úrovni zpráv; nenahrazuje platební engine, prověřovací systém ani nápravu kmenových dat klientů, kterou instituce stále musí provést u zdroje. Co dělá, je, že tuto nápravnou práci vezme a učiní ji vynutitelnou: mění soulad se strukturovanou adresou z ruční kontroly na konci dlouhé pipeline v automatizovanou bránu v bodě generování. Pro programy s nedostatkem času je tato brána rozdílem mezi čistým přechodem a nárůstem odmítnutí po přechodu.

## Prostředí nástrojů

pacs008 se nachází v širším ekosystému nástrojů pro zprávy [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) a volba přístupu závisí na technologickém stacku, rozsahu a filozofii migrace dané instituce. Prostředí s otevřeným zdrojovým kódem i komerční prostředí zahrnuje [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (širokou vícekategoriovou knihovnu Python s validací v beta verzi), související knihovnu [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") pro iniciaci plateb proti proudu, [Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (komplexní knihovnu Java pod Apache 2.0 s komerční vrstvou pro validaci a překlady CBPR+) a řadu komerčních platforem (Mambu, Kyriba, PaymentComponents a další), které schopnost [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) zabalují do širších nabídek treasury nebo platebních platforem.

Kompromis je známý. Komerční platformy snižují zátěž vlastního inženýrství, ale vážou instituci na plán dodavatele, který nemusí odpovídat jejímu vlastnímu. Komplexní vícekategoriové knihovny pokrývají širší plochu, ale u kteréhokoli jednotlivého typu zprávy vyžadují více integrační práce. Zaměřené knihovny s otevřeným zdrojovým kódem (pacs008 pro mezibankovní úhradu klienta, [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) pro iniciaci plateb) minimalizují dobu integrace pro instituce, které potřebují rychle řešit konkrétní úzká místa, a ponechávají instituci kontrolu nad vlastními pravidly validace. Zejména u problému strukturované adresy má zaměřený přístup tu výhodu, že vynucovaná pravidla jsou úzká, dobře definovaná a je nepravděpodobné, že by se před přechodem změnila.

## Co to znamená podle sektorů

Listopadová lhůta 2026 nezasahuje všechny instituce stejně. Správná reakce závisí na objemu přeshraničního provozu, vyspělosti stávajícího datového prostředí a roli, kterou instituce hraje v platebním řetězci.

### Velké korespondentské a přeshraniční banky

Pro banky první úrovně provozující významný objem CBPR+ je požadavek na strukturovanou adresu jedním pracovním proudem v rámci mnohem širšího programu připravenosti SR2026, který zahrnuje také výjimky a šetření, zpevnění BAH a (v USA) souběžnou migraci Fedwire a CHIPS. Data RedCompass Labs naznačují, že většina těchto institucí vynakládá na připravenost pro rok 2026 20 až 30 milionů dolarů, s realizačními týmy o 10 až 20 specialistech. Rizikem pro tuto skupinu není technická způsobilost, nýbrž realizační kapacita. Když více paralelních pracovních proudů soupeří o stejná okna vydání, náprava kvality adres se může tiše opozdit za viditelnějšími proudy, až se z ní stane problém přechodového týdne. Praktickým opatřením je posunout validaci adres dopředu v pipeline, aby selhání vyplula na povrch ve vývojových a testovacích prostředích měsíce předtím, než by dosáhla produkce.

### Banky střední velikosti a platební instituce

Pro banky střední úrovně a instituce EMI/PI je požadavek na strukturovanou adresu často nejzávažnější povinností roku 2026, které čelí, protože nenesou stejnou okolní zátěž pracovních proudů jako banky první úrovně. Výzvou zde je obvykle kvalita vstupních dat. Procesy onboardingu klientů, které po desetiletí zachycovaly adresy jako volný text, produkují prostředí kmenových dat, jež nelze snadno parsovat. Automatizovaná náprava (s využitím modelu SWIFT pro strukturování adres s otevřeným zdrojovým kódem, komerčních služeb pro čištění adres nebo jejich kombinace) může vyřešit podstatnou část záznamů, ale zbytkový dlouhý chvost složitých mezinárodních adres bude vyžadovat ruční kontrolu. Čím dříve tato práce začne, tím menší tento chvost bude.

### Firmy a poskytovatelé platebních služeb

Firmy iniciující platby přes pain.001 jsou proti proudu od bankovního generování pacs.008, nejsou však z požadavku na strukturovanou adresu vyňaty. Banky nebudou zpětně doplňovat adresy příjemců za firemní klienty; strukturovaná data musí pocházet z vlastních systémů firmy. Pro firemní treasury to znamená zajistit, aby systémy ERP a treasury zachycovaly adresy příjemců ve strukturované podobě, aby informace o signatáři a konečném plátci byly obdobně strukturované a aby šablony iniciace plateb při generování souboru tiše nevynechávaly pole. Předběžná validace souborů pain.001 (s využitím buď vlastních nástrojů firmy, nebo služeb zpřístupněných bankou) se stává praktickým kontrolním bodem.

### Dodavatelé, fintechy a systémoví integrátoři

Pro dodavatele budující nad platebními systémy je lhůta vynucujícím faktorem pro schopnost [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html), která mohla být odsunuta do pozdějších fází. Fintechy, které přeshraniční platby směrují nebo iniciují prostřednictvím bankovních partnerů, musí zpřístupnit zachycení strukturované adresy ve svých vlastních UI a API, nebo přijmout, že z jejich dat nelze vytvořit vyhovující soubory pain.001. Příležitostí pro dodavatele, kteří se dokážou rychle pohnout, je převzít zátěž nápravy za firemní klienty a proměnit problém compliance ve službu.

## Závěr

Listopadová lhůta 2026 pro strukturovanou adresu je v jednom smyslu úzkou změnou: dvě povinná pole, několik doporučených a vyřazení volby volného textu, která se pro data relevantní pro sankce nikdy neměla používat. V jiném smyslu je to provozně nejvýznamnější milník [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) od původní migrace CBPR+, protože vynucuje strukturovaná data nejen do vrstvy zpráv, ale i do vstupních systémů, které ji napájejí.

Obraz připravenosti na úrovni odvětví šest měsíců před lhůtou není povzbudivý. Dvě třetiny zpráv CBPR+ stále nesou nestrukturované adresy. Téměř polovina bank není na dobré cestě. Téměř třetina záznamů klientských adres zůstává neparsovatelná. Financování je zajištěno (průzkumy soustavně ukazují osmi- a devíticiferné investice), ale práce nikoli, a rozměr problému spočívající v kvalitě dat nelze v posledních měsících vyřešit pouhými výdaji.

Co nyní pomáhá, je automatizace v bodě validace: přesunutí pravidel do pipeline, které problémy zachytí dříve, než dosáhnou sítě, nikoli poté. Pro instituce provozující prostředí Python nebo FastAPI poskytují nástroje s otevřeným zdrojovým kódem jako [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") praktický způsob, jak tento posun provést bez cyklu výběru dodavatele. Pro všechny, bez ohledu na stack, je strategický bod stejný: instituce, které změnu industrializují nyní, budou v mnohem silnější pozici než ty, které se spoléhají na compliance na poslední chvíli, abychom si vypůjčili formulaci výzkumu RedCompass Labs, který zarámoval velkou část konverzace roku 2026.

Přechodový víkend v listopadu uzavře jednu kapitolu. Instituce, které k němu dorazí s čistými daty, automatizovanou validací a funkčním porozuměním tomu, co strukturované adresy skutečně dělají pro prověřování sankcí, stráví tento víkend sledováním provozu. Ty, které dorazí bez těchto věcí, jej stráví na telefonech.

## Často kladené otázky

**Co přesně se k listopadové lhůtě 2026 mění?**

Od poloviny listopadu 2026 bude SWIFT CBPR+ odmítat zprávy pacs.008, pacs.009, pacs.004 a pacs.003, jejichž pole stran obsahují pouze nestrukturované poštovní adresy. Minimálním strukturovaným požadavkem je název města v prvku TwnNm a země v prvku Ctry (za použití kódu ISO 3166-1 alpha-2). Hybridní adresy jsou stále povoleny (město a země ve strukturovaných polích plus až dva prvky AdrLine ve volném textu pro zbývající složky), ale tatáž složka se nemůže objevit ve strukturovaných i nestrukturovaných polích zároveň. Plně strukturované adresy jsou preferovaným formátem. European Payments Council sladil schémata SEPA (SCT, SDD, SCT Inst) se stejným datem přechodu.

**Kterých zpráv a kterých polí stran se to týká?**

U pacs.008 se požadavek vztahuje na poštovní adresy plátce a příjemce. U pacs.009 se vztahuje na adresy institucí v mezibankovních úhradách a krycích platbách. U pacs.004 se vztahuje na adresy stran ve vratkách plateb. U pacs.003 se vztahuje na adresy příjemce a plátce v inkasech klientů. Zprávy o výpisech a oznámeních (camt.052, camt.053, camt.054) a některé administrativní zprávy zůstávají mimo striktní požadavek. Navazující zprávy pain.001 od firemních klientů nepodléhají přímo CBPR+, ale nestrukturované adresy v souborech pain.001 zablokují vyhovující generování pacs.008 dále po proudu, a jsou tak fakticky v rozsahu.

**Jaký je rozdíl mezi strukturovanou, hybridní a nestrukturovanou adresou?**

Plně strukturovaná adresa mapuje každou složku na její vyhrazený prvek [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html): StrtNm, BldgNb nebo PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. Hybridní adresa má název města a zemi ve strukturovaných polích, zbytek adresy pak v až dvou prvcích AdrLine ve volném textu; tatáž složka se nesmí objevit v obou. Nestrukturovaná adresa má celou poštovní adresu v prvcích AdrLine bez strukturovaných TwnNm či Ctry; to je formát vyřazovaný v listopadu 2026 u dotčených polí stran.

**Jak pacs008.com při tomto přechodu pomáhá?**

Knihovna [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") validuje strukturovaná a hybridní pole poštovní adresy před generováním XML, označuje nestrukturovaná data, která by po lhůtě neprošla, podporuje jak hybridní formáty před lhůtou, tak plně strukturované formáty po lhůtě a integruje se do CI pipeline a dávkových validačních postupů. Generuje XML pro všech 13 podporovaných verzí pacs.008, validuje proti oficiálním schématům XSD [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) a zpřístupňuje službu FastAPI pro automatizovanou orchestraci. Je open source pod licencí typu MIT, dostupná na PyPI a navržená konkrétně pro pracovní postupy mezibankovní úhrady klienta (FI-to-FI), takže pravidla validace jsou kalibrována podle pokynů pro použití SR2026 CBPR+, nikoli abstrahována přes mnoho typů zpráv.

**Co se stane, pokud moje instituce nebude do listopadu 2026 připravena?**

Zprávy s nestrukturovanými adresami v dotčených polích stran budou po přechodu odmítány na úrovni sítě. Prakticky se to promítne do selhání plateb, zvýšených objemů výjimek, nárůstů ručních oprav a pravděpodobného dopadu na klienty. Průběžná překladová služba SWIFT je pro některé přechodné případy dostupná, ale od ledna 2026 podléhá příplatkům a nedokáže spolehlivě parsovat každý formát adresy. SWIFT rovněž vydal model AI pro strukturování adres s otevřeným zdrojovým kódem, který z nestrukturovaných starších dat odvozuje město a zemi, ale je navržen pro nápravu a předzpracování, nikoli jako trvalá náhrada čistých vstupních dat. Instituce, které ke lhůtě dorazí bez napraveného prostředí kmenových dat klientů a automatizované validační pipeline, by měly očekávat obtížný přechodový týden a citelný nárůst provozní zátěže v následujících měsících.

## Odkazy

- Sebastien Rousseau, (2023). [Automating ISO 20022-Compliant Payment File Creation with Pain001](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html "Automating ISO 20022-Compliant Payment File Creation with Pain001").
- pacs008, (2026). [November 2026 structured-address deadline ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"). pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 Toolkit and API ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"). pacs008.com.
- SWIFT, (2026). [ISO 20022 milestone for November 2026: Unstructured addresses to be removed ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"). SWIFT.
- SWIFT, (2026). [ISO 20022 for Financial Institutions ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions "ISO 20022 for Financial Institutions"). SWIFT.
- SWIFT, (2026). [The Swift AI address structuring model ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"). SWIFT.
- RedCompass Labs, (2026). [Nearly Half of Banks Are Behind on ISO 20022 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022"). Financial IT.
- RedCompass Labs, (2026). [ISO 20022 is arriving all at once for US banks ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). RedCompass Labs.
- ClearingPost, (2026). [The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline"). ClearingPost.
- CGI UK, (2026). [2026: A defining year for ISO 20022 and structured data enforcement ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"). CGI UK.
- J.P. Morgan, (2026). [ISO 20022 Migration: Guidance, Messaging & More ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration "ISO 20022 Migration: Guidance, Messaging & More"). J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022 "FAQ Swift ISO 20022 — ING"). ING Wholesale Banking.
- Mambu, (2026). [CBPR+ is live: what ISO 20022 means in practice ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice "CBPR+ is live: what ISO 20022 means in practice"). Mambu.
- Kyriba, (2026). [ISO 20022 migration: what every treasury team needs to know about what's next ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/ "ISO 20022 migration: what every treasury team needs to know about what's next"). Kyriba.
- Standard Chartered, (2025). [ISO 20022 – Standard Chartered Address Guidelines (H2H and API) ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf "Standard Chartered ISO 20022 Address Guidelines"). Standard Chartered.
- State Street, (2025). [Client Guide to ISO 20022 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"). State Street.
- ISO 20022, (2026). [Message Definitions Catalogue ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 Message Definitions"). ISO 20022.
