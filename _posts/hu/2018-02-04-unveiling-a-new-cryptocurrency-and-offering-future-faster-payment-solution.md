---
title: "Új kriptovaluta és gyorsabb fizetési megoldás bemutatása"
tags: "EXTC, ERC-223, Ethereum, smart contracts, cryptocurrency, blockchain, faster payments, decentralised finance, payment token, cross-border payments, ISO 20022, post-quantum cryptography, AI, tokenised deposits, stablecoins"
subtitle: "Új kriptovaluta és gyorsabb fizetési megoldás a pénzügyek következő generációja számára."
description: "2018 elején az EXTC platform gyorsabb, határokon átnyúló fizetéseket vizsgált Ethereum ERC-223 okosszerződéseken keresztül: korai tervrajz ahhoz, amit a decentralizált pénzügyek később felépítettek."
date: "Feb 04, 2018"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp"
banner_alt: "Kikapcsolt laptop egy barna fa asztal tetején"
keywords: "EXTC, ERC-223, Ethereum okosszerződések, gyorsabb fizetések, kriptovaluta, blokklánc-fizetések, fizetési token, decentralizált pénzügyek, ERC-20, határokon átnyúló fizetések"
---

![Egy nagyon magas épület, amelyen sok lyuk van](https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp).class=\"img-fluid clearfix\"

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - **Az alapfeltevés.** Az Ethereum okosszerződések kiválthatnák a levelezőbanki váltófutást a határokon átnyúló fizetéseknél, napok helyett másodpercek alatt teljesítve, és kiiktatva a 3-7%-os díjréteget ([World Bank, 2018](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data "World Bank Remittance Prices")).
> - **Az ERC-223 konkrét hozzájárulása.** A szabvány kijavította az ERC-20 néma tokenvesztési hibáját azzal, hogy megkövetelte az okosszerződésektől egy `tokenFallback` függvény közzétételét, így a sikertelen átutalások visszagördültek, ahelyett hogy visszafordíthatatlanul elégették volna a tokeneket ([Ethereum EIPs](https://eips.ethereum.org/EIPS/eip-20 "EIP-20: Token Standard")).
> - **Az EXTC fizetési primitívjei.** A token felépítése támogatta az egyszeri atomi átutalásokat, az időzített állandó megbízásokat, a többaláírásos vállalati kifizetéseket és az azonnali, fedezettel biztosított mikrohiteleket, mindezt elszámolóintézmény nélkül.
> - **Amit a kísérlet feltárt.** A technikai felépítés koherens volt, de az Ethereum főhálózata 2018-ban nagyjából 15 tranzakciót dolgozott fel másodpercenként. A nagy volumenű fizetésekhez olyan Layer-2 megoldások kellettek, amelyek még nem voltak éles használatra készek.
> - **Örökség.** Az EXTC-ben megjelenő architekturális ötletek, a programozható pénz, az atomi teljesítés és a megfelelőségbe ágyazott token-logika, később újra felbukkantak a DeFi-protokollokban, a CBDC-tervekben és a tokenizált betéti keretrendszerekben.

---

## A probléma: határokon átnyúló fizetések 2018-ban

A nemzetközi fizetések 2018 elején eleve lassúak, drágák és átláthatatlanok voltak. Egy lakossági átutalás az Egyesült Királyságból Délkelet-Ázsiába jellemzően két-négy levelezőbankot érintett, amelyek mindegyike díjat számított fel, és egy nappal meghosszabbította a teljesítési láncot. A World Bank Remittance Prices Worldwide adatbázisa 2018 első negyedévében 6,9%-os globális átlagköltséget rögzített egy 200 USD-s átutalásra.

A kriptovaluta már bebizonyította, hogy a peer-to-peer digitális készpénz technikailag megvalósítható. A Bitcoin nagyjából tíz perc alatt teljesítette a tranzakciókat világszerte, az Ethereum programozható rétege pedig okosszerződésekkel egészült ki: önvégrehajtó kóddal, amely a fizetési szabályokat közvetlenül magába az átutalásba képes kódolni. Az a rés, amely a láncon technikailag lehetséges és a régi levelezőbanki rendszer által nyújtott dolgok között tátongott, volt az a tervezési tér, amelybe az EXTC belépett.

## A technikai alap: az ERC-20 és a hibája

Az Ethereum Improvement Proposal 20 keretében formalizált ERC-20 szabvány definiálta a helyettesíthető tokenek kanonikus felületét: `balanceOf`, `transfer`, `transferFrom`, `approve` és `allowance`. 2018 elejére az ERC-20 volt a domináns tokenszabvány, több száz tokennel a főhálózaton.

Az ERC-20 azonban strukturális problémát hordozott. Amikor a tokeneket a standard `transfer` függvénnyel közvetlenül egy okosszerződés címére küldték, a szerződésnek nem volt módja észlelni a beérkező átutalást vagy reagálni rá. Az így küldött tokenek véglegesen csapdába estek. Az Ethereum-közösség becslése szerint 2018 közepéig több millió dollárnyi ERC-20 token veszett el ilyen módon.

Az ERC-223, amelyet Dexaran javasolt az Ethereum GitHub hibakövetőjében, ezt úgy kezelte, hogy a fogadó szerződéseken megkövetelt egy `tokenFallback(address _from, uint _value, bytes _data)` függvényt. Ha a fogadó szerződés nem valósította meg a `tokenFallback`-et, az átutalás visszagördült, és a tokenek visszakerültek a küldőhöz. Ez az ERC-223 átutalásokat atomivá tette: vagy elfogadta a szerződés a tokeneket és végrehajtotta a logikáját, vagy a tranzakció tisztán meghiúsult.

## Az EXTC token felépítése

Az Express Transaction Credits tokent öt alapvető jellemző köré tervezték:

- **Név, szimbólum és tizedesjegyek.** Standard ERC-223 azonosítómezők, 18 tizedesjeggyel a centnél kisebb pontosság érdekében.
- **Teljes kínálat.** A kibocsátáskor rögzítve, ami az EXTC-t deflációs eszközzé tette, mivel az elveszett vagy be nem váltott tokeneket nem lehetett újra kibocsátani.
- **Egyenleg és átutalás.** Standard olvasási és írási függvények, kiegészítve az ERC-223 `tokenFallback` követelményével.
- **Többaláírásos támogatás.** A vállalati kifizetések végrehajtás előtt több felhatalmazott cím együttes aláírását igényelték, ami auditnaplót biztosított központosított elszámolóház nélkül.
- **Időzárolt átutalások.** Egy állandó megbízás primitív lehetővé tette az EXTC számára a jövőbeli fizetések ütemezését: olyan képesség, amelyhez a hagyományos banki átutalások külső utasítást igényeltek.

## A platform célzott fizetési primitívjei

Az EXTC architektúrája négy konkrét fizetési munkafolyamat kiváltására készült, amelyeket a régi rendszerek nem hatékonyan kezeltek:

**Egyszeri atomi fizetések**: egyszeri átutalás, amely egyetlen Ethereum-tranzakcióban teljesült, jellemzően 15-30 másodpercen belül a 2018-as főhálózaton.

**Időalapú állandó megbízások**: időzárolt okosszerződés-hívásokként kódolt ismétlődő átutalások, amelyek kiküszöbölték, hogy egy banknak időszakos utasításokat kelljen fogadnia és újra végrehajtania.

**Vállalati tömeges kifizetések**: több címzettnek szóló kötegelt fizetések egyetlen tranzakcióban, ahol minden egyes átutalás többaláírásos engedélyezést igényelt, csökkentve a költséget és a partnerkockázatot.

**Fedezettel biztosított azonnali hitelek**: a hitelfelvevők EXTC tokeneket zároltak fedezetként egy okosszerződésben; a szerződés a beérkezéskor automatikusan folyósította a hitelösszeget, hitelbizottság vagy kockázatelbírálási késedelem nélkül.

## Amit a kísérlet feltárt

Az EXTC felépítése technikailag koherens volt. Az ERC-223 alap feloldotta a domináns tokenszabvány legjelentősebb biztonsági hibáját, a fizetési primitívek pedig közvetlenül leképezték azokat a valós munkafolyamatokat, amelyeket a levelezőbanki rendszer nem hatékonyan kezelt.

A gyakorlati korlátot az Ethereum áteresztőképessége jelentette. 2018 első negyedévében a főhálózat átlagosan 15 tranzakciót dolgozott fel másodpercenként, blokkonként megközelítőleg 8 milliós gázlimit mellett. Egy fizetési hálózat, amely a globális átutalási volumen akár csak kis töredékét is feldolgozná, a World Bank becslése szerint 2017-ben 270 millió migráns küldött haza pénzt, percek alatt telítette volna a főhálózatot.

A Layer-2 skálázási megoldások, különösen az állapotcsatornák és a később rollup technológiává vált korai változatok, 2018-ban aktív kutatás alatt álltak, de nem voltak éles használatra készek. A Lightning Network éppen 2018 januárjában indult el a Bitcoin főhálózatán, jelentős fenntartásokkal. A blokklánc-alapú fizetési hálózat levelezőbanki léptékű működéséhez szükséges technikai előfeltételek még nem léteztek.

## A túlélő ötletek

Az EXTC-ből és az egyidejű fizetési tokenprojektekből származó több architekturális koncepciót is igazolt a későbbi fejlődés:

**Programozható pénz**: a fizetési szabályok közvetlen kódolása az átutalási logikába, a DeFi hitelezési protokollok, például a Compound és az Aave központi jellemzőjévé vált, amelyek 2018-ban, illetve 2020-ban indultak.

**Atomi teljesítés elszámolóházak nélkül**: az a tulajdonság, hogy egy átutalás vagy teljesen sikeres, vagy visszagördül, mára tervezési követelmény a tokenizált betéti keretrendszerekben és a nagybani CBDC-architektúrákban, amelyeket olyan központi bankok vizsgálnak, mint a Bank of England és a European Central Bank.

**Megfelelőségbe ágyazott tokenek**: a magában a token-szerződésben kódolt átutalási korlátozások és jelentési kötelezettségek, megjelennek az olyan szabályozott tokenszabványokban, mint az ERC-1400 (értékpapír-tokenek), valamint a Project Agorá és hasonló többközponti-banki tokenizációs kísérletek megfelelőségi rétegének terveiben.

Az EXTC-kísérlet nem érte el az éles léptéket, de a kérdések, amelyeket feltett, a programozható teljesítésről, az atomi átutalásokról és az önérvényesítő fizetési szabályokról, a helyes kérdések voltak 2018-ban. A megválaszolásukhoz szükséges infrastruktúrának még öt évre volt szüksége, hogy beérjen.

## Gyakran ismételt kérdések

**Mi volt az ERC-223, és miért használta az EXTC az ERC-20 helyett?**

Az okosszerződés-címekre közvetlenül küldött ERC-20 tokenek némán elvesztek, mert a szerződéseknek nem volt módjuk észlelni a beérkező átutalást. Az ERC-223 ezt úgy javította ki, hogy megkövetelte a fogadó szerződésektől egy `tokenFallback` függvény megvalósítását; ha a függvény hiányzott, az átutalás visszagördült, ahelyett hogy elégette volna a tokeneket. Az EXTC azért választotta az ERC-223-at, hogy minden láncon belüli átutalás atomi és biztonságos legyen.

**Miért nem skálázódtak a korai fizetési tokenprojektek a levelezőbanki rendszer kiváltásáig?**

Az Ethereum főhálózata 2018-ban nagyjából 15 tranzakciót dolgozott fel másodpercenként. Már önmagában a globális átutalási volumen, a kereskedelemfinanszírozást és a vállalati fizetéseket nem is számítva, több tízezer tranzakciót igényelne másodpercenként. Az ehhez az áteresztőképességhez szükséges Layer-2 skálázási infrastruktúra csak 2021-2023 között vált éles használatra késszé.

**Mi lett az EXTC mögötti ötletekkel?**

Az alapkoncepciókat, a programozható fizetési szabályokat, az atomi teljesítést és a megfelelőségbe ágyazott token-logikát, átvették a DeFi-protokollok, a szabályozott értékpapír-token szabványok (ERC-1400) és a jegybanki digitális valuták kutatása. A most kereskedelmi bankok által pilotozott tokenizált betéti keretrendszerek közvetlenül azokra a tervezési kérdésekre vezethetők vissza, amelyeket az olyan korai fizetési tokenkísérletek, mint az EXTC, először feltettek.

**Hogyan viszonyul a 2018-as EXTC-felépítés a 2026-os tokenizált betéti javaslatokhoz?**

A teljesítési modell hasonló: pénzügyi követeléseket megtestesítő tokenek, amelyeket atomi módon utalnak át egy elosztott főkönyvben. A fő különbségek: (1) a 2026-os tokenizált betétek kereskedelmi banki kötelezettségek, nem pedig bemutatóra szóló tokenek; (2) engedélyezett vagy hibrid főkönyveken működnek szabályozói felügyelet mellett, nem pedig nyilvános főhálózaton; (3) a megfelelőséget és a személyazonosság-ellenőrzést a protokoll rétegében érvényesítik, nem pedig a résztvevőkre bízzák.

## Hivatkozások

- Ethereum Foundation, (2018). [EIP-20: Token Standard ⧉](https://eips.ethereum.org/EIPS/eip-20 "EIP-20 Token Standard").
- Dexaran, Ethereum GitHub, (2017). [ERC-223 Token Standard Proposal ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223 discussion").
- World Bank, (2018). [Remittance Prices Worldwide - Q1 2018 ⧉](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data "World Bank Remittance Prices").
- Buterin, V., (2014). [Ethereum: A Next-Generation Smart Contract and Decentralised Application Platform ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").

