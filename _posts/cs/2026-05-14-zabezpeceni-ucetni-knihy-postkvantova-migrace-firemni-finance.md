---
title: "Zabezpečení účetní knihy: příručka na úrovni správní rady k postkvantové migraci pro firemní finance"
subtitle: "Kvantové riziko přešlo od výzkumné zajímavosti k aktivnímu regulačnímu mandátu. S plánem G7 zveřejněným v lednu 2026 a s projektem BIS Project Leap, který prokázal proveditelnost v provozních platebních systémech, už otázka na úrovni správní rady nezní, zda migrovat. Zní, zda lze migraci dokončit dříve, než vyprší doba životnosti dnešních dat."
description: "Kvantové riziko přešlo od výzkumné zajímavosti k aktivnímu regulačnímu mandátu. S plánem G7 zveřejněným v lednu 2026, s vyjasněnými časovými plány EU, Spojeného království a ASD a s projektem BIS Project Leap, který prokázal proveditelnost na úrovni centrální banky, už otázka pro správní rady nezní, zda migrovat. Zní, zda lze migraci dokončit dříve, než vyprší kryptografická doba životnosti dnešních dat."
date: "May 14, 2026"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Diagram plánu migrace postkvantové kryptografie: infrastruktura firemního bankovnictví přecházející z RSA na ML-KEM a ML-DSA"
keywords: "postkvantová kryptografie, migrace PQC, firemní bankovnictví, finanční služby, plán G7 CEG, BIS Project Leap, ML-KEM, ML-DSA, FIPS 203, FIPS 204"
---

Kvantové riziko přešlo od výzkumné zajímavosti k aktivnímu regulačnímu mandátu. S plánem G7 zveřejněným v lednu 2026, s vyjasněnými časovými plány EU, Spojeného království a Austrálie a s projektem BIS Project Leap, který prokázal proveditelnost v provozních platebních systémech, už otázka pro správní rady nezní, zda migrovat. Zní, zda lze migraci dokončit dříve, než vyprší kryptografická doba životnosti dnešních dat.

---

> **Klíčové závěry**
>
> - **Rok 2026 je rokem, kdy regulační postoj ztvrdl.** Lednový plán G7 Cyber Expert Group, koordinovaný harmonogram EU NIS Cooperation Group a třífázový plán britské NCSC posunuly diskusi od povědomí k realizaci. Australian Signals Directorate zašla ještě dál a stanovila pevné datum konce roku 2030 pro klasickou asymetrickou kryptografii.
> - **Expozice je asymetrická.** RSA, ECC a Diffie–Hellman jsou bezprostředním problémem. Jde o asymetrické algoritmy, na nichž stojí handshaky SWIFT, TLS, PKI, podepisování kódu a autentizace clearingových sítí. Symetrické šifrování (AES-256) zůstává stabilní, pokud jsou zachovány délky klíčů. Pozornost správní rady musí směřovat na asymetrickou plochu.
> - **Harvest-now-decrypt-later není budoucí scénář.** Protivníci dnes zachycují a ukládají šifrované finanční protokoly, záznamy o vypořádání, materiály k fúzím a akvizicím (M&A) a data přeshraničních převodů s výslovným úmyslem je dešifrovat, jakmile bude existovat kryptograficky relevantní kvantový počítač (CRQC). Pro data s požadavkem na důvěrnost v délce 10 až 20 let je toto riziko již naplněno.
> - **Odvětví má nyní funkční referenční bod.** [BIS Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), zveřejněný v prosinci 2025, úspěšně nahradil tradiční digitální podpisy postkvantovou kryptografií v provozních převodech likvidity přes TARGET2 a odhalil konkrétní inženýrské náklady (latence ověření, velikost paketů), kterým bude čelit každý migrační program.
> - **Sada NIST je globální kotvou.** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") a FIPS 204 (ML-DSA) jsou referencovány každou významnou jurisdikcí, i tam, kde se národní postoje k sadám parametrů a hybridním požadavkům rozcházejí. Správní rady by měly považovat ML-KEM-768/ML-DSA-65 za spodní hranici a ML-KEM-1024/ML-DSA-87 za konzervativní základnu pro dlouhožijící data.
> - **Hybridní řešení je jedinou věrohodnou cestou.** Žádná významná autorita nedoporučuje přímé přepnutí. Souběžný provoz klasických a kvantově odolných algoritmů je model nasazení podporovaný NCSC, ANSSI, BSI a ověřený v projektu Project Leap. Je náročnější než kterákoli z alternativ, ale jako jediný řeší jak dnešní kompatibilitu, tak zítřejší hrozbu.

---

## Rok, kdy regulační postoj ztvrdl

Po většinu uplynulé dekády žila postkvantová kryptografie v pohodlném koutě dlouhodobého plánu. Kvantové počítače byly působivé, ale vzdálené; kryptografická matematika, na níž stojí RSA a eliptické křivky, se považovala za stabilní podklad; a diskuse o migraci se z velké části omezovala na specializované pracovní skupiny. Tento postoj již není udržitelný.

V lednu 2026 [G7 Cyber Expert Group zveřejnila své dosud nejzávažnější prohlášení ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "Prohlášení G7 CEG o pokroku v koordinovaném plánu přechodu na postkvantovou kryptografii ve finančním sektoru"), pod společným předsednictvím amerického ministerstva financí a Bank of England. Dokument není regulací, ale má větší váhu než běžný návod: představuje sdílený názor ministerstev financí, centrálních bank a dohledových orgánů napříč jurisdikcemi G7, že kryptografický přechod je nyní otázkou řízení systémového rizika. Plán zarovnává svůj plánovací horizont kolem poloviny 30. let, přičemž kritické finanční systémy jsou vybízeny k dřívější migraci. To je formulace, která v obezřetném jazyce centrálních bankéřů signalizuje očekávání, nikoli návrh.

O dva měsíce dříve zveřejnily BIS Innovation Hub a Eurosystém výsledky [Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), technického experimentu, který nahradil tradiční digitální podpisy postkvantovou kryptografií v provozních převodech likvidity mezi Bank of Italy, Banque de France, Deutsche Bundesbank, Nexi-Colt a Swift. Hlavní zjištění bylo úspěchem: kvantově odolně podepsané převody prošly celou cestou provozním platebním systémem. Detail pod titulkem je poučnější a je rozebrán dále v tomto článku.

Kombinace těchto dvou událostí, koordinovaného politického rámce G7 a funkčního důkazu v reálném platebním systému, přinesla to, na co technická komunita čekala deset let: jednoznačnou odpověď na otázku „je to skutečné?“ Odpověď v květnu 2026 zní ano. Zbývající otázkou je tempo.

## Tři vektory hrozeb, které by měly znepokojovat správní radu

Než probereme mechaniku migrace, vyplatí se přesně určit, co konkrétně je ohroženo. Kvantové riziko ve firemním bankovnictví není rovnoměrné napříč celým kryptografickým parkem a pozornost správní rady je nejlépe směřovat na tři vektory, kde je expozice nejakutnější.

### 1. Harvest Now, Decrypt Later (HNDL)

Nejbezprostřednější obava není budoucí. Je přítomná. Státní i vyspělí kriminální protivníci systematicky zachycují a ukládají šifrovaný finanční provoz, tedy převody, toky zpráv SWIFT, komunikaci k fúzím a akvizicím, protokoly přeshraničního vypořádání, swapové smlouvy a soubory KYC, aniž by je dnes dokázali číst. Jejich cíl je přímočarý: uložit nyní, dešifrovat později, jakmile bude existovat CRQC. Jak [Banka pro mezinárodní platby výslovně uvedla ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), tento sběr již probíhá.

Pro správní rady je důsledek nepříjemný, ale konkrétní: jakákoli citlivá data přenášená dnes pod klasickým asymetrickým šifrováním, jejichž požadavek na důvěrnost přesahuje příchod CRQC, je nutné již nyní považovat za vystavená. Při HNDL nepřijde žádné oznámení o narušení. V SIEM se nespustí žádný poplach. Šifrování drží, prozatím, ale data již opustila perimetr.

### 2. Riziko dlouhodobé citlivosti

Data firemního bankovnictví mají neobvykle dlouhou institucionální dobu životnosti. Strategická dokumentace k fúzím a akvizicím může zůstat citlivá pro trh po celou dekádu. Komunikace o obchodním tajemství a ocenění duševního vlastnictví mohou zůstat důvěrné patnáct až dvacet let. Protokoly přeshraničního vypořádání, expozice vůči centrálním protistranám a hodnocení úvěruschopnosti protistran si zachovávají obchodní citlivost dlouho po svém bezprostředním transakčním životě.

[Moscova rovnice ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), kterou původně formuloval Michele Mosca a která je nyní zabudována v každém seriózním migračním rámci, tento problém formalizuje. Je-li **S** doba životnosti dat, **M** čas potřebný k migraci systémů, které je chrání, a **Q** čas do dostupnosti CRQC, pak:

```
Pokud S + M > Q, jsou data již vystavena.
```

Pro data s dvacetiletým horizontem důvěrnosti a migrační program, který reálně vyžaduje pět až sedm let, je implicitní hodnota Q, na kterou správní rada sází, vzdálená nejméně 25 let. Rostoucí soubor odborných hodnocení, [predikce Forrester pro APAC na rok 2026 ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), každoroční průzkumy Global Risk Institute a architektonická studie z února 2026 navrhující CRQC při přibližně 100 000 fyzických qubitech s využitím kódů QLDPC, naznačuje, že tato sázka je riskantní.

### 3. Zranitelnost základních handshaků

Třetí vektor je architektonicky nejvýznamnější. Symetrické šifry (AES-256) zůstávají poměrně stabilní; Groverův algoritmus snižuje efektivní úroveň zabezpečení na polovinu, ale zdvojnásobení délky klíče obnovuje rezervu. Katastrofická expozice se týká asymetrických algoritmů a jsou to právě ty algoritmy, na nichž stojí každý autentizovaný handshake ve firemních financích: RSA v infrastruktuře veřejných klíčů SWIFT, ECDSA v autentizaci klient/server v TLS, ECDH při ustavení klíče relace a varianty ECC napříč mobilní autentizací klienta, podpisy API a řetězci podepisování kódu.

Funkční CRQC provozující Shorův algoritmus tyto systémy postupně neoslabuje. Prolomí je. Jakmile je CRQC v provozu, každý handshake chráněný RSA, každý podpis ECDSA a každá výměna klíčů na eliptických křivkách se stanou obnovitelnými, nikoli po měsících úsilí, ale během hodin. Přechod od „bezpečného“ ke „kompromitovanému“ je binární a šíří se současně napříč každým systémem, který používá dotčený algoritmus. To je základ, na němž stojí regulační naléhavost.

## Zpřísňování regulace: pohled podle jednotlivých jurisdikcí

Globální regulační obraz v květnu 2026 už není směsicí návrhů. Je to koordinovaný soubor časových plánů, které se liší přísností, ale sbíhají se ke stejnému cíli. Nadnárodní banka působící napříč hlavními finančními centry nyní podléhá nejpřísnější použitelné jurisdikci, nikoli té nejmírnější.

### Spojené státy

Spojené státy mají nejpreskriptivnější postoj pro jakoukoli instituci, která se dotýká federálních systémů. [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") od NSA nařizuje ML-KEM-1024 a ML-DSA-87 pro systémy národní bezpečnosti, přičemž nové systémy musí nasadit PQC od ledna 2027 a dokončit migraci infrastruktury do roku 2035. Memorandum OMB M-23-02 zavazuje federální agentury ke stejné trajektorii. Pro komerční banky vzniká bezprostřední expozice prostřednictvím federálních dodavatelských řetězců, zakázek v blízkosti NSS a nepřímého tlaku, který návod NSA vyvíjí na širší trh.

### Evropská unie

EU operuje ve třech vrstvách. [Koordinovaný implementační plán Evropské komise ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), který v červnu 2025 rozpracovala NIS Cooperation Group, stanovuje fázované milníky na roky 2026 (národní strategie), 2030 (migrace vysoce rizikových systémů) a 2035 (úplný přechod). Cyber Resilience Act bude od konce roku 2027 vyžadovat bezpečnostní aktualizace na úrovni současného stavu techniky pro digitální produkty. NIS2 posiluje řízení rizik v oblasti ICT, ačkoli ani jedna ze směrnic neobsahuje výslovný požadavek na PQC. Národní regulátoři však Komisi předběhli. Německý BSI nařizuje hybridní výměnu klíčů a schvaluje konzervativní koš ML-KEM, FrodoKEM a Classic McEliece. Francouzský ANSSI vyžaduje hybridní řešení jak pro zapouzdření klíčů, tak pro podpisy. Nizozemský NLNCSA a norské orgány se sjednotily na ML-KEM-1024 jako konzervativní základně pro dlouhožijící data.

### Spojené království

Britská NCSC zveřejnila svůj definitivní návod v březnu 2025 a potvrdila jej ve výroční zprávě Annual Review 2025. Třífázový časový plán je explicitní:

- **Do roku 2028:** identifikovat kryptografické služby vyžadující aktualizaci, sestavit migrační plán a vytvořit úplnou kryptografickou inventuru.
- **2028 až 2031:** provést vysoce prioritní aktualizace, zejména u kritických systémů a internetových protokolů vystavených navenek.
- **2031 až 2035:** dokončit migraci napříč všemi systémy, službami a produkty.

Pro britské finanční instituce stojí [návod PQC od CMORG (Cross-Market Operational Resilience Group) ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") vedle rámce NCSC, přičemž banky považuje za kritickou národní infrastrukturu a klade důraz na připravenost dodavatelů a sladění dodavatelského řetězce.

### Asie a Tichomoří

Postoj APAC je roztříštěnější, ale rychle se vyvíjí. Australská ASD má globálně nejtvrdší pozici: klasická kryptografie s veřejným klíčem se nesmí používat po konci roku 2030, žádné doporučení hybridního řešení a požadovaná ML-KEM-1024 (ML-KEM-768 přijatelná jen do roku 2030). Organizace by měly mít vypilovaný přechodový plán do konce roku 2026. Měnový úřad Singapuru (Monetary Authority) vydal formální návod k připravenosti na kvantovou bezpečnost. Japonsko a Jižní Korea investují podstatně, ačkoli oba mají národní algoritmické směry (Korea vybrala NTRU+ a SMAUG-T jako KEM, ALMer a HAETAE jako podpisy). Indická National Quantum Mission, podpořená vládním výdajem 6 003,65 crore rupií, výslovně označuje bankovní a finanční systémy za strategickou prioritu. [Predikce Forrester pro APAC na rok 2026 ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") odhadují počet regionálních podniků, které letos plánují investovat do postkvantových technologií, na více než 90 %.

### Výsledná pozice

Pro správní radu je praktická syntéza těchto jurisdikčních postojů přímočará. Nadnárodní banka se nemůže řídit časovým plánem jediného regulátora; musí se řídit tím nejpřísnějším použitelným. Pro většinu velkých institucí to znamená plánovací horizont konce roku 2030 pro vysoce rizikové systémy a konce roku 2035 pro dlouhý zbytek, přičemž subjekty vystavené ASD cílí na čisté PQC do roku 2030 a subjekty vystavené CNSA cílí na stejné období konkrétně s ML-KEM-1024 a ML-DSA-87.

## BIS Project Leap: co odvětví skutečně prokázalo

Project Leap si zaslouží pozornost správní rady ne proto, že by šlo o marketingový milník, ale proto, že jde o dosud nejvěrohodnější komplexní demonstraci postkvantové kryptografie v provozním finančním platebním systému. Hlavní závěr je přímočarý: funguje to. Detail pod povrchem je místem, kde sídlí provozní důsledky.

Fáze 1, dokončená v roce 2023, ustavila kvantově odolnou VPN mezi IT systémy Banque de France a Deutsche Bundesbank, přičemž platební zprávy se přenášely mezi Paříží a Frankfurtem pod hybridním šifrovacím schématem. Fáze 2, dokončená koncem roku 2025 a [zveřejněná v prosinci ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), zašla podstatně dále. Konsorcium nahradilo tradiční digitální podpisy založené na RSA postkvantovými podpisy při provádění převodů likvidity přes TARGET2, systém hrubého vypořádání v reálném čase Eurosystému. Účastníci, tedy BIS Innovation Hub Eurosystem Centre, Bank of Italy, Banque de France, Deutsche Bundesbank, Nexi-Colt (který zajišťuje konektivitu k TARGET2) a Swift, představují právě ty instituce, jejichž infrastruktura bude nakonec muset migrovat.

Zpráva zdůraznila tři zjištění, která by měl každý migrační program vzít za svá:

- **Latence ověření je citelně vyšší.** Ověření postkvantového podpisu trvalo na stejném hardwaru výrazně déle než ověření založené na RSA. Pro systém RTGS navržený kolem zpracování zpráv pod jednu sekundu to není okrajové pozorování; je to vstup pro plánování kapacity.
- **Velikosti paketů vyžadují přepracování systému.** Podpisy PQC jsou o řád větší než ekvivalenty ECDSA (více k tomu níže). Platební systémy, jejichž interní fronty, monitorovací nástroje a databázová schémata byly dimenzovány pro rozměry starších zpráv, nedokážou pojmout nový datový obsah bez přepracování. Project Leap výslovně zjistil, že TARGET2 nedokáže hybridní model „snadno pojmout“ bez podstatného přepracování.
- **Hybridní řešení je správnou odpovědí, ale je náročnější.** Souběžný provoz klasických a postkvantových algoritmů zachoval zpětnou kompatibilitu a poskytl hloubkovou obranu, ale zdvojnásobil režii kryptografického zpracování. To je provozní náklad správného provádění PQC během přechodu; nelze se mu vyhnout jen chytrým inženýrstvím.

Pro finančního ředitele (CFO), který posuzuje obchodní případ PQC, jsou zjištění Project Leap užitečná právě proto, že jsou přesná. Náklad postkvantové migrace není jediná kapitálová položka. Je to latence ověření, která se propisuje do smluv SLA, nárůst velikosti zpráv, který se dotýká rozpočtů na úložiště a šířku pásma, a přechodné období zdvojených kryptografických operací, které ovlivňuje plánování výpočetní kapacity. Nic z toho není spekulativní. Bylo to změřeno v provozním systému centrální banky.

## Sada nástrojů NIST: srovnání ML-KEM a ML-DSA

Technickým jádrem každého věrohodného národního rámce je sada postkvantových standardů NIST zveřejněná v srpnu 2024. Dva z těchto standardů jsou bezprostředním těžištěm pro firemní bankovnictví: ML-KEM (FIPS 203) pro zapouzdření klíčů a ML-DSA (FIPS 204) pro digitální podpisy. Sdílejí matematický základ, oba se opírají o obtížnost problémů Module Learning With Errors (ML-LWE) a Module Short Integer Solution nad strukturovanými mřížkami, ale v kryptografickém parku plní velmi odlišné role a jejich profily výkonu a velikosti se podstatně liší.

### ML-KEM (FIPS 203): zapouzdření klíčů

ML-KEM, odvozený z [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html), je náhradou za ECDH a RSA-KEM v protokolech, kde dvě strany potřebují ustavit sdílený symetrický klíč přes nezabezpečený kanál. Prakticky vzato je to místo, kam směřují handshaky TLS po vyřazení RSA a ECDH. NIST definuje tři sady parametrů s rostoucí bezpečnostní silou a klesajícím výkonem: ML-KEM-512 (NIST Kategorie 1), ML-KEM-768 (Kategorie 3) a ML-KEM-1024 (Kategorie 5).

### ML-DSA (FIPS 204): digitální podpisy

ML-DSA, odvozený z CRYSTALS-Dilithium, je náhradou za podpisy RSA a ECDSA. Zajišťuje podepisování certifikátů, podepisování kódu, podepisování dokumentů a autentizaci. Tři sady parametrů jsou ML-DSA-44, ML-DSA-65 a ML-DSA-87, které zhruba odpovídají NIST Kategoriím 2, 3 a 5.

### Profil velikosti a výkonu

Pro ředitele IT (CIO), který vymezuje migrační kapacitu, jsou nejdůležitějšími čísly velikosti artefaktů. Jsou to vstupy pro plánování síťové kapacity, projekce úložišť a testování na úrovni protokolu.

| Algoritmus | Veřejný klíč | Šifrový text / podpis | Nejbližší klasický ekvivalent | Velikost vs. klasika |
|---|---|---|---|---|
| ML-KEM-512 | 800 bajtů | 768 bajtů (šifrový text) | ECDH P-256 (~32 bajtů veř. klíč) | ~25× větší |
| ML-KEM-768 | 1 184 bajtů | 1 088 bajtů (šifrový text) | ECDH P-384 | ~25× větší |
| ML-KEM-1024 | 1 568 bajtů | 1 568 bajtů (šifrový text) | ECDH P-521 | ~25× větší |
| ML-DSA-44 | 1 312 bajtů | ~2 420 bajtů (podpis) | ECDSA P-256 (podpis 64 bajtů) | ~38× větší |
| ML-DSA-65 | 1 952 bajtů | ~3 293 bajtů (podpis) | ECDSA P-384 | ~50× větší |
| ML-DSA-87 | 2 592 bajtů | ~4 595 bajtů (podpis) | ECDSA P-521 | ~70× větší |

*Zdroj: syntéza specifikací [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") a FIPS 204, s porovnávacími daty z nezávislé benchmarkové literatury.*

Přímo z toho plynou tři provozní důsledky. **Zaprvé**, velikost podpisu je závazným omezením pro většinu podnikových nasazení. Podpis ML-DSA-65 je přibližně padesátkrát větší než podpis ECDSA P-256 a řetězce certifikátů TLS nesoucí zprostředkující CA rostou úměrně. Kapacitní práce na této ploše není volitelná; je nosná. **Zadruhé**, ML-KEM je výpočetně konkurenceschopná s ECDH a v některých implementacích citelně rychlejší, zejména na hardwaru s vektorizovanou podporou pro podkladovou mřížkovou aritmetiku. **Zatřetí**, ověření ML-DSA je trvale rychlé (často rychlejší než ověření ECDSA), ale podepisování ML-DSA zahrnuje smyčku rejection sampling, která může na omezeném hardwaru vyžadovat více pokusů. Pro služby podepisování s vysokou propustností je to benchmark, který je třeba ověřit, nikoli předpokládat.

### Volba sad parametrů

Jurisdikční postoje k volbě parametrů nejsou totožné, ale sbíhavost je zřejmá. ML-KEM-768 a ML-DSA-65 jsou podnikovou spodní hranicí, kterou britská NCSC podporuje jako základ pro britské organizace a která je přijatelná ve většině evropských rámců. ML-KEM-1024 a ML-DSA-87 jsou konzervativním stropem, který NSA CNSA 2.0 nařizuje pro americké systémy národní bezpečnosti a který ASD vyžaduje pro australské regulované subjekty do roku 2030. Pro data s extrémně dlouhodobou citlivostí, tedy suverénní protokoly vypořádání, duševní vlastnictví s horizontem přes deset let a záznamy o úschově dlouhodobých nástrojů, jsou vyšší sady parametrů obhajitelnou výchozí volbou.

### Sdílený matematický základ, sdílené riziko

Bod hodný pozornosti správní rady: ML-KEM i ML-DSA odvozují svou bezpečnost ze stejné rodiny mřížkových problémů. Budoucí kryptoanalytický průlom vůči Module-LWE by zasáhl oba standardy současně. Právě proto několik národních autorit, zejména německý BSI a francouzský ANSSI, doporučuje doplnit mřížkově založený stack o hashovací podpisy (SLH-DSA, FIPS 205) pro případy dlouhodobého podepisování a podepisování kódu. Kryptografická agilita v tomto smyslu není jen o schopnosti vyměnit RSA za ML-KEM. Je o schopnosti vyměnit jeden algoritmus PQC za druhý, když se změní stav kryptoanalýzy.

## Logická cesta migrace: zjištění → triáž → hybridní nasazení

Pro správní radu schvalující víceletý program PQC je provozní otázkou, jak práci rozfázovat, aniž by vzniklo nepřijatelné riziko dostupnosti služeb. Vzorec, který se vynořil napříč plánem G7, rámcem NCSC, projektem BIS Project Leap a hlavními národními dokumenty s návody, se sbíhá do tří fází.

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  1. ZJIŠTĚNÍ A CBOM  │ → │  2. TRIÁŽ (MOSCA)    │ → │  3. HYBRIDNÍ NASAZENÍ│
│  Kryptografická      │   │  Prioritizace podle  │   │  Dvojitá obálka      │
│  inventura všech     │   │  rizika dle doby     │   │  klasika + PQC,      │
│  systémů             │   │  životnosti dat      │   │  krypto-agilní       │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### Fáze 1: zjištění a kryptografický soupis materiálů (CBOM)

Migraci nelze naplánovat pro kryptografický park, který nebyl zmapován, a většina institucí přesnou mapu nemá. První fází je proto vytvoření kryptografického soupisu materiálů (Cryptographic Bill of Materials), tedy strukturované inventury každého výskytu asymetrické kryptografie v organizaci, kde je každý výskyt označen algoritmem, délkou klíče, protokolovým kontextem, citlivostí dat a vlastníkem systému. Automatizované skenování napříč kódovými bázemi, webovými aplikacemi, obrazy kontejnerů, konfiguracemi databází, úložišti certifikátů, hardwarovými bezpečnostními moduly a rozhraními dodavatelů je praktickým mechanismem; manuální inventura starších systémů a proprietárních protokolů je nevyhnutelným doplňkem.

Výstup fáze 1 není okázalý, ale je jediným základem, na němž mohou spočívat fáze 2 a 3. Je také výstupem, který většina útvarů interního auditu a externích regulátorů bude hledat jako první, jakmile se začnou vyžadovat atestace souladu s PQC.

### Fáze 2: triáž rizik pomocí Moscovy rovnice

S CBOM v ruce může instituce aplikovat Moscův rámec aktivum po aktivu. U každé kryptografické závislosti je otázkou, zda platí **S + M > Q**, tedy zda doba životnosti dat plus doba migrace přesahuje odhadovaný čas do CRQC. Aktiva, u nichž je nerovnost nejakutnější, tedy dlouhožijící citlivá data na infrastruktuře, jejíž migrace trvá roky, jdou na začátek fronty. Aktiva s krátkou dobou životnosti dat nebo již modernizovanou infrastrukturou lze v programu zařadit později.

Toto je fáze, kde je apetit správní rady k riziku nejviditelnější. Hodnota Q, kterou si instituce zvolí jako plánovací cíl, je v podstatě strategickou sázkou na tempo pokroku kvantového hardwaru. Konzervativní Q (polovina 30. let) vede k agresivnějšímu migračnímu plánu a vyšší kapitálové položce v blízkém období. Optimistická Q (po roce 2040) vede k uvolněnějšímu plánu a vyšší zbytkové expozici dat, která jsou již sbírána. Ani jedno není špatně; obojí by mělo být výslovným rozhodnutím správní rady, nikoli implicitní výchozí volbou technologického útvaru.

### Fáze 3: hybridní nasazení

Jakmile jsou prioritní aktiva identifikována, nasazení by mělo následovat hybridní vzorec ověřený v projektu Project Leap a podporovaný NCSC, ANSSI, BSI a plánem G7. Hybridní nasazení provozuje klasický algoritmus a postkvantový algoritmus souběžně a spojuje jejich výstupy do jediné obálky. Kompozit je bezpečný jak vůči klasickým útokům (klasický algoritmus drží dnes), tak vůči kvantovým útokům (algoritmus PQC drží zítra). Konkrétně je běžným vzorcem X25519 kombinovaný s ML-KEM-768 nebo ML-KEM-1024 pro zapouzdření klíčů a ECDSA kombinovaný s ML-DSA pro podpisy tam, kde jsou dvojité podpisy provozně proveditelné.

Zjištění Project Leap, že hybridní řešení je „mnohem, mnohem náročnější“ než kterýkoli z čistých přístupů, je poctivou protiváhou tohoto doporučení. Správní rady by měly během přechodu očekávat navýšení výpočetní a úložné kapacity, delší handshaky a další složitost řetězců certifikátů. Kompromisem je, že hybridní řešení odstraňuje jediný největší zdroj migračního rizika: skokové přepnutí z jednoho kryptografického základu na druhý v produkčním prostředí.

## Kolik to stojí a proč nečinnost stojí více

Analýza Mastercard, [zveřejněná počátkem roku 2026 ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs"), vyčíslila globální náklady na migraci PQC ve finančním sektoru na 28 až 42 miliard dolarů. V rámci tohoto souhrnu [výzkum RedCompass Labs a CMORG ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") sledující skutečné institucionální výdaje naznačuje, že banky první úrovně vyčleňují 20 až 30 milionů dolarů ročně na programy připravenosti, přičemž harmonogramy implementace zahrnují několik vedoucích cyklů. Jsou to podstatná čísla. Nejsou to však relevantní srovnání.

Relevantním srovnáním je náklad jediné události zpětného dešifrování. Pro instituci, jejíž nasbíraný provoz převodů, korespondence k fúzím a akvizicím nebo data o expozici vůči protistranám se v roce 2032 stanou čitelnými pro protivníka, není provozní a reputační náklad ohraničen položkou kapitálových výdajů na migraci. Je ohraničen hodnotou podkladové dekády strategických informací, která je pro jakoukoli systémově významnou instituci podstatně vyšší než jakýkoli věrohodný migrační rozpočet. Rámování kryptografického přechodu G7 jako otázky řízení systémového rizika, nikoli technologické aktualizace, je správné a správní rady by k němu měly přistupovat na tomto základě.

Existuje druhá nákladová položka, kterou se vyplatí oddělit. Migrace na PQC je vynucujícím faktorem pro kryptografickou agilitu, tedy architektonickou schopnost vyměňovat kryptografické algoritmy bez přestavby systémů, které na nich závisejí. Většina institucí dnes kryptografickou agilitu nemá; jejich závislosti na RSA a ECC jsou hluboce zabudovány do PKI, řetězců podepisování kódu, integrací dodavatelů a zakázkových protokolů, které se hromadily po desetiletí. Investice do agility, uskutečněná pod tlakem přechodu na PQC, je trvanlivá. Bude znovu využita, až přijde další kryptografický přechod, ať už je to nástupce mřížkově založené PQC, překryv kvantové distribuce klíčů, nebo něco, co ještě není na plánu standardů. Při správném zacházení jsou kapitálové výdaje na migraci PQC jednorázovou investicí, která přináší opakující se volnost volby.

## Závěr

Argument pro to, aby se postkvantová migrace považovala za prioritu správní rady v roce 2026, nestojí na bezprostřednosti CRQC. Odhady v tomto ohledu zůstávají skutečně nejisté; věrohodné odborné mínění klade pravděpodobnost CRQC do roku 2028 hluboko pod jedno procento a do let 2037 až 2040 zhruba na padesát procent. Argument stojí na třech dalších pozorováních, která nejsou nejistá.

Zaprvé, harvest-now-decrypt-later probíhá dnes a data s požadavkem na důvěrnost přesahujícím deset let jsou vystavena bez ohledu na to, kdy CRQC dorazí. Zadruhé, migrace kryptografického parku velké finanční instituce trvá pět až sedm let i při přiměřeném financování a soustředění vedení, což znamená, že program zahájený v roce 2026 skončí kolem roku 2031, což je dobře uvnitř konzervativního konce rozdělení pravděpodobnosti CRQC. Zatřetí, regulační očekávání se za posledních dvanáct měsíců podstatně zpřísnila a instituce, jejichž zápisy z jednání správní rady v roce 2026 zaznamenají jasný program PQC, budou v citelně silnější pozici než ty, jejichž zápisy zaznamenají jen vyčkávací postoj.

Instituce, které začnou nyní, mají výhodu volby. Mohou práci rozvrhnout napříč vedoucími cykly, integrovat ji se širšími iniciativami odolnosti a absorbovat provozní náklady hybridního nasazení v rámci běžného kapitálového plánování. Instituce, které vyčkávají, budou čelit stejné práci v napjatějších termínech, s menším prostorem pro rozvržení a na pozadí omezení dodávek hardwaru schopného PQC, odborných znalostí a kapacity dodavatelů. Náklad včasného jednání je známý; náklad pozdního jednání je asymetrický přesně tím způsobem, jemuž je řízení rizik navrženo předcházet.

Pro dřívější kontext na tomto webu: [dubnový text z roku 2026 o kompresi kvantových prahů](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") zkoumal podkladovou trajektorii hardwaru, [listopadová analýza CRYSTALS-Kyber z roku 2023](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") pokryla matematické základy nyní standardizované jako ML-KEM, [prosincový článek z roku 2023 o kvantové distribuci klíčů](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") se věnoval doplňkovému překryvu [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) a [open source referenční implementace KyberLib](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") poskytuje funkční implementaci podkladových primitiv v Rustu pro instituce, které chtějí kryptografickou plochu prozkoumat přímo. Zapojení do praktického a technického detailu, nikoli jen do regulačních titulků, je způsob, jímž správní rady odlišují věrohodné migrační programy od divadla souladu.

## Časté dotazy

**Kdy bude kryptograficky relevantní kvantový počítač skutečně existovat?**

Věrohodné odhady se značně liší. Počátkem roku 2026 dosáhly veřejné kvantové demonstrace zhruba 24 až 28 logických qubitů, zatímco u CRQC se odhaduje potřeba přibližně 6 000 logických qubitů podepřených něčím mezi 100 000 a několika miliony fyzických qubitů, v závislosti na přístupu k opravě chyb. Odborný konsenzus klade pravděpodobnost CRQC pod jedno procento do roku 2028 a kolem padesáti procent do let 2037 až 2040, s významnou variabilitou napříč prognózami. Nedávné snížení teoretických odhadů zdrojů, z 20 milionů qubitů před několika lety na méně než milion v Gidneyho práci z roku 2025 a na přibližně 100 000 ve studii architektury QLDPC z února 2026, stlačilo plánovací horizont. Pro potřeby správní rady je vhodným plánovacím předpokladem polovina 30. let pro vysoce rizikové systémy, konec 30. let jako konzervativní střed a dříve, pokud je expozice HNDL závaznou obavou.

**Proč hybridní nasazení místo čistě postkvantového?**

Tři důvody. Zaprvé, ML-KEM a ML-DSA, ač dobře prověřené, mají kratší kryptoanalytickou historii než RSA a ECC. Hybridní schéma zůstává bezpečné, pokud drží kterákoli složka; čistě PQC schéma je vystaveno, pokud je mřížkový problém nečekaně oslaben. Zadruhé, hybridní řešení zachovává zpětnou kompatibilitu s protistranami, které dosud nemigrovaly, což je kritické ve víceletém přechodu odvětví. Zatřetí, každá významná autorita mimo Australian Signals Directorate výslovně doporučuje hybridní řešení pro přechodné období: NCSC, ANSSI, BSI, NLNCSA i rámec G7 podporují přístup dvojité obálky. Kompromisem, jak Project Leap vyčíslil, je citelně vyšší režie výpočtu a úložiště. To je cena volnosti volby.

**Potřebujeme jak ML-KEM, tak ML-DSA, nebo si můžeme vybrat jeden?**

Oba. ML-KEM a ML-DSA plní odlišné kryptografické role. ML-KEM nahrazuje primitiva pro ustavení klíče v TLS, VPN, mobilní autentizaci a podobných protokolech, kde se dvě strany potřebují dohodnout na sdíleném symetrickém klíči. ML-DSA nahrazuje primitiva digitálního podpisu v certifikátech PKI, podepisování kódu, podepisování dokumentů, autentizovaných zprávách typu SWIFT a tvrzeních o identitě. Kryptografický park instituce používá oba druhy primitiv na různých místech; migrace musí pokrýt oba. Výrazně větší velikost podpisu ML-DSA (50 až 70× ECDSA) je obvykle provozně náročnějším z obou; práce na plánování sítě a úložiště pro ML-DSA dominuje většině hodnocení migrační kapacity.

**Jak měřit pokrok u tak rozsáhlého programu?**

Tři metriky jsou praktické a odpovídají hlavním regulačním rámcům. **Pokrytí CBOM**: jaké procento asymetrických kryptografických výskytů instituce bylo inventarizováno, klasifikováno a označeno migrační prioritou. **Migrační pokrytí vysoce rizikových aktiv**: jaké procento aktiv, u nichž platí Moscova podmínka S + M > Q, bylo převedeno na hybridní PQC. **Pokrytí kryptografickou agilitou**: jaké procento systémů s kryptografickou závislostí dokáže vyměnit algoritmy bez změn kódu, pouze konfigurací. Plán G7 CEG, třífázový rámec NCSC i koordinovaný plán EU se všechny zhruba mapují na tyto tři míry, i když používají odlišnou terminologii.

**Jaký je náklad dalšího roku čekání?**

Není nulový a není symetrický. Rok čekání znamená ztrátu jednoho roku ochrany HNDL u dlouhožijících dat; data, jejichž požadavek na důvěrnost sahá do roku 2040, jsou vystavena o rok déle, než je nutné. Stlačuje migrační okno vůči pevným regulačním termínům (ASD 2030, milníky NSA CNSA 2.0, cíl EU pro kritické systémy do roku 2030), což se promítá do vyššího rizika dodání a snížené flexibility rozvržení. Vystavuje instituci omezením dodávek ze strany dodavatelů a talentů, která jsou na trhu již viditelná a která se budou zhoršovat, jak se největší hráči odvětví přesunou od plánování k realizaci. Náklad není v žádném jednotlivém roce katastrofický, ale kumuluje se, a regulační prostředí se sbíhá k pozici, kde se od správních rad bude očekávat, že vysvětlí zpoždění, nikoli výdaj.

## Reference

- Sebastien Rousseau, (2026). [Quantum Thresholds Are Moving Again](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Sebastien Rousseau, (2023). [Quantum Key Distribution Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [KyberLib: A Rust-Powered Shield Against Quantum Threats](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats").
- G7 Cyber Expert Group, (2026). [Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement, January 2026"). GOV.UK.
- Bank for International Settlements, (2025). [Project Leap Phase 2: Quantum-Proofing Payment Systems ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"). BIS.
- Bank for International Settlements, (2025). [Project Leap: Quantum-Proofing the Financial System ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"). BIS.
- NIST, (2024). [FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard"). NIST.
- UK NCSC, (2025). [Timelines for Migration to Post-Quantum Cryptography ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines "Timelines for migration to post-quantum cryptography — NCSC"). UK National Cyber Security Centre.
- CMORG, (2025). [Guidance for Post-Quantum Cryptography ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"). Cross-Market Operational Resilience Group.
- Post-Quantum Cryptography Coalition, (2025). [International PQC Requirements ⧉](https://pqcc.org/international-pqc-requirements/ "International PQC Requirements — Post-Quantum Cryptography Coalition"). PQCC.
- PQShield, (2025). [PQC Roadmaps and Transition Guidance ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"). PQShield.
- Banking.Vision, (2026). [The Year of Quantum Computing: 2026 ⧉](https://banking.vision/en/the-year-of-quantum-computing/ "The Year of Quantum Computing 2026"). Banking.Vision / msg for banking.
- The Quantum Insider, (2026). [How to Prep For Post-Quantum Cryptography: G7 Releases Roadmap ⧉](https://thequantuminsider.com/2026/01/15/how-to-prep-for-post-quantum-crytography-g7-releases-roadmap-to-help-financial-sector-navigate-transition-to-quantum-era/ "How to Prep For Post-Quantum Cryptography — The Quantum Insider"). The Quantum Insider.
- Quantum Computing Report, (2026). [Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates ⧉](https://quantumcomputingreport.com/shor-qldpc-codes-and-the-compression-of-rsa-2048-resource-estimates-part-i/ "Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates"). Quantum Computing Report.
- Cryptomathic, (2025). [A Banker's Guide to Quantum Safe Cryptography — Roadmap to PQC Migration for Financial Institutions ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography"). Cryptomathic.
- Forrester, (2025). [2026 Asia Pacific Predictions: Quantum Security ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"). Forrester Research.
- The Asian Banker, (2025). [Building Resilience for a Quantum-Ready Financial System ⧉](https://www.theasianbanker.com/updates-and-articles/building-resilience-for-a-quantum-ready-financial-system "Building resilience for a quantum-ready financial system"). The Asian Banker.
